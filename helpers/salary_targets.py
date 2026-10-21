"""Exact salary arithmetic for Step 4 and Step 5b; JSON stdin/stdout, no files.

Requires Python 3.11+. Interface: skills/salary-calculation-helper.md.
Policy and presentation: prompts/salary-calculator/step4-table-calculation.md.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import sys


def fields(value, required, optional=()):
    """Reject missing, unknown and non-object inputs instead of guessing."""
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    if set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ValueError("Expected fields: " + ", ".join(required) +
                         "; optional: " + ", ".join(optional))


def decimal(value):
    """Accept nonnegative plain decimal strings without float conversion."""
    if (not isinstance(value, str) or len(value) > 100 or
            re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) is None):
        raise ValueError("Amounts and percentages must be nonnegative plain decimal strings (up to 100 characters)")
    return Fraction(value)


def rounded(value, step):
    """Nearest increment, with exact halfway ties upward for nonnegative pay."""
    units = value / step + Fraction(1, 2)
    return units.numerator // units.denominator * step


def calculate(payload):
    """Calculate two employer segments and already-comparable numeric minima."""
    fields(payload, ("schema_version", "country", "currency", "pay_basis", "segments"), ("comparisons",))
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise ValueError("Unsupported schema_version; expected integer 1")
    if not isinstance(payload["country"], str) or not payload["country"].strip():
        raise ValueError("country must be a nonempty display name")
    if not isinstance(payload["currency"], str) or re.fullmatch(r"[A-Z]{3}", payload["currency"]) is None:
        raise ValueError("currency must be an explicit three-letter uppercase code")
    if payload["pay_basis"] != "gross_base":
        raise ValueError("Only confirmed gross_base pay is comparable")
    fields(payload["segments"], ("mainstream", "premium"))
    comparisons = payload.get("comparisons", {})
    fields(comparisons, (), ("visa", "candidate_minimum"))
    for comparison in comparisons.values():
        fields(comparison, ("amount", "period", "currency", "pay_basis"))
        decimal(comparison["amount"])
        if comparison["period"] not in ("annual", "monthly"):
            raise ValueError("Comparison period must be annual or monthly")
        if (comparison["currency"] != payload["currency"] or
                comparison["pay_basis"] != payload["pay_basis"]):
            raise ValueError("Comparison currency and pay basis must match the targets; no implicit FX or tax conversion")

    policy = contract()
    results = {}
    adjustments = set()
    for name, segment in payload["segments"].items():
        if isinstance(segment, dict) and "raw_annual_target" in segment:
            fields(segment, ("raw_annual_target",))
            annual = decimal(segment["raw_annual_target"])
        else:
            fields(segment, ("market_midpoint", "adjustment_percent"))
            adjustment = decimal(segment["adjustment_percent"])
            if adjustment > Fraction(policy["adjustment"]["maximum"]):
                raise ValueError("adjustment_percent exceeds Step 3's contract bound")
            adjustments.add(adjustment)
            if len(adjustments) > 1:
                raise ValueError("Both initial segments must use the country's same typical adjustment")
            annual = decimal(segment["market_midpoint"]) * (1 - adjustment / 100)
        checks = {}
        for label, comparison in comparisons.items():
            target = annual if comparison["period"] == "annual" else annual / 12
            minimum = decimal(comparison["amount"])
            checks[label] = {"target_in_period": str(target), "meets": target >= minimum,
                             "shortfall": str(max(minimum - target, Fraction(0)))}
        results[name] = {"raw_annual": str(annual), "raw_monthly": str(annual / 12),
                         "annual_display": rounded(annual, policy["salary"]["annual_increment"]),
                         "monthly_display": rounded(annual / 12, policy["salary"]["monthly_increment"]), "comparisons": checks}
    return {"input": payload, "segments": results}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field: " + key)
        result[key] = value
    return result


def reject_number(value):
    raise ValueError("JSON floats and nonfinite numbers are not supported; use plain decimal strings")


def contract():
    """One readable contract for both Python and approved manual processing."""
    return json.loads((Path(__file__).resolve().parents[1] / "data" / "output-contracts.json").read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if sys.version_info < (3, 11):
        print(json.dumps({"error": {"kind": "runtime_unavailable", "message": "Python 3.11 or newer is required"}}), file=sys.stderr)
        return 3
    try:
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise ValueError("Input exceeds 65536 bytes; send one country per invocation")
        payload = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_float=reject_number, parse_constant=reject_number)
        result = calculate(payload)
    except (ValueError, TypeError, RecursionError) as error:
        print(json.dumps({"error": {"kind": "invalid_input", "message": str(error)}}), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
