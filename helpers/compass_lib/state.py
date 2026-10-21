"""Read-only checks. The parent still owns confirmation and checkpoint writes."""

from datetime import datetime

from .common import fields, loads, named, read, require, workspace


FILES = {
    "country-finder": ["cf-step1-criteria.md", "cf-step2-candidates.md", "cf-step3-country-research.md",
                       "cf-step4-country-data.md", "cf-step5-scoring-results.md", "cf-step6-final-ranking.md"],
    "salary-calculator": ["sc-step1-salary-research.md", "sc-step2-salary-data.md", "sc-step3-adjustment-values.md",
                          "sc-step4-salary-table.md", "sc-step5b-final-verification.md"],
}


def check(payload):
    fields(payload, ("workspace", "workflow"))
    require(payload["workflow"] in FILES, "Unknown checkpointed workflow")
    root = workspace(payload["workspace"])
    path = named(root, "." + payload["workflow"] + "-state.json")
    if not path.exists():
        return {"status": "missing", "completed": False}
    state = loads(read(path))
    fields(state, ("last_completed_step", "updated_at"))
    step = state["last_completed_step"]
    outputs = FILES[payload["workflow"]]
    require(type(step) is int and 0 <= step <= len(outputs), "Checkpoint step is out of range")
    require(isinstance(state["updated_at"], str), "updated_at must be a string")
    if state["updated_at"]:
        require(datetime.fromisoformat(state["updated_at"].replace("Z", "+00:00")).tzinfo is not None,
                "Checkpoint time requires an ISO8601 timezone")
    else:
        require(step == 0, "Completed steps need an ISO8601 timestamp")
    expected = outputs[:step]
    if payload["workflow"] == "salary-calculator" and step == len(outputs):
        expected = [*expected, "sc-step5a-career-ladder.md"]
    missing = [name for name in expected if not named(root, name).is_file()]
    if step == len(outputs) and outputs[-1] not in missing and not read(named(root, outputs[-1])).strip():
        missing.append(outputs[-1])
    return {"status": "inconsistent" if missing else "complete" if step == len(outputs) else "in_progress",
            "completed": step == len(outputs) and not missing, "state": state, "missing": missing,
            "human_confirmation_checked": False}
