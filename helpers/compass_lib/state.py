"""Read-only checks. The parent still owns confirmation and checkpoint writes."""

from datetime import datetime

from .common import fields, loads, named, read, require, workspace
from .files import definition, resolve


def check(payload):
    fields(payload, ("workspace", "workflow"))
    root = workspace(payload["workspace"])
    layout = resolve(root, payload["workflow"])
    spec = definition(payload["workflow"])
    path = named(root, layout["files"]["state"])
    if not path.exists():
        return {**layout, "status": "missing", "completed": False}
    state = loads(read(path))
    fields(state, ("last_completed_step", "updated_at"))
    step = state["last_completed_step"]
    final_step = max(artifact["step"] for artifact in spec["artifacts"].values())
    require(type(step) is int and 0 <= step <= final_step, "Checkpoint step is out of range")
    require(isinstance(state["updated_at"], str), "updated_at must be a string")
    if state["updated_at"]:
        require(datetime.fromisoformat(state["updated_at"].replace("Z", "+00:00")).tzinfo is not None,
                "Checkpoint time requires an ISO8601 timezone")
    else:
        require(step == 0, "Completed steps need an ISO8601 timestamp")
    expected = [layout["files"][key] for key, artifact in spec["artifacts"].items() if artifact["step"] <= step]
    missing = [name for name in expected if not named(root, name).is_file()]
    final = layout["files"]["final-results"]
    if step == final_step and final not in missing and not read(named(root, final)).strip():
        missing.append(final)
    return {**layout, "status": "inconsistent" if missing else "complete" if step == final_step else "in_progress",
            "completed": step == final_step and not missing, "state": state, "missing": missing,
            "human_confirmation_checked": False}
