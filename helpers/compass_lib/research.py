"""Documented country blocks and narrow, hash-guarded ingestion only."""

import os
import re
import tempfile

from .common import (LIMIT, Problem, array, cell, contract, country_map, digest, fields, identity, named,
                     read, require, text, workspace)
from .files import resolve


def partition(payload):
    fields(payload, ("groups",), ("aliases",))
    maximum = contract()["batch_maximum"]
    batches, expected, seen = [], [], set()
    for group in array(payload["groups"]):
        fields(group, ("region", "countries"))
        region = text(group["region"])
        countries = array(group["countries"])
        for country in countries:
            key = identity(country, payload.get("aliases"))
            require(key not in seen, "Duplicate country in research scope: " + country)
            seen.add(key)
            expected.append(country)
        for start in range(0, len(countries), maximum):
            batches.append({"label": region + (" " + str(start // maximum + 1) if len(countries) > maximum else ""),
                            "countries": countries[start:start + maximum]})
    return {"batches": batches, "expected": expected}


def blocks(raw, scope=None, aliases=None):
    """Return source slices, not reconstructed datasets. Never infer prose boundaries."""
    lines = re.findall(r"[^\n]*\n|[^\n]+$", raw.decode("utf-8"))
    result, start, country, fence, report = [], None, None, None, len(lines)

    def add(first, end, name, issues=()):
        data = "".join(lines[first:end]).encode("utf-8")
        result.append({"index": len(result), "country": name, "start_line": first + 1,
                       "end_line": end, "sha256": digest(data), "issues": list(issues), "raw": data})

    for i, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})([^\r\n]*)", line)
        if fence:
            first, delimiter, explicit, headers = fence
            if marker and marker[1][0] == delimiter[0] and len(marker[1]) >= len(delimiter) and not marker[2].strip():
                if explicit:
                    if len(headers) == 1:
                        if any(line.strip() for line in lines[first + 1:headers[0][0]]):
                            raise Problem("needs_clarification", "Explicit dataset has pre-Country content; preserve and clarify its scope", line=first + 1)
                        add(headers[0][0], i, headers[0][1])
                    else:
                        add(first + 1, i, headers[0][1] if headers else None,
                            ["Explicit dataset must contain exactly one country"])
                fence = None
            elif explicit and (found := re.match(r"^Country:[ \t]*(.*?)\s*$", line)):
                headers.append((i, found[1]))
            continue
        if re.match(r"^## Validation report[ \t]*(?:\r?\n)?$", line):
            tail = "".join(lines[i:])
            owned = re.fullmatch(r"## Validation report\n<!-- agent-compass report sha256:([0-9a-f]{64}) -->\n(.*?)<!-- /agent-compass report -->\n?\s*", tail, re.DOTALL)
            if owned is None or digest(owned[2].encode("utf-8")) != owned[1] or re.search(r"^Country:", tail, re.MULTILINE):
                raise Problem("needs_clarification", "Report is legacy/edited or has appended research; preserve it and clarify before replacement", line=i + 1)
            report = i
            break
        if marker:
            explicit = marker[2].strip().lower() == "research" or start is None and marker[2].strip().lower() in ("", "text", "md", "markdown")
            if explicit and start is not None:
                add(start, i, country)
                start, country = None, None
            fence = (i, marker[1], explicit, [])
            continue
        if found := re.match(r"^Country:[ \t]*(.*?)\s*$", line):
            if start is not None:
                add(start, i, country)
            start, country = i, found[1]
    if fence:
        raise Problem("needs_clarification", "Unclosed research/code fence", line=fence[0] + 1)
    if start is not None:
        add(start, report, country)
    if not result and any(line.strip() for line in lines[:report]):
        preface = "".join(lines[:report]).lstrip()
        scope_section = re.fullmatch(r"## Research scope\r?\n(.*)", preface, re.DOTALL)
        scope_keys = {identity(name, aliases) for name in scope or []}
        metadata_only = scope is not None and scope_section is not None
        if metadata_only:
            for line in scope_section[1].split("\n"):
                line = line.strip().lstrip("-* ")
                if not line or not scope_keys and line.casefold() == "none":
                    continue
                values = [line] if identity(line, aliases) in scope_keys else line.split(",")
                if not all(identity(value, aliases) in scope_keys for value in values):
                    metadata_only = False
                    break
        if not metadata_only:
            raise Problem("needs_clarification", "No unambiguous Country blocks; clarify legacy boundaries")
    return result, "".join(lines[:report]).encode("utf-8")


