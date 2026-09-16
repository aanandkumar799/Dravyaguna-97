#!/usr/bin/env python3
"""Validate public-readiness requirements and generate an accurate sitemap/robots file."""
from pathlib import Path
import json
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "plant-index.json"
PLANTS = ROOT / "plants.json"
BASE = "https://aanandkumar799.github.io/Dravyaguna-97/"
REQUIRED = ["identity", "classification", "identification", "dravya_guna", "therapeutics", "classical_reference", "student", "metadata"]


def load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main():
    errors = []
    if not INDEX.exists() or not PLANTS.exists():
        print("Missing plant-index.json or plants.json", file=sys.stderr)
        return 1
    index = load(INDEX)
    plants = load(PLANTS)
    indexed = [p for p in (index if isinstance(index, list) else index.get("plants", [])) if p.get("category") == "NCISM-97" and 1 <= int(p.get("order", 0)) <= 97]
    if len(indexed) != 97:
        errors.append(f"Canonical NCISM-97 index has {len(indexed)} records; expected 97")
    ids = {p.get("id") for p in indexed}
    detail_ids = {p.get("id") for p in plants if isinstance(p, dict)}
    missing = sorted(ids - detail_ids)
    if missing:
        errors.append("Missing plant detail records: " + ", ".join(missing[:10]))
    status_counts = {}
    for p in plants:
        if not isinstance(p, dict) or p.get("id") not in ids:
            continue
        for field in REQUIRED:
            if field not in p:
                errors.append(f"{p.get('id')}: missing required field {field}")
        status = str(p.get("metadata", {}).get("status", "draft")).strip() or "draft"
        status_counts[status] = status_counts.get(status, 0) + 1
    print("NCISM-97 records:", len(indexed))
    print("Verification status counts:", json.dumps(status_counts, ensure_ascii=False, sort_keys=True))
    # Generate sitemap from the canonical 97 only; this prevents unrelated legacy records from being indexed as part of the syllabus.
    urls = [BASE, BASE + "plants.html", BASE + "compare.html", BASE + "quiz.html"]
    for p in sorted(indexed, key=lambda x: int(x.get("order", 0))):
        urls.append(BASE + "plant.html?id=" + quote(str(p["id"]), safe=""))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc></url>" for u in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
    if errors:
        print("PUBLIC READINESS FAILED", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        return 1
    print(f"PUBLIC READINESS PASSED: {len(urls)} sitemap URLs generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
