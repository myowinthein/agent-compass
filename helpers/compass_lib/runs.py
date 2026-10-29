"""Chat/person-scoped run selection. Prior runs and flat workspaces are never changed."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import uuid

from .common import ROOT, Problem, fields, loads, named, read, require, text, workspace
from .files import definition
from .state import check
from .workspaces import base


def checkpointed(workflow):
    registry = loads(read(ROOT / "data" / "workspace-files.json"))
    require(isinstance(workflow, str), "Expected a run workflow")
    if workflow in registry["runs"]["profile_workflows"]:
        return False
    definition(workflow)
    return True


def token(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{32}", value), "Expected a returned run/person ID")
    return value


def directory(parent, name):
    require(not parent.is_symlink(), "Unsafe run directory parent")
    require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", name) and name not in (".", ".."),
            "Invalid run directory name")
    path = parent / name
    require(not path.is_symlink() and (not path.exists() or path.is_dir()), "Unsafe run directory")
    return path


def location(payload):
    supplied = Path(text(payload["workspace"]))
    require(supplied.is_absolute(), "workspace must be an absolute directory")
    root = workspace(str(supplied)) if supplied.exists() else base()
    require(supplied.resolve() == root, "Missing workspace is not the fixed storage base")
    chat = text(payload["chat_id"])
    require(chat == chat.strip() and len(chat) <= 512 and all(ord(c) >= 32 for c in chat)
            and not any(c in chat for c in "${}<>"), "Supply an actual chat ID or chat-local random token")
    host, separator, identifier = chat.partition(":")
    require(separator and host in ("claude", "codex", "local") and identifier
            and not any(c.isspace() for c in identifier), "Expected a host-prefixed chat ID")
    if host == "local":
        value = uuid.UUID(identifier)
        require(value.version == 4 and str(value) == identifier,
                "Generate a canonical random UUID4 with a tool for the local chat token")
    spec = loads(read(ROOT / "data" / "workspace-files.json"))["runs"]
    key = hashlib.sha256(chat.encode("utf-8")).hexdigest()
    return directory(directory(root, spec["directory"]), "chat-" + key), key, spec["metadata"]


def catalog(folder, key, metadata):
    records = {}
    require(not folder.is_symlink(), "Unsafe chat directory")
    if not folder.exists():
        return records
    for path in sorted(folder.iterdir()):
        if path.name == ".DS_Store":
            require(not path.is_symlink() and path.is_file(), "Unsafe Finder metadata entry")
            continue
        if path.name.startswith(".creating-"):
            continue
        require(path.name.startswith("run-"), "Unexpected occupant in the selected chat's run directory")
        identifier = token(path.name[4:])
        require(directory(folder, path.name).is_dir(), "Missing run directory")
        record = loads(read(named(path, metadata)))
        fields(record, ("schema_version", "run_id", "chat_key", "person_id", "person_label", "workflow",
                        "created_at", "previous_run_id", "profile_source_run"))
        require(type(record["schema_version"]) is int and record["schema_version"] == 1, "Unsupported run metadata")
        require(record["run_id"] == identifier and record["chat_key"] == key, "Run identity mismatch")
        token(record["person_id"])
        label(record["person_label"])
        checkpointed(record["workflow"])
        require(isinstance(record["created_at"], str) and
                datetime.fromisoformat(record["created_at"]).tzinfo is not None, "Run time needs a timezone")
        for field in ("previous_run_id", "profile_source_run"):
            if record[field] is not None:
                token(record[field])
        records[identifier] = record
    for record in records.values():
        for field in ("previous_run_id", "profile_source_run"):
            reference = record[field]
            if reference is not None:
                require(reference in records, "Referenced run is missing")
                source = records[reference]
                require(source["person_id"] == record["person_id"], "Cross-person run reference")
                if field == "previous_run_id":
                    require(source["workflow"] == record["workflow"], "Cross-command baseline reference")
        seen = {record["run_id"]}
        previous = record["previous_run_id"]
        while previous is not None:
            require(previous not in seen, "Run baseline cycle")
            seen.add(previous)
            previous = records[previous]["previous_run_id"]
    return records


def label(value):
    require(isinstance(value, str) and bool(value.strip()) and value == value.strip()
            and len(value) <= 200 and all(ord(c) >= 32 for c in value), "Supply a confirmed person label")
    return value


def active(records, person, workflow):
    group = {key: r for key, r in records.items() if r["person_id"] == person and r["workflow"] == workflow}
    superseded = {r["previous_run_id"] for r in group.values()}
    leaves = [r for key, r in group.items() if key not in superseded]
    if len(leaves) > 1:
        raise Problem("conflict", "Multiple active runs; select/reconcile explicitly without deleting results")
    return leaves[0] if leaves else None


def list_runs(payload):
    fields(payload, ("workspace", "chat_id"), ("person_id", "workflow"))
    folder, key, metadata = location(payload)
    records = catalog(folder, key, metadata)
    person = token(payload["person_id"]) if "person_id" in payload else None
    workflow = payload.get("workflow")
    if workflow is not None:
        checkpointed(workflow)
    groups = sorted({(r["person_id"], r["workflow"]) for r in records.values()
                     if (person is None or r["person_id"] == person) and
                     (workflow is None or r["workflow"] == workflow)})
    result = []
    for person_id, command in groups:
        record = active(records, person_id, command)
        path = folder / ("run-" + record["run_id"])
        try:
            if checkpointed(command):
                status = check({"workspace": str(path), "workflow": command})
            else:
                profile = named(path, "profile.md")
                ready = profile.is_file() and bool(read(profile).strip())
                status = {"status": "ready" if ready else "profile_missing", "completed": False}
        except (ValueError, OSError) as error:
            status = {"status": "inconsistent", "completed": False, "error": str(error)}
        result.append({**record, "workspace": str(path), "status": status["status"],
                       "completed": status["completed"], "state": status.get("state"),
                       "missing": status.get("missing", []), "error": status.get("error")})
    return {"chat_key": key, "active_runs": result}


def start(payload):
    fields(payload, ("workspace", "chat_id", "workflow", "person_label"),
           ("person_id", "previous_run_id", "profile_source_run"))
    checkpointed(payload["workflow"])
    person_label = label(payload["person_label"])
    require(Path(text(payload["workspace"])).is_absolute()
            and Path(payload["workspace"]).resolve() == base(),
            "New searches must use the fixed home/Agent Compass storage base")
    folder, key, metadata = location(payload)
    records = catalog(folder, key, metadata)
    person = token(payload["person_id"]) if "person_id" in payload else uuid.uuid4().hex
    if "person_id" in payload:
        require(any(r["person_id"] == person for r in records.values()), "Person does not belong to this chat")
        require(all(r["person_label"] == person_label for r in records.values() if r["person_id"] == person),
                "Person label differs; clarify identity instead of reassigning saved work")
    baseline = active(records, person, payload["workflow"])
    previous = payload.get("previous_run_id")
    if previous is not None:
        token(previous)
    if previous != (baseline["run_id"] if baseline else None):
        raise Problem("conflict", "Starting fresh requires the exact active run selected by the user")
    source_id = payload.get("profile_source_run")
    copies = {}
    if source_id is not None:
        token(source_id)
        require(source_id in records and records[source_id]["person_id"] == person, "Profile source is not this person in this chat")
        source = folder / ("run-" + source_id)
        for name in ("profile.md", "situational-profile.md"):
            path = named(source, name)
            if path.exists():
                copies[name] = read(path)
    run_id = uuid.uuid4().hex
    record = {"schema_version": 1, "run_id": run_id, "chat_key": key, "person_id": person,
              "person_label": person_label, "workflow": payload["workflow"],
              "created_at": datetime.now(timezone.utc).isoformat(), "previous_run_id": previous,
              "profile_source_run": source_id}
    # These directories contain private candidate files. No existing run is rewritten.
    base(create=True)
    folder.parent.mkdir(mode=0o700, exist_ok=True)
    directory(folder.parent, folder.name)
    folder.mkdir(mode=0o700, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".creating-", dir=folder) as temporary:
        staging = Path(temporary) / "run"
        staging.mkdir(mode=0o700)
        for name, raw in {**copies, metadata: (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode()}.items():
            path = staging / name
            with path.open("xb") as handle:
                os.chmod(path, 0o600)
                handle.write(raw)
        if catalog(folder, key, metadata) != records:
            raise Problem("conflict", "Run catalog changed; reselect before starting")
        target = directory(folder, "run-" + run_id)
        require(not target.exists(), "Run ID collision; no result was replaced")
        os.rename(staging, target)
    return {**record, "workspace": str(target), "copied_profiles": sorted(copies)}
