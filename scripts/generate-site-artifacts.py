#!/usr/bin/env python3
"""Generate deployment indexes without removing any plant records."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
plants_path = ROOT / "plants.json"
plants = json.loads(plants_path.read_text(encoding="utf-8"))
if not isinstance(plants, list):
    raise SystemExit("plants.json must contain an array")

ids = [str(p.get("id", "")).strip() for p in plants if isinstance(p, dict)]
if len(ids) != len(set(ids)):
    raise SystemExit("plants.json contains duplicate IDs")
if len(ids) < 97:
    raise SystemExit(f"Expected at least 97 records, found {len(ids)}")

index = []
for plant in plants:
    pid = str(plant.get("id", "")).strip()
    if not pid:
        continue
    identity = plant.get("identity") or {}
    guna = plant.get("dravya_guna") or plant.get("dravyaguna") or {}
    therapeutic = plant.get("therapeutics") or {}
    category = plant.get("category", "NCISM-97")
    index.append({
        "id": pid,
        "order": plant.get("order", 9999),
        "category": category,
        "name": identity.get("name") or plant.get("name") or pid,
        "sanskrit_name": identity.get("sanskrit_name", ""),
        "transliteration": identity.get("transliteration", ""),
        "botanical_name": identity.get("botanical_name", ""),
        "family": identity.get("family", ""),
        "english_name": identity.get("english_name", ""),
        "rasa": guna.get("rasa", []),
        "guna": guna.get("guna", []),
        "virya": guna.get("virya", ""),
        "vipaka": guna.get("vipaka", ""),
        "useful_part": therapeutic.get("useful_part", []),
        "search_text": " ".join(str(x) for x in [
            identity.get("name", ""), identity.get("sanskrit_name", ""),
            identity.get("transliteration", ""), identity.get("botanical_name", ""),
            identity.get("family", ""), identity.get("english_name", ""),
            identity.get("hindi_name", ""), pid
        ]),
    })
index.sort(key=lambda item: (float(item["order"]) if isinstance(item["order"], (int, float)) else 9999, item["name"].lower()))
(ROOT / "plant-index.json").write_text(
    json.dumps({"total": len(index), "plants": index}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

base = "https://aanandkumar799.github.io/Dravyaguna-97/"
urls = [base, base + "index.html", base + "plants.html", base + "plant.html"]
urls += [base + "plant.html?id=" + pid for pid in ids]
urls.append(base + "plants/ashwagandha.html")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "".join(f"  <url><loc>{escape(url)}</loc></url>\n" for url in urls)
sitemap += "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print(f"Generated {len(index)} index records and {len(urls)} sitemap URLs")
