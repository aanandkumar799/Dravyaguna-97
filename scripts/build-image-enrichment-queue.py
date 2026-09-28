#!/usr/bin/env python3
"""Build a deterministic, species-specific queue for unresolved plant images.

This tool never invents an image URL or marks an image as verified. It creates
search metadata for human/automated enrichment from approved sources only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "curated-image-manifest.json"
OUT = ROOT / "data" / "image-enrichment-queue.json"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
records = manifest.get("records", [])
approved = {"Wikimedia Commons", "iNaturalist"}
queue = []

for row in records:
    if not isinstance(row, dict):
        continue
    status = str(row.get("verification_status", "")).strip()
    if status not in {"missing-queued", "download-failed"}:
        continue

    plant = str(row.get("plant_name", "")).strip()
    botanical = str(row.get("botanical_name", "")).strip()
    part = str(row.get("part", "")).strip()
    if not plant or not botanical or not part:
        continue

    queue.append({
        "plant_id": str(row.get("plant_id", "")).strip(),
        "ncism_order": row.get("ncism_order"),
        "plant_name": plant,
        "botanical_name": botanical,
        "part": part,
        "current_status": status,
        "search_queries": [
            f'"{botanical}" "{part}"',
            f'"{botanical}" "{part}" site:commons.wikimedia.org',
            f'"{botanical}" "{part}" site:inaturalist.org',
        ],
        "approved_sources": sorted(approved),
        "acceptance_rules": [
            "exact botanical species match",
            "requested plant part is actually visible",
            "source license is documented",
            "not a duplicate of another selected image",
            "downloaded into the canonical local asset path before verified-local",
        ],
        "target_path": f"images/plants/{row.get('plant_id','')}/{part}/image.jpg",
    })

queue.sort(key=lambda x: (int(x["ncism_order"] or 9999), x["plant_id"], x["part"]))
payload = {
    "generated_from": "data/curated-image-manifest.json",
    "manifest_version": manifest.get("version"),
    "purpose": "Safe enrichment queue for unresolved botanical images",
    "approved_sources": sorted(approved),
    "total_unresolved_slots": len(queue),
    "items": queue,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"IMAGE ENRICHMENT QUEUE: {len(queue)} unresolved slots queued")
