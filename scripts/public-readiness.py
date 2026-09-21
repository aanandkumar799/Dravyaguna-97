#!/usr/bin/env python3
"""Validate the modular NCISM-97 database and generate sitemap/robots."""
from pathlib import Path
import json, sys
from urllib.parse import quote

ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/"data"/"plants"
INDEX=ROOT/"plant-index.json"
BASE="https://dravyaguna-97.web.app/"
REQUIRED=["identity","classification","identification","dravya_guna","therapeutics","classical_reference","student","metadata"]
PUBLIC_PAGES=["index.html","plants.html","plant.html","compare.html","quiz.html","viva.html","progress.html","rasa.html","reference-library.html","practical-lab.html","references.html","404.html"]

records=[]
for path in sorted(DB.glob("*.json")):
    if path.name in {"index.json","schema.json"}: continue
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit(f"{path}: invalid JSON: {e}")
    if not isinstance(data,dict): raise SystemExit(f"{path}: record must be a JSON object")
    records.append(data)

indexed=[p for p in records if p.get("category")=="NCISM-97" and 1<=int(p.get("order",0))<=97]
errors=[]
if len(indexed)!=97: errors.append(f"Expected exactly 97 NCISM-97 files; found {len(indexed)}")
ids=[p.get("id") for p in indexed]
if len(ids)!=len(set(ids)): errors.append("Duplicate NCISM plant IDs detected")
orders=[int(p.get("order",0)) for p in indexed]
if sorted(orders)!=list(range(1,98)): errors.append("NCISM order must contain every number 1-97 exactly once")
for p in indexed:
    missing=[f for f in REQUIRED if f not in p]
    if missing: errors.append(f"{p.get('id')}: missing required fields: {', '.join(missing)}")

if not INDEX.exists(): errors.append("Missing plant-index.json")
else:
    idx=json.loads(INDEX.read_text(encoding="utf-8"))
    rows=idx if isinstance(idx,list) else idx.get("plants",[])
    core=[p for p in rows if p.get("category")=="NCISM-97" and 1<=int(p.get("order",0))<=97]
    if len(core)!=97: errors.append(f"plant-index.json has {len(core)} canonical entries; expected 97")
    if {p.get("id") for p in core}!={p.get("id") for p in indexed}: errors.append("Index/detail ID mismatch")

for page in PUBLIC_PAGES:
    if not (ROOT/page).is_file(): errors.append(f"Missing public page: {page}")

status_counts={}
for p in indexed:
    status=str((p.get("metadata") or {}).get("status","draft")).strip() or "draft"
    status_counts[status]=status_counts.get(status,0)+1
print("NCISM-97 records:",len(indexed))
print("Verification status counts:",json.dumps(status_counts,ensure_ascii=False,sort_keys=True))
print("Public pages validated:",len(PUBLIC_PAGES))

urls=[BASE]+[BASE+p for p in PUBLIC_PAGES if p not in {"index.html","plant.html","404.html"}]
urls += [BASE+"plant.html?id="+quote(str(p["id"]),safe="") for p in sorted(indexed,key=lambda x:int(x["order"]))]
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"  <url><loc>{u}</loc></url>\n" for u in urls)+'</urlset>\n',encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")

# Prevent plant.html's client-side canonical assignment from reverting to GitHub Pages.
plant=ROOT/"plant.html"
if plant.exists():
    html=plant.read_text(encoding="utf-8")
    old="https://aanandkumar799.github.io/Dravyaguna-97/plant.html?id="
    new=BASE+"plant.html?id="
    if old in html: plant.write_text(html.replace(old,new),encoding="utf-8")

if errors:
    print("PUBLIC READINESS FAILED",file=sys.stderr)
    for e in errors: print(" -",e,file=sys.stderr)
    sys.exit(1)
print(f"PUBLIC READINESS PASSED: {len(urls)} sitemap URLs generated")
