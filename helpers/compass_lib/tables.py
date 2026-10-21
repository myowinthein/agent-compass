"""Two fixed renderers. The caller supplies researched facts and judgments."""

from salary_targets import calculate
from .common import array, cell, contract, country_map, display_country, fields, identity, named, number, read, require, text, workspace
from .files import definition, resolve


def table(headers, rows, alignment=None):
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(alignment or ["---"] * len(headers)) + "|"]
    lines.extend("| " + " | ".join(cell(value) for value in row) + " |" for row in rows)
    return "\n".join(lines) + "\n"


def exact_display(value):
    """Format a terminating exact decimal without rounding a legal threshold."""
    amount = number(value)
    denominator, scale = amount.denominator, 0
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        raise ValueError("Numeric visa display needs an exact terminating amount; establish official precision or preserve Unknown")
    while (amount * 10 ** scale).denominator != 1:
        scale += 1
    integer = int(amount * 10 ** scale)
    if not scale:
        return f"{integer:,}"
    digits = str(integer).zfill(scale + 1)
    return f"{int(digits[:-scale]):,}." + digits[-scale:]


def salary(payload):
    fields(payload, ("rows",), ("priority_order", "aliases"))
    policy = contract()["salary"]
    priority = array(payload.get("priority_order", []))
    normalize = lambda value: identity(value, payload.get("aliases"))
    order = [normalize(country) for country in priority]
    require(len(set(order)) == len(order), "Duplicate country in priority_order")
    rows, calculations, notes, seen = [], [], [], set()
    for row in array(payload["rows"]):
        fields(row, ("country", "calculation", "visa"))
        country = display_country(row["country"])
        key = normalize(country)
        require(key not in seen, "Duplicate salary country")
        seen.add(key)
        result = calculate(row["calculation"])
        source = result["input"]
        require(normalize(source["country"]) == key, "Country does not match calculation")
        visa = row["visa"]
        fields(visa, ("state",), ("amount", "period", "currency", "pay_basis", "reason"))
        if visa["state"] == policy["numeric_state"]:
            require(set(visa) >= {"amount", "period", "currency", "pay_basis", "state"}, "Numeric visa rule needs amount, period, currency and pay_basis")
            require(visa["period"] in policy["period_suffixes"], "Unknown visa pay period")
            require(visa["currency"] == source["currency"] and visa["pay_basis"] == source["pay_basis"],
                    "Visa comparison needs the same currency and eligible base components")
            amount = number(visa["amount"])
            raw = [number(segment["raw_annual"] if visa["period"] == "annual" else segment["raw_monthly"])
                   for segment in result["segments"].values()]
            label = exact_display(visa["amount"]) + policy["period_suffixes"][visa["period"]]
            if any(value < amount for value in raw):
                label += " " + policy["warning"]
            recorded = source.get("comparisons", {}).get("visa")
            if recorded:
                require(number(recorded["amount"]) == amount and recorded["period"] == visa["period"],
                        "Visa rule contradicts the calculation input")
        else:
            require(visa["state"] in policy["visa_labels"], "Unknown visa state")
            require(not ({"amount", "period", "currency", "pay_basis"} & set(visa)), "Use no numeric comparison for a nonnumeric visa state")
            require("visa" not in source.get("comparisons", {}), "Remove numeric visa comparison for a nonnumeric state")
            label = policy["visa_labels"][visa["state"]]
            if visa["state"] == "Blocked":
                notes.append(country + ": " + text(visa.get("reason")) + "; targets are reference-only for sponsorship through this route.")
        mainstream, premium = (result["segments"][name] for name in ("mainstream", "premium"))
        rows.append((key, [country + " (" + source["currency"] + ")", label,
                           f"{mainstream['annual_display']:,}", f"{premium['annual_display']:,}",
                           f"{mainstream['monthly_display']:,}", f"{premium['monthly_display']:,}"]))
        calculations.append(result)
    rows.sort(key=lambda row: (order.index(row[0]) if row[0] in order else len(order),
                               "" if row[0] in order else row[0]))
    rendered = table(policy["headers"], [r[1] for r in rows], policy["alignment"])
    return {"markdown": policy["caption"] + "\n\n" + rendered,
            "table_markdown": rendered, "calculations": calculations, "notes": notes, "calculated": len(rows)}


