#!/usr/bin/env python3
"""Audit actual curated image files for path, readability, dimensions and duplicate misuse."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data/curated-image-manifest.json"; REPORT=ROOT/"data/visual-image-audit-report.json"
try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required")
m=json.loads(MANIFEST.read_text(encoding="utf-8")); issues=[]; checked=[]; hashes={}
for row in m.get("records",[]):
    if not isinstance(row,dict) or row.get("verification_status")!="verified-local": continue
    pid=str(row.get("plant_id","")).strip(); part=str(row.get("part","")).strip(); rel=str(row.get("image_path","")).strip()
    item={"plant_id":pid,"part":part,"image_path":rel}; prefix=f"images/plants/{pid}/{part}/"
    if not rel.startswith(prefix):
        issues.append({**item,"type":"path-mismatch","detail":f"Expected path under {prefix}"}); continue
    p=ROOT/rel
    if not p.is_file(): issues.append({**item,"type":"missing-file"}); continue
    if p.stat().st_size<2048: issues.append({**item,"type":"suspiciously-small-file","bytes":p.stat().st_size}); continue
    try:
        with Image.open(p) as im:
            w,h,fmt,mode=im.size[0],im.size[1],im.format,im.mode; im.verify()
        with Image.open(p) as im:
            rgb=im.convert("RGB"); rgb.thumbnail((32,32)); digest=hashlib.sha256(rgb.tobytes()).hexdigest()
    except Exception as exc:
        issues.append({**item,"type":"unreadable-image","detail":str(exc)}); continue
    if w<160 or h<160: issues.append({**item,"type":"low-resolution","width":w,"height":h})
    if digest in hashes: issues.append({**item,"type":"duplicate-visual-content","duplicate_of":hashes[digest]})
    else: hashes[digest]=f"{pid}/{part}"
    item.update({"width":w,"height":h,"format":fmt,"mode":mode,"bytes":p.stat().st_size}); checked.append(item)
report={"generated_by":"scripts/visual-image-audit.py","semantic_verification":"not_claimed","purpose":"Actual-file integrity and duplicate/path screening; no geographic capture metadata is collected or required.","verified_local_checked":len(checked),"issue_count":len(issues),"issue_type_counts":{},"issues":issues,"checked":checked}
for x in issues: report["issue_type_counts"][x["type"]]=report["issue_type_counts"].get(x["type"],0)+1
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"verified_local_checked":len(checked),"issue_count":len(issues),"issue_type_counts":report["issue_type_counts"]},indent=2))