def missing_fields(block, workflow, tracks):
    """Missing canonical labels need human semantic review, not guessed synonyms."""
    if workflow == "salary-calculator":
        required = {heading: ("low", "realistic", "strong", "sources") for heading in
                    ("mid-size / mainstream local-market tier", "premium / international / remote-first tier")}
        headings = {heading: heading for heading in required}
    else:
        required = {track: labels for track, labels in {
            "remote": ("confirmed salary range", "hiring prevalence evidence", "payment structure norms", "sources"),
            "sponsorship": ("visa or pathway name", "minimum salary threshold", "employer willingness",
                            "processing time", "quota or cap limitations", "family or dependent provisions",
                            "citizenship-specific considerations", "sources"),
        }.items() if track in tracks}
        headings = {track + " track": track for track in ("remote", "sponsorship")}
    sections, current, fence = {}, None, None
    for line in block["raw"].decode("utf-8").split("\n"):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})([^\r\n]*)", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        field = re.match(r"^ {0,3}(?:#{1,6}[ \t]+)?(?:[-+*] )?([^:\r\n]+):", line)
        if not field:
            continue
        label = field[1].strip().strip("*_").strip().casefold()
        heading = re.sub(r" \([^()]*\)$", "", label)
        if heading in headings:
            current = headings[heading]
            sections.setdefault(current, set())
        elif label in ("notes", "sponsorship salary threshold", "evidence grade"):
            current = None
        elif current is not None:
            sections[current].add(label)
    return [heading + ": " + label + ":" for heading, labels in required.items()
            for label in labels if label not in sections.get(heading, set())]


def inspect(payload, ingest=False):
    required = ("workspace", "workflow", "expected")
    optional = ("aliases", "required_tracks", "stage")
    if ingest:
        required += ("source_hash", "stored_hash", "decisions")
    fields(payload, required, optional)
    workflow = payload["workflow"]
    require(payload.get("stage", "research") in ("research", "discovery"), "Unknown research stage")
    discovery = payload.get("stage") == "discovery"
    require(not discovery or workflow == "country-finder" and not ingest, "Discovery scanning is read-only Country Finder only")
    root = workspace(payload["workspace"])
    layout = resolve(root, workflow)["files"]
    source = named(root, layout["candidates" if discovery else "research"])
    stored = named(root, layout["validated-data"])
    raw = read(source)
    old = read(stored) if stored.exists() and not discovery else b""
    aliases = payload.get("aliases")
    expected = payload["expected"]
    require(expected is None or isinstance(expected, list), "expected must be a country array or null for unknown legacy scope")
    expected_keys = [identity(name, aliases) for name in expected or []]
    require(len(set(expected_keys)) == len(expected_keys), "Duplicate expected country")
    parsed, prefix = blocks(raw, expected, aliases)
    stored_blocks = blocks(old)[0] if old.strip() else []
    tracks = payload.get("required_tracks", {})
    require(workflow != "country-finder" or discovery or "required_tracks" in payload,
            "Country Finder research needs explicit required_tracks from Step 2")
    require(isinstance(tracks, dict), "required_tracks must be an object")
    tracks = {name: array(values) for name, values in country_map(tracks, aliases).items()}
    require(all(values and set(values) <= {"remote", "sponsorship"} for values in tracks.values()), "Expected eligible track lists")
    old_keys, seen, duplicates = {}, set(), []
    for block in stored_blocks:
        require(block["country"] and not block["issues"], "Stored dataset has ambiguous country blocks")
        key = identity(block["country"], aliases)
        require(key not in old_keys, "Stored dataset already contains a duplicate; ask before changing it")
        old_keys[key] = block
    for block in parsed:
        if not block["country"]:
            block["issues"].append("Unrecognizable country")
            block["missing_fields"] = []
            continue
        try:
            key = identity(block["country"], aliases)
        except ValueError:
            block["issues"].append("Unrecognizable country")
            block["missing_fields"] = []
            continue
        block["key"] = key
        if key in seen:
            duplicates.append(block["index"])
        seen.add(key)
        block["missing_fields"] = [] if discovery else missing_fields(block, workflow, tracks.get(key, []))
        if workflow == "country-finder" and not discovery and key not in tracks:
            block["issues"].append("Country not eligible on either track")
    result = {"source_hash": digest(raw), "stored_hash": digest(old) if stored.exists() and not discovery else None,
              "blocks": [{k: v for k, v in block.items() if k not in ("raw", "key")} for block in parsed],
              "duplicate_blocks": duplicates, "expected_not_supplied": [name for name in expected or [] if identity(name, aliases) not in seen],
              "stored_countries": [b["country"] for b in stored_blocks], "coverage_known": expected is not None}
    return result, (source, stored, raw, old, prefix, parsed, old_keys)


def scan(payload):
    return inspect(payload)[0]


def replace(path, raw):
    """Atomic per file only. No multi-file transaction or new durable records."""
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def ingest(payload):
    result, (source, stored, raw, old, prefix, parsed, originals) = inspect(payload, True)
    require(isinstance(payload["source_hash"], str) and re.fullmatch(r"[0-9a-f]{64}", payload["source_hash"]), "Expected source SHA256")
    require(payload["stored_hash"] is None or isinstance(payload["stored_hash"], str) and re.fullmatch(r"[0-9a-f]{64}", payload["stored_hash"]), "Expected stored SHA256 or null")
    if result["source_hash"] != payload["source_hash"] or result["stored_hash"] != payload["stored_hash"]:
        raise Problem("conflict", "Research or stored data changed; rescan before retrying")
    decisions = {}
    for decision in array(payload["decisions"]):
        fields(decision, ("index", "accept"), ("reason", "reviewed_fields"))
        require(type(decision["index"]) is int and 0 <= decision["index"] < len(parsed) and decision["index"] not in decisions,
                "Each research block needs one unique decision index")
        require(type(decision["accept"]) is bool, "accept must be boolean")
        require("reviewed_fields" not in decision or type(decision["reviewed_fields"]) is bool, "reviewed_fields must be boolean")
        if not decision["accept"]:
            text(decision.get("reason"))
        decisions[decision["index"]] = decision
    require(set(decisions) == set(range(len(parsed))), "Review every research block before ingestion")
    accepted, rejected, new_blocks, matched_originals = dict(originals), [], [], set()
    for block in parsed:
        decision = decisions[block["index"]]
        key = block.get("key")
        reason = "; ".join(block["issues"])
        if not reason and not decision["accept"]:
            reason = decision["reason"]
        if not reason and key in accepted:
            if key not in matched_originals and block["raw"].rstrip(b"\r\n") == accepted[key]["raw"].rstrip(b"\r\n"):
                matched_originals.add(key)
                continue
            reason = "Duplicate; original retained"
        if not reason and block["missing_fields"] and not decision.get("reviewed_fields"):
            raise Problem("needs_clarification", "Canonical fields missing; reject or confirm a semantic legacy review",
                          block=block["index"], missing_fields=block["missing_fields"])
        if reason:
            rejected.append({"index": block["index"], "country": block["country"], "reason": reason})
        else:
            accepted[key] = block
            new_blocks.append(block["raw"])
            matched_originals.add(key)
    content = old
    for block in new_blocks:
        if content and not content.endswith(b"\n"):
            content += b"\n"
        content += block
    expected = payload["expected"]
    missing = [country for country in expected or [] if identity(country, payload.get("aliases")) not in accepted]
    report = "Stored: " + str(len(accepted)) + " countries.\n\n"
    report += "Stored countries: " + (", ".join(cell(b["country"]) for b in accepted.values()) or "none") + ".\n"
    for item in rejected:
        report += "\n- Skipped block " + str(item["index"]) + " (" + cell(item["country"] or "unrecognizable") + "): " + cell(item["reason"]) + "\n"
    report += "\nExpected countries not stored: " + (", ".join(cell(name) for name in missing) or "none") + ".\n"
    if expected is None:
        report += "\nLegacy research scope unknown; complete coverage cannot be established.\n"
    report = "## Validation report\n<!-- agent-compass report sha256:" + digest(report.encode("utf-8")) + " -->\n" + report + "<!-- /agent-compass report -->\n"
    separator = b"" if not prefix or prefix.endswith(b"\n\n") else b"\n" if prefix.endswith(b"\n") else b"\n\n"
    updated = prefix + separator + report.encode("utf-8")
    require(len(content) <= LIMIT and len(updated) <= LIMIT, "Combined research/report exceeds 4 MiB; no files written")
    writes = []
    try:
        # Recheck both hashes and symlinks immediately before any replacement.
        for path, previous in ((source, raw), (stored, old)):
            named(path.parent, path.name)
            if (read(path) if path.exists() else b"") != previous:
                raise Problem("conflict", "Workspace changed during ingestion; rescan", written_paths=writes)
        if content != old or not stored.exists():
            replace(stored, content)
            writes.append(stored.name)
        if updated != raw:
            replace(source, updated)
            writes.append(source.name)
    except OSError as error:
        raise Problem("io_error", str(error), written_paths=writes, state_unchanged=True) from error
    return {"stored": len(accepted), "rejected": rejected, "expected_not_stored": missing,
            "report_markdown": report, "written_paths": writes, "source_hash": digest(updated),
            "stored_hash": digest(content), "state_unchanged": True}