def country(payload):
    fields(payload, ("expected", "decisions", "early_exclusions"), ("aliases",))
    policy = contract()["country"]
    fits, priorities = policy["fits"], policy["priorities"]
    normalize = lambda value: identity(value, payload.get("aliases"))
    expected = [normalize(name) for name in array(payload["expected"])]
    require(len(set(expected)) == len(expected), "Duplicate expected candidate")
    require(isinstance(payload["early_exclusions"], dict), "early_exclusions must be an object")
    early = country_map(payload["early_exclusions"], payload.get("aliases"))
    require(set(early) <= set(expected), "Early exclusion outside candidate universe")
    summary, candidates, notes, audit_notes, seen = [], [], {}, [], set()
    counts = {track: {"scored": 0, "excluded": 0, "not_scored": 0} for track in ("remote", "sponsorship")}
    for decision in array(payload["decisions"]):
        fields(decision, ("country", "remote", "sponsorship", "priority", "limitation", "ingestion"),
               ("remote_reason", "sponsorship_reason", "ingestion_reason"))
        name = display_country(decision["country"])
        key = normalize(name)
        require(key in expected and key not in seen, "Duplicate or unexpected final candidate")
        seen.add(key)
        values = [decision[track] for track in ("remote", "sponsorship")]
        require(all(f in fits.values() for f in values), "Unknown Summary fit")
        early_tracks = early.get(key, {})
        require(isinstance(early_tracks, dict) and set(early_tracks) <= {"remote", "sponsorship"}, "Invalid early exclusion track")
        for track in counts:
            fit = decision[track]
            if track in early_tracks:
                require(fit == fits["excluded"], "Early exclusion must not become missing data or a scored fit")
                require(decision.get(track + "_reason") == text(early_tracks[track]), "Preserve the exact early exclusion reason")
            if fit in (fits["excluded"], fits["missing"]):
                audit_notes.append(name + " " + track + ": " + text(decision.get(track + "_reason")))
            counts[track]["excluded" if fit == fits["excluded"] else "not_scored" if fit == fits["missing"] else "scored"] += 1
        usable = any(f in (fits["strong"], fits["moderate"]) for f in values)
        priority = decision["priority"]
        require(priority in priorities, "Unknown application priority")
        require(priority in priorities[:3] if usable else priority == priorities[-1] if fits["missing"] in values else priority == priorities[-2],
                "Priority contradicts the final track states")
        require(decision["ingestion"] in ("stored", "not_supplied", "rejected", "unknown"), "Unknown ingestion disposition")
        if decision["ingestion"] == "stored" or fits["excluded"] in values:
            summary.append([name, *values])
        else:
            require(all(f == fits["missing"] for f in values), "Scored tracks need stored research")
            heading = {"not_supplied": "Flagged but not researched", "rejected": "Researched but not ingested", "unknown": "Ingestion outcome unknown"}[decision["ingestion"]]
            notes.setdefault(heading, []).append(name + ": " + text(decision.get("ingestion_reason")))
        candidates.append((priorities.index(priority), key, [name, priority,
                           *(policy["missing_display"] if f == fits["missing"] else f for f in values), text(decision["limitation"])]))
    require(seen == set(expected), "Every expected candidate needs exactly one final decision")
    candidates.sort(key=lambda row: (row[0], row[1] if row[0] == len(priorities) - 1 else ""))
    rendered_summary = "## Summary\n\n" + table(policy["summary_headers"], summary)
    for heading, values in notes.items():
        rendered_summary += "\n### " + heading + "\n\n" + "\n".join("- " + cell(v) for v in values) + "\n"
    for track, count in counts.items():
        rendered_summary += f"\n- {track.title()}: {count['scored']} scored, {count['excluded']} excluded, {count['not_scored']} {fits['missing']}\n"
    rendered_table = table(policy["headers"], [r[2] for r in candidates])
    return {"summary_markdown": rendered_summary, "table_markdown": rendered_table,
            "markdown": rendered_summary + "\n## Priority Table\n\n" + rendered_table,
            "counts": counts, "audit_notes": audit_notes}


def check_saved(payload):
    fields(payload, ("workspace", "file", "kind", "render_input"))
    require(payload["kind"] in ("salary", "country"), "Unknown rendered kind")
    workflow = "salary-calculator" if payload["kind"] == "salary" else "country-finder"
    allowed = ("salary-table", "final-results") if payload["kind"] == "salary" else ("final-results",)
    matches = [key for key, artifact in definition(workflow)["artifacts"].items()
               if key in allowed and payload["file"] in (artifact["current"], artifact["legacy"])]
    require(len(matches) == 1, "Unsupported rendered output filename")
    root = workspace(payload["workspace"])
    saved = read(named(root, resolve(root, workflow)["files"][matches[0]])).decode("utf-8").replace("\r\n", "\n")
    rendered = salary(payload["render_input"]) if payload["kind"] == "salary" else country(payload["render_input"])
    header = rendered["table_markdown"].splitlines()[0] + "\n"
    require(saved.count(header) == 1, "Saved table must occur exactly once")
    tail = saved[saved.index(header):].splitlines(keepends=True)
    actual = ""
    for line in tail:
        if not line.startswith("|"):
            break
        actual += line
    require(actual.rstrip("\n") == rendered["table_markdown"].rstrip("\n"), "Saved table differs from canonical rendering")
    require(saved.count(rendered["markdown"].rstrip("\n")) == 1, "Saved caption/Summary differs from canonical rendering")
    return {"valid": True, "semantic_evidence_checked": False}
