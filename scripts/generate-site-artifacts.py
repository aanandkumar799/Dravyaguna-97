#!/usr/bin/env python3
"""Generate canonical navigation and compatibility artifacts from modular NCISM-97 data."""
import json
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "plants"
BASE = "https://aanandkumar799.github.io/Dravyaguna-97/"

records=[]
for path in sorted(DB.glob("*.json")):
    if path.name in {"index.json", "schema.json"}: continue
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict): raise SystemExit(f"{path}: record must be a JSON object")
    records.append(data)

canonical=[p for p in records if p.get("category")=="NCISM-97" and 1 <= int(p.get("order",0)) <= 97]
ids=[str(p.get("id","")).strip() for p in canonical]
if len(canonical)!=97: raise SystemExit(f"Expected exactly 97 NCISM-97 plant files, found {len(canonical)}")
if len(ids)!=len(set(ids)): raise SystemExit("Duplicate NCISM plant IDs detected")
canonical=sorted(canonical,key=lambda p:(int(p.get("order",9999)),str(p.get("id",""))))

index=[]
for plant in canonical:
    pid=str(plant["id"]).strip(); identity=plant.get("identity") or {}; guna=plant.get("dravya_guna") or plant.get("dravyaguna") or {}; therapeutic=plant.get("therapeutics") or {}
    index.append({"id":pid,"order":plant.get("order"),"category":"NCISM-97","name":identity.get("name") or plant.get("name") or pid,"sanskrit_name":identity.get("sanskrit_name",""),"transliteration":identity.get("transliteration",""),"botanical_name":identity.get("botanical_name",""),"family":identity.get("family",""),"english_name":identity.get("english_name",""),"rasa":guna.get("rasa",[]),"guna":guna.get("guna",[]),"virya":guna.get("virya",""),"vipaka":guna.get("vipaka",""),"useful_part":therapeutic.get("useful_part",[]),"search_text":" ".join(str(x) for x in [identity.get("name",""),identity.get("sanskrit_name",""),identity.get("transliteration",""),identity.get("botanical_name",""),identity.get("family",""),identity.get("english_name",""),identity.get("hindi_name",""),pid])})

payload={"total":97,"plants":index}
(ROOT/"plant-index.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
# Backward-compatible legacy endpoint. New code should use plant-index.json + data/plants/{id}.json.
(ROOT/"plants.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

urls=[BASE,BASE+"plants.html",BASE+"compare.html",BASE+"quiz.html",BASE+"practical-lab.html",BASE+"references.html"]+[BASE+"plant.html?id="+quote(pid,safe="") for pid in ids]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"  <url><loc>{escape(u)}</loc></url>\n" for u in urls)+"</urlset>\n"
(ROOT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")
print(f"Generated index + compatibility file for {len(index)} NCISM plants and {len(urls)} sitemap URLs")
