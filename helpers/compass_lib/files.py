"""One filename registry; read-only resolution without migration or alias copies."""

from .common import ROOT, Problem, fields, loads, named, read, require, workspace


def definition(workflow):
    registry = loads(read(ROOT / "data" / "workspace-files.json"))
    require(registry["schema_version"] == 1, "Unknown workspace filename registry")
    require(isinstance(workflow, str) and workflow in registry["workflows"], "Unknown checkpointed workflow")
    return registry["workflows"][workflow]


def resolve(root, workflow):
    """Keep existing names; use legacy for missing artifacts if this run has any."""
    spec = definition(workflow)
    present = {}
    spellings = set()
    for key, artifact in spec["artifacts"].items():
        found = [style for style in ("current", "legacy") if named(root, artifact[style]).is_file()]
        if len(found) > 1:
            raise Problem("conflict", "Both filenames exist for the same output; preserve them and ask which belongs to this run",
                          artifact=key, paths=[artifact[style] for style in found])
        if found:
            present[key] = artifact[found[0]]
            spellings.add(found[0])
    preferred = "legacy" if "legacy" in spellings else "current"
    return {"workflow": workflow, "naming": "mixed" if len(spellings) > 1 else preferred,
            "files": {"state": named(root, spec["state"]).name,
                      **{key: present.get(key, artifact[preferred]) for key, artifact in spec["artifacts"].items()}},
            "existing_outputs": list(present.values())}


def resolve_request(payload):
    fields(payload, ("workspace", "workflow"))
    return resolve(workspace(payload["workspace"]), payload["workflow"])
