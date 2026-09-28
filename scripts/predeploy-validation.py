#!/usr/bin/env python3
"""Pre-deployment integrity checks for DravyaGuna 97."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "plants"
MANIFEST = ROOT / "data" / "curated-image-manifest.json"
REPORT = ROOT / "data" / "image-audit-report.json"

errors = []

def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None

records = []
for path in sorted(DB.glob("*.json")):
    if path.name in {"index.json", "schema.json"}:
        continue
    data = load(path)
    if isinstance(data, dict):
        records.append((path, data))

canonical = [
    (path, data) for path, data in records
    if data.get("category") == "NCISM-97"
    and isinstance(data.get("order"), int)
    and 1 <= data["order"] <= 97
]

if len(canonical) != 97:
    errors.append(f"Expected 97 canonical NCISM records; found {len(canonical)}")

ids = [str(data.get("id", "")).strip() for _, data in canonical]
orders = [data.get("order") for _, data in canonical]
if len(ids) != len(set(ids)):
    errors.append("Duplicate canonical plant IDs")
if sorted(orders) != list(range(1, 98)):
    errors.append("Canonical plant orders must be exactly 1..97")
for path, data in canonical:
    if path.stem != str(data.get("id", "")).strip():
        errors.append(f"{path.name}: filename does not match plant id")

manifest = load(MANIFEST)
if isinstance(manifest, dict):
    parts = manifest.get("parts") or []
    rows = manifest.get("records") or []
    if len(parts) != 9:
        errors.append(f"Image manifest must define 9 plant parts; found {len(parts)}")
    expected = {(str(data.get("id")), int(data.get("order")), part)
               for _, data in canonical for part in parts}
    actual = {(str(row.get("plant_id")), row.get("ncism_order"), row.get("part"))
              for row in rows if isinstance(row, dict)}
    if len(rows) != 873:
        errors.append(f"Image manifest must contain 873 slots; found {len(rows)}")
    if expected != actual:
        errors.append("Image manifest plant/order/part coverage does not match the 97×9 canonical matrix")
    statuses = {str(row.get("verification_status", "")) for row in rows if isinstance(row, dict)}
    allowed = {"verified-local", "missing-queued", "download-failed"}
    unexpected = sorted(statuses - allowed)
    if unexpected:
        errors.append(f"Unexpected image verification statuses: {unexpected}")
    # A verified-local row is valid only when the referenced file is actually in the repository.
    canonical_by_id = {str(data.get("id")): data for _, data in canonical}
    for row in rows:
        if not isinstance(row, dict) or row.get("verification_status") != "verified-local":
            continue
        image_path = str(row.get("image_path", "")).strip()
        if not image_path:
            errors.append(f"verified-local image has no image_path: {row.get('plant_id')}/{row.get('part')}")
        elif not (ROOT / image_path).is_file():
            errors.append(f"verified-local image file is missing: {image_path}")
        elif (ROOT / image_path).stat().st_size == 0:
            errors.append(f"verified-local image file is empty: {image_path}")
        expected_botanical = str(canonical_by_id.get(str(row.get("plant_id")), {}).get("botanical_name", "")).strip()
        if str(row.get("verified_botanical_name", "")).strip() != expected_botanical:
            errors.append(f"verified-local botanical name mismatch: {row.get('plant_id')}/{row.get('part')}")

report = load(REPORT)
if isinstance(report, dict) and isinstance(manifest, dict):
    summary = report.get("summary") or {}
    rows = manifest.get("records") or []
    counts = {}
    for row in rows:
        status = str(row.get("verification_status", ""))
        counts[status] = counts.get(status, 0) + 1
    # Support the current flat audit-report schema and the earlier nested summary schema.
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else report
    if summary.get("plants_checked") != 97:
        errors.append("Image audit report plants_checked is not 97")
    if summary.get("slots_checked") != 873:
        errors.append("Image audit report slots_checked is not 873")
    report_counts = summary.get("status_counts") or {}
    if report_counts != counts:
        errors.append(f"Image audit report status counts {report_counts} do not match manifest {counts}")

required = [
    "plant-index.json", "sw.js", "firebase.json", "firestore.rules",
    ".github/workflows/deploy.yml", ".github/workflows/firebase-deploy.yml",
]
for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f"Missing deployment-critical file: {rel}")

if errors:
    print("PRE-DEPLOY VALIDATION FAILED")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

print("PRE-DEPLOY VALIDATION PASSED: 97 canonical records, 873 image slots, synchronized audit report, and deployment-critical files verified.")
