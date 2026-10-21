"""Exact supplied-date calculations, never proof of seasonal coverage."""

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .common import Problem, array, fields, require, text


def local(value, zone):
    naive = datetime.fromisoformat(text(value))
    require("T" in value, "Supply an explicit local date and time, not a date-only midnight assumption")
    require(naive.tzinfo is None, "Local schedule endpoints must not contain a UTC offset")
    candidates = {naive.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
                  for fold in (0, 1)
                  if naive.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) == naive}
    if len(candidates) != 1:
        raise Problem("needs_clarification", "Ambiguous or nonexistent local time", local_time=value, zone=zone.key)
    return candidates.pop()


def offsets(payload):
    fields(payload, ("zones", "instants"), ("schedules",))
    require(len(array(payload["zones"])) == 2, "Supply exactly two IANA zones")
    try:
        zones = [ZoneInfo(text(name)) for name in payload["zones"]]
    except ZoneInfoNotFoundError as error:
        try:
            ZoneInfo("UTC")
        except ZoneInfoNotFoundError:
            raise Problem("runtime_unavailable", "Timezone data unavailable; use dated sources", zone=str(error)) from error
        raise ValueError("Unknown or unavailable IANA zone; check the supplied name: " + str(error)) from error
    evaluations = []
    for value in array(payload["instants"]):
        instant = datetime.fromisoformat(text(value).replace("Z", "+00:00"))
        require(instant.tzinfo is not None, "An instant must include its UTC offset")
        seconds = [int(instant.astimezone(z).utcoffset().total_seconds()) for z in zones]
        evaluations.append({"instant": value, "offset_seconds": seconds,
                            "absolute_difference_seconds": abs(seconds[0] - seconds[1])})
    overlaps = []
    for pair in array(payload.get("schedules", [])):
        require(len(array(pair)) == 2, "Supply one dated interval per zone")
        windows = []
        for window, zone in zip(pair, zones):
            fields(window, ("start", "end"))
            start, end = local(window["start"], zone), local(window["end"], zone)
            require(timedelta(0) < end - start <= timedelta(days=2),
                    "Use explicit increasing endpoints, including the next date for overnight hours")
            windows.append((start, end))
        overlaps.append(max(0, int((min(w[1] for w in windows) - max(w[0] for w in windows)).total_seconds())))
    require(bool(evaluations or overlaps), "Supply instants or dated schedules")
    return {"evaluations": evaluations, "overlap_seconds": overlaps,
            "evaluated_at_supplied_instants_only": True, "seasonal_coverage": "unverified",
            "tzdata_available": True, "tzdata_freshness": "not_established"}
