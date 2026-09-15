#!/usr/bin/env python3
"""Fast, dependency-free checks for the DravyaGuna 97 static site."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
errors = []

required_files = ["index.html", "plant.html", "plants.json", "script.js", "style.css"]
for name in required_files:
    if not (ROOT / name).is_file():
        errors.append(f"missing required file: {name}")

try:
    raw_data = json.loads((ROOT / "plants.json").read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"plants.json could not be parsed: {exc}")
    raw_data = None

if isinstance(raw_data, list):
    plants = raw_data
elif isinstance(raw_data, dict) and raw_data.get("id"):
    plants = [raw_data]
else:
    plants = []
    errors.append("plants.json must contain a plant record object or an array of plant records")

if not plants:
    errors.append("plants.json must contain at least one plant record")

for index, plant in enumerate(plants):
    if not isinstance(plant, dict) or not plant.get("id"):
        errors.append(f"plants.json record {index + 1} has no id")
        continue

    images = plant.get("images", {})
    if isinstance(images, dict):
        for field, value in images.items():
            if value:
                image_path = ROOT / value
                if not image_path.is_file():
                    errors.append(f"{plant['id']} image {field} is missing: {value}")

index_html = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").is_file() else ""
for required in ('id="plant-list"', 'id="search"', 'script.js'):
    if required not in index_html:
        errors.append(f"index.html is missing homepage hook: {required}")

if not re.search(r'<link[^>]+rel="icon"[^>]+href="[^"]+"', index_html, re.IGNORECASE | re.DOTALL):
    errors.append("index.html has no favicon link")

if errors:
    print("SITE CHECK FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"SITE CHECK PASSED: {len(plants)} plant record(s), homepage hooks, and referenced images verified")
