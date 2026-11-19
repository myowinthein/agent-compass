"""Country-scoped, immutable Portal Finder reports; no profiles or checkpoints."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlsplit
import uuid

from .common import Problem, array, dated, digest, fields, identity, loads, named, read, require, text
from .files import registry
from .runs import directory, token
from .workspaces import base


def location(country):
    country = text(country).strip()
    require(len(country) <= 200 and not any(ord(c) < 32 for c in country), "Expected one country name")
    key = identity(country)
    spec = registry()["portal_reports"]
    root = directory(base(), spec["directory"])
    return directory(root, "country-" + digest(key.encode("utf-8"))), country, key, spec


def evidence(record):
    dated(record["evidence_date"])
    require(record["verification"] in ("live", "supplied", "mixed", "unverified"), "Unknown verification kind")
    require(record["coverage"] in ("complete", "partial", "none"), "Unknown coverage kind")
    sources = array(record["sources"])
    for source in sources:
        url = urlsplit(text(source))
        require(url.scheme in ("http", "https") and url.hostname and not url.username and not url.password,
                "Sources must be credential-free HTTP(S) URLs")
    if record["verification"] in ("live", "mixed"):
        require(bool(sources), "Live research needs its opened official source URLs")


def record_at(folder, report_id, country_key, spec):
    path = directory(folder, "report-" + token(report_id))
    record = loads(read(named(path, spec["metadata"])))
    fields(record, ("schema_version", "report_id", "country", "country_key", "saved_at", "evidence_date",
                    "verification", "coverage", "sources", "report_sha256"))
    require(type(record["schema_version"]) is int and record["schema_version"] == 1, "Unsupported portal report metadata")
    require(record["report_id"] == report_id and record["country_key"] == country_key and
            identity(record["country"]) == country_key, "Portal report country or identity mismatch")
    require(isinstance(record["saved_at"], str) and
            datetime.fromisoformat(record["saved_at"]).tzinfo == timezone.utc, "Saved report time must be UTC")
    evidence(record)
    raw = read(named(path, spec["report"]))
    require(bool(raw.strip()) and digest(raw) == record["report_sha256"], "Saved portal report is missing, empty or changed")
    return {**record, "path": str(path / spec["report"])}, raw


def catalog(folder, key, spec):
    if not folder.exists():
        return []
    reports = []
    for path in folder.iterdir():
        if path.name.casefold() in (".ds_store", "desktop.ini", "thumbs.db"):
            require(not path.is_symlink() and path.is_file(), "Unsafe OS metadata entry")
            continue
        if path.name.startswith(".creating-"):
            continue
        require(path.name.startswith("report-"), "Unexpected entry in this country's portal reports")
        reports.append(record_at(folder, path.name[7:], key, spec)[0])
    return sorted(reports, key=lambda r: (r["saved_at"], r["report_id"]), reverse=True)


def list_reports(payload):
    fields(payload, ("country",), ("include_history",))
    history = payload.get("include_history", False)
    require(type(history) is bool, "include_history must be a boolean")
    folder, country, key, spec = location(payload["country"])
    reports = catalog(folder, key, spec)
    result = {"country": country, "workspace": str(folder), "latest": reports[0] if reports else None}
    if history:
        result["reports"] = reports
    return result


def read_report(payload):
    fields(payload, ("country", "report_id", "expected_sha256"))
    folder, _, key, spec = location(payload["country"])
    record, raw = record_at(folder, payload["report_id"], key, spec)
    if payload["expected_sha256"] != record["report_sha256"]:
        raise Problem("conflict", "Saved report changed after selection; list again before viewing")
    return {**record, "report": raw.decode("utf-8")}


def save_report(payload):
    fields(payload, ("country", "evidence_date", "verification", "coverage", "sources", "report"))
    folder, country, key, spec = location(payload["country"])
    evidence(payload)
    raw = text(payload["report"]).encode("utf-8")
    report_id = uuid.uuid4().hex
    record = {"schema_version": 1, "report_id": report_id, "country": country, "country_key": key,
              "saved_at": datetime.now(timezone.utc).isoformat(), "evidence_date": payload["evidence_date"],
              "verification": payload["verification"], "coverage": payload["coverage"],
              "sources": payload["sources"], "report_sha256": digest(raw)}
    base(create=True)
    folder.parent.mkdir(mode=0o700, exist_ok=True)
    folder.mkdir(mode=0o700, exist_ok=True)
    # Never publish a partial report or replace an earlier run, even on retry.
    catalog(folder, key, spec)
    target = directory(folder, "report-" + report_id)
    require(not target.exists(), "Report ID collision; no report was replaced")
    with tempfile.TemporaryDirectory(prefix=".creating-", dir=folder) as temporary:
        staging = Path(temporary) / "report"
        staging.mkdir(mode=0o700)
        for name, data in {spec["report"]: raw,
                           spec["metadata"]: (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")}.items():
            with (staging / name).open("xb") as handle:
                os.chmod(staging / name, 0o600)
                handle.write(data)
        require(not target.exists(), "Report ID collision; no report was replaced")
        os.rename(staging, target)
    saved, actual = record_at(folder, report_id, key, spec)
    require(actual == raw, "Saved portal report readback differs")
    return saved
