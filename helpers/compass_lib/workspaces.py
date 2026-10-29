"""The one storage base shared by all Compass hosts on this OS account."""

from pathlib import Path

from .common import ROOT, fields, require


def base(create=False):
    home = Path.home()
    require(home.is_absolute() and home.is_dir(), "Cannot resolve an accessible user home directory")
    path = home / "Agent Compass"
    require(not path.is_symlink(), "The fixed storage base must not be a symlink")
    resolved = path.resolve()
    require(resolved != ROOT and ROOT not in resolved.parents, "Storage must be outside the plugin")
    require(not path.exists() or path.is_dir(), "The fixed storage base is occupied by a file")
    if create:
        path.mkdir(mode=0o700, exist_ok=True)
    return resolved


def resolve(payload):
    fields(payload, (), ("create",))
    create = payload.get("create", False)
    require(type(create) is bool, "create must be a boolean")
    path = base(create)
    return {"workspace": str(path), "exists": path.is_dir()}
