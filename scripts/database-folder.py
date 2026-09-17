#!/usr/bin/env python3
"""Manage the modular DravyaGuna database.

Canonical editable data lives in data/plants/<id>.json, one record per plant.
The legacy plants.json file is assembled temporarily for the existing
validation/enrichment pipeline and removed from the repository after migration.

Commands:
  assemble  Build temporary plants.json from data/plants/*.json. On the first
            migration, if the modular folder is empty, preserve the existing
            plants.json as the migration source.
  split     Split temporary plants.json into one JSON file per record.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "data" / "plants"
AGGREGATE = ROOT / "plants.json"


def sort_key(record: dict):
    order = record.get("order", 9999)
    try:
        order = float(order)
    except (TypeError, ValueError):
        order = 9999
    return (order, str(record.get("identity", {}).get("name", record.get("id", ""))).lower())


def validate_records(records: list[dict]) -> None:
    ids = [str(r.get("id", "")).strip() for r in records]
    if not records:
        raise SystemExit("No plant records found")
    if any(not x for x in ids):
        raise SystemExit("Every plant record must have a non-empty id")
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate plant IDs detected")
    names = [str(r.get("identity", {}).get("name", "")).strip() for r in records]
    if any(not x for x in names):
        raise SystemExit("Every plant record must have identity.name")


def assemble() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    paths = [p for p in DB_DIR.glob("*.json") if p.name not in {"index.json", "schema.json"}]
    # First migration: the repository still contains the legacy aggregate.
    # Do not fail before it can be split into modular files.
    if not paths:
        if AGGREGATE.exists():
            print("No modular records yet; using existing plants.json as one-time migration source")
            return
        raise SystemExit("No modular plant JSON files and no legacy plants.json source found")

    records = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SystemExit(f"{path}: plant record must be a JSON object")
        records.append(data)
    records.sort(key=sort_key)
    validate_records(records)
    AGGREGATE.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Assembled temporary plants.json from {len(records)} modular records")


def split() -> None:
    if not AGGREGATE.exists():
        raise SystemExit("plants.json does not exist; run assemble first")
    data = json.loads(AGGREGATE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("plants.json must contain an array")
    validate_records(data)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    expected = set()
    for record in data:
        pid = str(record["id"]).strip()
        expected.add(f"{pid}.json")
        (DB_DIR / f"{pid}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    for path in DB_DIR.glob("*.json"):
        if path.name not in expected and path.name not in {"index.json", "schema.json"}:
            path.unlink()
    print(f"Split {len(data)} records into data/plants/<id>.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("assemble", "split"))
    args = parser.parse_args()
    if args.command == "assemble":
        assemble()
    else:
        split()


if __name__ == "__main__":
    main()
