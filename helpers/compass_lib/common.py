"""Strict transient data, explicit errors and bounded workspace access."""

from datetime import date
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import unicodedata

from salary_targets import contract, fields, unique_object, reject_number


ROOT = Path(__file__).resolve().parents[2]
LIMIT = 4 * 1024 * 1024


class Problem(ValueError):
    """A caller-actionable failure, optionally after a partial ingest write."""

    def __init__(self, kind, message, **details):
        super().__init__(message)
        self.kind = kind
        self.details = details


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "Expected nonempty text")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value), "Control characters are not supported")
    return value


def array(value):
    require(isinstance(value, list), "Expected a JSON array")
    return value


def number(value):
    require(isinstance(value, str) and len(value) <= 201 and
            re.fullmatch(r"[0-9]{1,100}(?:\.[0-9]{1,100}|/[0-9]{1,100})?", value),
            "Expected a nonnegative exact decimal or rational string")
    try:
        return Fraction(value)
    except ZeroDivisionError as error:
        raise ValueError("A denominator cannot be zero") from error


def currency(value):
    require(isinstance(value, str) and re.fullmatch(r"[A-Z]{3}", value), "Expected explicit uppercase three-letter currency")
    return value


def dated(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "Expected YYYY-MM-DD")
    return date.fromisoformat(value)


def loads(raw):
    require(len(raw) <= LIMIT, "Input exceeds 4 MiB")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                       parse_float=reject_number, parse_constant=reject_number)
    def depth(item, level=0):
        require(level <= 32, "Input nesting exceeds 32 levels")
        if isinstance(item, str):
            item.encode("utf-8")
        if isinstance(item, dict):
            for key in item:
                key.encode("utf-8")
        for child in item.values() if isinstance(item, dict) else item if isinstance(item, list) else ():
            depth(child, level + 1)
    depth(value)
    return value


def identity(value, aliases=None):
    cleaned = re.sub(r"^[\U0001F1E6-\U0001F1FF\ufe0f\s]+|[\U0001F1E6-\U0001F1FF\ufe0f\s]+$", "", text(value))
    key = " ".join(unicodedata.normalize("NFKC", cleaned).casefold().split())
    require(bool(key), "Country identity cannot contain only a flag")
    if aliases:
        require(isinstance(aliases, dict), "aliases must be an object")
        mapping = {}
        for alias, name in aliases.items():
            a, b = identity(alias), identity(name)
            require(a not in mapping or mapping[a] == b, "Conflicting normalized country aliases")
            mapping[a] = b
        require(all(mapping.get(value, value) == value for value in mapping.values()), "Aliases must point directly to canonical names")
        key = mapping.get(key, key)
    return key


def cell(value):
    return " ".join(text(value).split()).replace("&", "&amp;").replace("<", "&lt;").replace(
        ">", "&gt;").replace("|", "&#124;").replace("*", "&#42;").replace("`", "&#96;")


def country_map(value, aliases=None):
    require(isinstance(value, dict), "Expected a country-keyed object")
    result = {}
    for name, item in value.items():
        key = identity(name, aliases)
        require(key not in result, "Duplicate normalized country key")
        result[key] = item
    return result


def display_country(value):
    value = text(value).strip()
    flags = re.findall(r"[\U0001F1E6-\U0001F1FF]{2}", value)
    require(len(flags) == 1, "Supply one researched country flag with the display name")
    name = value.replace(flags[0], "").strip()
    text(name)
    return flags[0] + " " + name


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def workspace(value):
    path = Path(text(value))
    require(path.is_absolute() and path.is_dir(), "workspace must be an existing absolute directory")
    path = path.resolve()
    require(path != ROOT and ROOT not in path.parents, "Consumer workspace must be outside the plugin")
    return path


def named(root, name):
    """Callers pass only their fixed supported filenames, never arbitrary paths."""
    path = root / name
    require(not path.is_symlink() and path.resolve().parent == root,
            "Refusing symlink or outside-workspace file: " + name)
    require(not path.exists() or path.is_file(), "Expected a regular file: " + name)
    return path


def read(path):
    with path.open("rb") as handle:
        raw = handle.read(LIMIT + 1)
    require(len(raw) <= LIMIT, "File exceeds 4 MiB: " + path.name)
    raw.decode("utf-8")
    return raw
