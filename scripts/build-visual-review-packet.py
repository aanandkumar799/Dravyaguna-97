#!/usr/bin/env python3
"""Build a conservative visual-review packet for curated plant images."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"data/curated-image-manifest.json").read_text(encoding="utf-8"))
plants={p.get("id"):p for p in (json.loads(x.read_text(encoding="utf-8")) for x in (ROOT/"data/plants").glob("*.json")) if p.get("id")}
rows=[r for r in manifest["records"] if r.get("verification_status")=="verified-local" and r.get("image_path")]
out=ROOT/"visual-review"
out.mkdir(exist_ok=True)
thumb_dir=out/"thumbs"; thumb_dir.mkdir(exist_ok=True)
font=ImageFont.load_default()

review=[]
for r in rows:
    path=ROOT/r["image_path"]
    rec=plants.get(r["plant_id"],{})
    botanical=rec.get("identity",{}).get("botanical_name","")
    review.append({"plant_id":r["plant_id"],"plant_name":rec.get("identity",{}).get("name",r["plant_id"]),
                   "botanical_name":botanical,"part":r["part"],"image_path":r["image_path"],
                   "semantic_verification":"REVIEW_REQUIRED"})
    try:
        im=Image.open(path).convert("RGB")
        im.thumbnail((320,240))
        canvas=Image.new("RGB",(340,285),"white")
        canvas.paste(im,((340-im.width)//2,5))
        d=ImageDraw.Draw(canvas)
        d.text((8,250),f'{r["plant_id"]} / {r["part"]}',fill="black",font=font)
        d.text((8,265),botanical[:48],fill="black",font=font)
        safe=f'{r["plant_id"]}__{r["part"]}.jpg'
        canvas.save(thumb_dir/safe,quality=88)
    except Exception as e:
        review[-1]["render_error"]=str(e)

(review_path:=out/"review-manifest.json").write_text(json.dumps(
    {"generated_from":"data/curated-image-manifest.json","semantic_verification":"not_claimed",
     "review_required_count":len(review),"records":review},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

with (out/"review-manifest.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["plant_id","plant_name","botanical_name","part","image_path","semantic_verification"])
    w.writeheader(); w.writerows(review)

cols=4; cellw,cellh=340,285; rows_per=math.ceil(len(review)/cols)
sheet=Image.new("RGB",(cols*cellw,rows_per*cellh),"white")
for i,r in enumerate(review):
    p=thumb_dir/f'{r["plant_id"]}__{r["part"]}.jpg'
    if p.exists(): sheet.paste(Image.open(p),(i%cols*cellw,i//cols*cellh))
sheet.save(out/"contact-sheet.jpg",quality=90)
print(f"Created visual review packet for {len(review)} verified-local images.")
