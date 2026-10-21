"""Shared Agent Compass mechanics. JSON stdin/stdout; only ingest writes files.

Read skills/helper-runtime.md and the relevant helper reference before use.
"""

import argparse
from pathlib import Path
import sys

# Isolated Python excludes the script directory. Add only this trusted bundle.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json


def emit(value, stream):
    stream.buffer.write((json.dumps(value, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8"))


def main():
    if sys.version_info < (3, 11):
        emit({"error": {"kind": "runtime_unavailable", "message": "Python 3.11 or newer is required"}}, sys.stderr)
        return 3
    from compass_lib import money, research, state, tables, timezones
    from compass_lib.common import LIMIT, Problem, loads, require
    commands = {"batch-partition": research.partition, "research-scan": research.scan, "ingest": research.ingest,
                "compare": money.compare, "adjust-check": money.adjust, "tz-offsets": timezones.offsets,
                "render-cf": tables.country, "render-salary": tables.salary,
                "check-saved": tables.check_saved, "state-check": state.check}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=commands)
    arguments = parser.parse_args()
    try:
        payload = loads(sys.stdin.buffer.read(LIMIT + 1))
        require(isinstance(payload, dict) and type(payload.get("schema_version")) is int and payload["schema_version"] == 1,
                "Expected schema_version integer1")
        original = dict(payload)
        del payload["schema_version"]
        result = commands[arguments.command](payload)
    except Problem as error:
        emit({"error": {"kind": error.kind, "message": str(error), **error.details}}, sys.stderr)
        return {"runtime_unavailable": 3, "needs_clarification": 4, "conflict": 5, "io_error": 6}[error.kind]
    except (ValueError, TypeError, KeyError, RecursionError, OverflowError) as error:
        emit({"error": {"kind": "invalid_input", "message": str(error)}}, sys.stderr)
        return 2
    except OSError as error:
        emit({"error": {"kind": "io_error", "message": str(error)}}, sys.stderr)
        return 6
    except Exception as error:
        emit({"error": {"kind": "internal_error", "message": type(error).__name__ + ": " + str(error)}}, sys.stderr)
        return 7
    emit({"schema_version": 1, "input": original, "result": result}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
