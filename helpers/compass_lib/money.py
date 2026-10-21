"""Exact comparable amounts only; no FX lookup, taxes or legal decisions."""

from fractions import Fraction
from urllib.parse import urlsplit

from .common import array, contract, currency, dated, fields, number, require, text


def quote_legs(quotes):
    """Validate declarations even when other comparison facts are unknown."""
    require(len(array(quotes)) <= 2, "Use at most a two-leg cross quote")
    legs = []
    for quote in quotes:
        fields(quote, ("base", "quote", "rate", "date", "source"))
        base, target = currency(quote["base"]), currency(quote["quote"])
        require(base != target, "An FX leg must use two different currencies")
        rate = number(quote["rate"])
        require(rate > 0, "An FX rate must be positive")
        dated(quote["date"])
        source = urlsplit(text(quote["source"]))
        require(source.scheme in ("http", "https") and source.hostname, "Supply the named quote's HTTP(S) source URL")
        legs.append((base, target, rate))
    require(len({q["date"] for q in quotes}) <= 1, "Cross-rate dates must match")
    return legs


def exchange(start, end, quotes):
    """Resolve one explicit direct, reciprocal or two-leg cross quote."""
    if start == end:
        require(not quotes, "No FX quotes needed for identical currencies")
        return Fraction(1)
    require(bool(quotes), "An FX quote is required")
    legs = quote_legs(quotes)
    # Follow the given ordered legs. Never search or invent an extra conversion.
    current, multiplier = start, Fraction(1)
    visited = {start}
    for base, target, rate in legs:
        if current == base:
            current, multiplier = target, multiplier * rate
        elif current == target:
            current, multiplier = base, multiplier / rate
        else:
            raise ValueError("FX legs do not connect in the supplied order")
        require(current not in visited, "FX quote chain contains a cycle")
        visited.add(current)
    require(current == end, "FX quote chain does not reach the pay currency")
    return multiplier


def compare(payload):
    fields(payload, ("pay", "minimum"), ("quotes", "multiple"))
    pay, minimum = payload["pay"], payload["minimum"]
    fields(pay, ("low", "high", "currency", "period", "basis"))
    fields(minimum, ("amount", "currency", "period", "basis", "hard_floor"))
    require(type(minimum["hard_floor"]) is bool, "hard_floor must be a boolean")
    low, high = number(pay["low"]), number(pay["high"])
    amount = number(minimum["amount"])
    quotes = array(payload.get("quotes", []))
    quote_legs(quotes)
    require(low <= high, "Pay range is reversed")
    if "multiple" in payload:
        amount *= number(payload["multiple"])
    for item in (pay, minimum):
        if item["currency"] is not None:
            currency(item["currency"])
        require(item["period"] in ("annual", "monthly", None), "Unsupported pay period")
        require(item["basis"] in ("gross_base", "net", None), "Unsupported or unconfirmed pay basis")
    if (None in (pay["currency"], minimum["currency"], pay["period"], minimum["period"], pay["basis"], minimum["basis"])
            or pay["basis"] != minimum["basis"]):
        return {"outcome": "unverified", "reason": "Currency, period or comparable pay basis unavailable", "hard_floor_failed": False}
    if pay["currency"] != minimum["currency"] and not payload.get("quotes"):
        return {"outcome": "unverified", "reason": "Exchange rate unavailable", "hard_floor_failed": False}
    rate = exchange(minimum["currency"], pay["currency"], quotes)
    normalized = amount * rate
    if minimum["period"] != pay["period"]:
        normalized *= 12 if pay["period"] == "annual" else Fraction(1, 12)
    outcome = "pass" if low >= normalized else "fail" if high < normalized else "uncertain"
    return {"outcome": outcome, "normalized_minimum": str(normalized), "fx_multiplier": str(rate),
            "pay_period": pay["period"], "shortfall_at_maximum": str(max(normalized - high, Fraction(0))),
            "hard_floor_failed": outcome == "fail" and minimum["hard_floor"],
            "provenance_checked": "structure_only"}


def adjust(payload):
    fields(payload, ("low", "high", "typical", "label", "confidence", "salary_evidence"), ("evidence",))
    policy = contract()["adjustment"]
    low, high, typical = (number(payload[k]) for k in ("low", "high", "typical"))
    require(number(policy["minimum"]) <= low <= typical <= high <= number(policy["maximum"]),
            "Adjustment midpoint/range must lie within contract bounds")
    label = next(b["label"] for b in policy["bands"] if typical <= number(b["maximum"]))
    require(payload["label"] == label, "Adjustment label contradicts its midpoint")
    require(payload["confidence"] in policy["confidence"], "Unknown confidence")
    require(payload["salary_evidence"] in (*policy["confidence"], "not provided"), "Unknown salary evidence grade")
    if payload["salary_evidence"] == policy["confidence"][-1]:
        require(policy["confidence"].index(payload["confidence"]) >=
                policy["confidence"].index(policy["low_evidence_confidence_cap"]), "Confidence exceeds the Low-baseline cap")
    if typical > number(policy["evidence_above"]):
        text(payload.get("evidence"))
    return {"valid": True, "evidence_substantive": "not_checked"}
