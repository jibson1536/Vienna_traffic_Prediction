"""
Collect Wiener Linien disruptions and store them as one row per disruption event.

Each run (every 15 minutes via GitHub Actions):
  1. Fetch the live disruption feed from the Wiener Linien open data API.
  2. For every disruption in the feed:
       - new disruption      -> add a row with first_seen = last_seen = now
       - known disruption    -> update last_seen, times_seen and the latest text
  3. Save the events file.

Because one row = one event, the duration is simply last_seen - first_seen.
No grouping step is needed later, and the file stays small.
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import requests

API_URL = "https://www.wienerlinien.at/ogd_realtime/trafficInfoList"

# Relative path: works on any computer and on GitHub Actions
EVENTS_FILE = os.path.join("data", "live", "disruption_events.csv")

COLUMNS = [
    "event_id",          # stable id for the disruption
    "first_seen_utc",    # first time our collector saw it
    "last_seen_utc",     # last time our collector saw it
    "times_seen",        # number of runs in which it appeared
    "lines",             # affected lines, e.g. "U6|13A"
    "category_id",       # Wiener Linien category id
    "title",
    "description",
    "start_reported",    # start time reported by Wiener Linien (if given)
    "end_reported",      # planned end time reported by Wiener Linien (if given)
    "related_stops",     # stop ids, "|" separated
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def event_id(info: dict) -> str:
    """Use the API's own 'name' field if present, otherwise a hash of title + description."""
    if info.get("name"):
        return str(info["name"])
    raw = f"{info.get('title', '')}|{info.get('description', '')}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def join_list(values) -> str:
    if not values:
        return ""
    if isinstance(values, list):
        return "|".join(str(v) for v in values)
    return str(values)


def fetch_disruptions() -> list:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", {}).get("trafficInfos", []) or []


def load_events() -> dict:
    if not os.path.isfile(EVENTS_FILE):
        return {}
    with open(EVENTS_FILE, newline="", encoding="utf-8") as f:
        return {row["event_id"]: row for row in csv.DictReader(f)}


def save_events(events: dict) -> None:
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    rows = sorted(events.values(), key=lambda r: r["first_seen_utc"])
    with open(EVENTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def update_events(events: dict, infos: list, timestamp: str) -> tuple:
    new_count = 0
    for info in infos:
        eid = event_id(info)
        time_info = info.get("time") or {}
        latest = {
            "lines": join_list(info.get("relatedLines")),
            "category_id": str(info.get("refTrafficInfoCategoryId", "")),
            "title": info.get("title", "") or "",
            "description": (info.get("description", "") or "").replace("\n", " ").strip(),
            "start_reported": time_info.get("start", "") or "",
            "end_reported": time_info.get("end", "") or "",
            "related_stops": join_list(info.get("relatedStops")),
        }
        if eid in events:
            row = events[eid]
            row["last_seen_utc"] = timestamp
            row["times_seen"] = str(int(row.get("times_seen") or 0) + 1)
            # Update with the latest text, but never overwrite a value with an empty one
            row.update({k: v for k, v in latest.items() if v})
        else:
            events[eid] = {
                "event_id": eid,
                "first_seen_utc": timestamp,
                "last_seen_utc": timestamp,
                "times_seen": "1",
                **latest,
            }
            new_count += 1
    return new_count, len(infos)


def main() -> int:
    timestamp = now_utc()
    try:
        infos = fetch_disruptions()
    except Exception as exc:  # network error, API down, bad JSON
        print(f"{timestamp} ERROR fetching feed: {exc}")
        return 1

    events = load_events()
    new_count, active = update_events(events, infos, timestamp)
    save_events(events)
    print(f"{timestamp} active={active} new={new_count} total_events={len(events)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
