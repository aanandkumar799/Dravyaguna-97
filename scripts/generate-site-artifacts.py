#!/usr/bin/env python3
"""Generate canonical navigation and compatibility artifacts from modular NCISM-97 data."""
import json
import re
from pathlib import Path
from html import escape as html_escape
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "plants"
BASE = "https://aanandkumar799.github.io/Dravyaguna-97/"

records=[]
for path in sorted(DB.glob("*.json")):
    if path.name in {"index.json","schema.json"}: continue
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
(ROOT/"plants.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def as_list(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if value is None or value == "":
        return []
    return [str(value).strip()]

def flat(value):
    if isinstance(value, list):
        return ", ".join(flat(x) for x in value if x is not None and str(x).strip())
    if isinstance(value, dict):
        return ", ".join(f"{k}: {flat(v)}" for k, v in value.items() if v is not None and str(v).strip())
    return str(value or "").strip()

def esc(value):
    return html_escape(flat(value), quote=True)

def source_items(plant):
    sources = plant.get("sources") or []
    if not isinstance(sources, list):
        return []
    out = []
    for s in sources:
        if isinstance(s, dict):
            title = s.get("title") or s.get("type") or "Source"
            url = s.get("url") or ""
            out.append((str(title), str(url)))
        elif str(s).strip():
            out.append((str(s), ""))
    return out

def static_plant_html(plant):
    identity = plant.get("identity") or {}
    classification = plant.get("classification") or {}
    identification = plant.get("identification") or {}
    guna = plant.get("dravya_guna") or plant.get("dravyaguna") or {}
    therapeutics = plant.get("therapeutics") or {}
    classical = plant.get("classical_reference") or {}
    metadata = plant.get("metadata") or {}
    student = plant.get("student") or {}
    pid = str(plant.get("id") or "").strip()
    name = str(identity.get("name") or plant.get("name") or pid)
    botanical = str(identity.get("botanical_name") or "")
    family = str(identity.get("family") or "")
    sanskrit = str(identity.get("sanskrit_name") or "")
    english = str(identity.get("english_name") or "")
    description = str(identification.get("description") or "")
    quick = student.get("quick_revision") or student.get("exam_points") or ""
    last_updated = metadata.get("last_verified") or metadata.get("last_enrichment") or metadata.get("updated_at") or ""
    sources = source_items(plant)
    source_html = "".join(
        f'<li>{esc(title)}' + (f' — <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">source</a>' if url else "") + "</li>"
        for title, url in sources
    )
    canonical = BASE + "plants/" + quote(pid, safe="") + "/"
    image = BASE + "images/icon-512.png"
    title = f"{name} | DravyaGuna 97"
    meta_desc = f"BAMS Dravyaguna reference for {name}" + (f" ({botanical})" if botanical else "") + ". Identification, Rasa Panchaka, therapeutic information, classical references and exam revision."
    rows = [
        ("Sanskrit name", sanskrit), ("Botanical name", botanical), ("Family", family),
        ("English name", english), ("Habit", classification.get("habit")),
        ("Description", description), ("Rasa", guna.get("rasa")), ("Guna", guna.get("guna")),
        ("Virya", guna.get("virya")), ("Vipaka", guna.get("vipaka")),
        ("Useful part", therapeutics.get("useful_part")), ("Indications", therapeutics.get("indications")),
        ("Dose", therapeutics.get("dose")), ("Quick revision", quick),
        ("Shloka / classical text", classical.get("shlokas") or classical.get("text")),
        ("Nighantu references", classical.get("nighantu_references")),
        ("Samhita references", classical.get("samhita_references")),
    ]
    row_html = "".join(
        f'<div class="row"><dt>{esc(label)}</dt><dd>{esc(value) if str(flat(value)).strip() else "<span class=\"muted\">Not available in verified record</span>"}</dd></div>'
        for label, value in rows
    )
    status = metadata.get("status") or metadata.get("verification_status") or "recorded in the database"
    updated_html = f"<p><strong>Last verified/updated:</strong> {esc(last_updated)}</p>" if last_updated else "<p><strong>Last verified/updated:</strong> Not recorded for this entry.</p>"
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta_desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta_desc)}">
<meta name="twitter:image" content="{esc(image)}">
<link rel="icon" href="{esc(BASE)}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{esc(BASE)}site-theme.css?v=15">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":meta_desc,"url":canonical,"inLanguage":"en-IN","isPartOf":{"@type":"WebSite","name":"DravyaGuna 97","url":BASE},"about":{"@type":"Thing","name":name, **({"alternateName":botanical} if botanical else {})},"educationalUse":["study","revision","practical identification"]}, ensure_ascii=False)}</script>
<style>
body{{margin:0;background:#f8f5ed;color:#24302a;font:16px/1.6 Arial,sans-serif}}
.wrap{{max-width:1050px;margin:auto;padding:22px 18px 60px}}
header{{background:#fff;border-bottom:1px solid #dfe8df}}
.head{{max-width:1050px;margin:auto;padding:13px 18px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}}
.brand{{font-weight:800;color:#1b4332;text-decoration:none}}nav{{display:flex;gap:6px;flex-wrap:wrap}}nav a{{padding:7px 9px;border-radius:8px;color:#24302a;text-decoration:none;font-weight:700}}nav a:hover{{background:#edf5ef;color:#1b4332}}
.crumb{{font-size:.86rem;color:#66736b;margin-bottom:14px}}.crumb a{{color:#2d6a4f;font-weight:700}}
.hero,.card{{background:#fff;border:1px solid #dfe8df;border-radius:18px;padding:22px;box-shadow:0 7px 22px rgba(27,67,50,.06);margin-bottom:18px}}
.hero h1{{margin:0 0 6px;color:#1b4332;font-family:Georgia,serif;font-size:clamp(2rem,5vw,3rem)}}.botanical{{font-style:italic;color:#5e7469}}.badge{{display:inline-block;margin-top:10px;padding:5px 9px;border-radius:999px;background:#edf5ef;color:#1b4332;font-weight:800;font-size:.78rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px}}.card h2{{color:#1b4332;margin-top:0}}.row{{display:grid;grid-template-columns:145px 1fr;gap:12px;padding:9px 0;border-top:1px solid #edf1ee}}.row:first-child{{border-top:0}}dt{{font-weight:800;color:#365f50}}dd{{margin:0;overflow-wrap:anywhere}}.muted{{color:#8a958f;font-style:italic}}
.notice{{background:#fff8e9;border-left:4px solid #d4a373;padding:13px 15px;border-radius:8px;color:#594a2e}}footer{{margin-top:25px;padding:22px;text-align:center;background:#1b4332;color:#eaf2ec}}footer a{{color:#fff}}.actions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}.btn{{display:inline-block;padding:9px 12px;border-radius:9px;background:#1b4332;color:#fff;text-decoration:none;font-weight:800}}@media(max-width:620px){{.head{{align-items:flex-start;flex-direction:column}}.row{{grid-template-columns:1fr;gap:3px}}}}
</style></head><body>
<header><div class="head"><a class="brand" href="{esc(BASE)}">🌿 DravyaGuna 97</a>
<nav aria-label="Primary"><a href="{esc(BASE)}">Home</a><a href="{esc(BASE)}plants.html">Plant Library</a><a href="{esc(BASE)}practical-lab.html">Practical Lab</a><a href="{esc(BASE)}reference-library.html">References</a><a href="{esc(BASE)}supplementary.html">Supplementary</a><a href="{esc(BASE)}quiz.html">Quiz</a></nav></div></header>
<main class="wrap"><div class="crumb"><a href="{esc(BASE)}plants.html">Plant Library</a> › {esc(name)}</div>
<section class="hero"><h1>{esc(name)}</h1><div class="botanical">{esc(botanical or "Botanical name not available")}</div><span class="badge">NCISM 97 · No. {esc(plant.get("order") or "—")} · {esc(status)}</span>
<p>{esc(description or f"{name} is part of the canonical NCISM-97 DravyaGuna plant library.")}</p>{updated_html}</section>
<section class="card"><h2>Verified study data</h2><dl>{row_html}</dl></section>
<div class="grid"><section class="card"><h2>Academic trust & review</h2><p>This page is a static, crawlable rendering of the DravyaGuna 97 database record. It does not invent missing fields.</p><p>Reviewer attribution is shown only when a named reviewer is actually recorded in the project data. See the <a href="{esc(BASE)}sources-review.html">Sources & Review</a> page for the verification framework and source policy.</p></section>
<section class="card"><h2>Continue to full dossier</h2><p>The interactive dossier contains the full image gallery, detailed textbook notes, MCQs and revision tools.</p><div class="actions"><a class="btn" href="{esc(BASE)}plant.html?id={quote(pid,safe='')}">Open full dossier</a><a class="btn" href="{esc(BASE)}plants.html">Back to Plant Library</a></div></section></div>
{"}
</main><div class="notice wrap"><strong>Educational reference only.</strong> This site is for BAMS study and revision. Do not use its dosing, therapeutic or identification information as a substitute for qualified clinical assessment, prescribing, dispensing, or professional supervision. Cross-check authoritative Ayurvedic texts, pharmacopoeial standards and current professional guidance before clinical use.</div>
<footer>DravyaGuna 97 • <a href="{esc(BASE)}sources-review.html">Sources & Review</a> • <a href="{esc(BASE)}feedback.html">Share your feedback</a></footer>
</body></html>"""

plant_static_dir = ROOT / "plants"
for plant in canonical:
    pid = str(plant.get("id") or "").strip()
    out = plant_static_dir / pid / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(static_plant_html(plant), encoding="utf-8")

urls=[BASE,BASE+"plants.html",BASE+"compare.html",BASE+"quiz.html",BASE+"viva.html",BASE+"progress.html",BASE+"rasa.html",BASE+"reference-library.html",BASE+"practical-lab.html",BASE+"references.html",BASE+"supplementary.html",BASE+"sources-review.html"]+[BASE+"plants/"+quote(pid,safe="")+"/" for pid in ids]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"  <url><loc>{escape(u)}</loc></url>\n" for u in urls)+'</urlset>\n'
(ROOT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")

fixes = {
    "plants.html": [(r'<div class="filter-row" aria-label="Dravyaguna filters">', '<div class="filter-row">')],
    "progress.html": [(r'<div class="progress-track" aria-label="Study progress">', '<div class="progress-track" role="progressbar" aria-label="Study progress" aria-valuemin="0" aria-valuemax="97" aria-valuenow="0">')],
    "plant.html": [
        (r'index\.html#student', 'progress.html'),
        (r'index\.html#teacher', 'reference-library.html'),
        (r'index\.html#doctor', 'references.html'),
        (r'r\.verification_status===\'verified-external\'', "['verified','verified-external','verified-local'].includes(r.verification_status)"),
        # HTML-Proofer rejects the inline SVG data URI used by the modal placeholder.
        # Keep the placeholder as a normal repository asset instead.
        (r'src="data:image/svg\+xml[^\"]*"', 'src="favicon.svg"'),
    ],
}
for filename, replacements in fixes.items():
    path = ROOT / filename
    if not path.exists(): continue
    html = path.read_text(encoding="utf-8")
    original = html
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, count=1)
    if html != original:
        path.write_text(html, encoding="utf-8")

# Ensure the homepage schema also uses the production GitHub Pages origin.
home_schema = ROOT / "index.html"
if home_schema.exists():
    h = home_schema.read_text(encoding="utf-8")
    h = h.replace("https://dravyaguna-97.web.app/", BASE)
    home_schema.write_text(h, encoding="utf-8")

# Enforce one production origin for SEO metadata on every public HTML page.
# GitHub Pages is the public production origin used by canonical, Open Graph,
# sitemap, and robots metadata.
for page in sorted(ROOT.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    html = html.replace('href="saved.html"', 'href="plants.html#favorites"')
    canonical = BASE if page.name == "index.html" else BASE + page.name
    if page.name == "plant.html":
        canonical = BASE + "plant.html"
    tag = f'<link rel="canonical" href="{canonical}">'
    if re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.I):
        html = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', tag, html, count=1, flags=re.I)
    elif "</head>" in html:
        html = html.replace("</head>", tag + "\n</head>", 1)
    if page.name != "plant.html":
        og = f'<meta property="og:url" content="{canonical}">'
        if re.search(r'<meta[^>]+property=["\']og:url["\'][^>]*>', html, re.I):
            html = re.sub(r'<meta[^>]+property=["\']og:url["\'][^>]*>', og, html, count=1, flags=re.I)
        elif "</head>" in html:
            html = html.replace("</head>", og + "\n</head>", 1)

    # Ensure every indexable page has share metadata in the original HTML,
    # not only after JavaScript executes.
    if page.name != "plant.html":
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
        page_title = re.sub(r'\s+', ' ', title_match.group(1)).strip() if title_match else "DravyaGuna 97"
        page_desc = desc_match.group(1).strip() if desc_match else "BAMS Dravyaguna learning and reference portal."
        meta = [
            f'<meta property="og:type" content="website">',
            f'<meta property="og:title" content="{html_escape(page_title, quote=True)}">',
            f'<meta property="og:description" content="{html_escape(page_desc, quote=True)}">',
            f'<meta property="og:image" content="{BASE}images/icon-512.png">',
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{html_escape(page_title, quote=True)}">',
            f'<meta name="twitter:description" content="{html_escape(page_desc, quote=True)}">',
            f'<meta name="twitter:image" content="{BASE}images/icon-512.png">',
        ]
        for tag in meta:
            marker = tag.split(" ", 2)[1]
            if marker.startswith('property="og:'):
                exists = re.search(r'<meta[^>]+property=["\']'+re.escape(marker.split('="')[1].rstrip('"'))+r'["\'][^>]*>', html, re.I)
            else:
                exists = re.search(r'<meta[^>]+name=["\']'+re.escape(marker.split('="')[1].rstrip('"'))+r'["\'][^>]*>', html, re.I)
            if not exists and "</head>" in html:
                html = html.replace("</head>", tag + "\n</head>", 1)
    if 'src="public-seo.js"' not in html and "</head>" in html:
        html = html.replace("</head>", '<script src="public-seo.js" defer></script>\n</head>', 1)
    page.write_text(html, encoding="utf-8")

# Materialize the theme on every generated HTML page. Versioned URLs prevent
# stale browser/CDN assets from hiding a newly deployed theme.
for page in sorted(ROOT.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    original = html
    if 'href="site-theme.css' not in html and "</head>" in html:
        html = html.replace("</head>", '<link rel="stylesheet" href="site-theme.css?v=4">\n</head>', 1)
    if 'src="site-theme.js' not in html and "</body>" in html:
        html = html.replace("</body>", '<script src="site-theme.js?v=4" defer></script>\n</body>', 1)
    if html != original:
        page.write_text(html, encoding="utf-8")

home=ROOT/"index.html"
if home.exists():
    html=home.read_text(encoding="utf-8")
    marker="</body>"
    if "feedback-config.js" not in html and marker in html:
        html=html.replace(marker,"\n<script src=\"feedback-config.js\"></script>\n<script src=\"feedback.js\"></script>\n"+marker,1)
        home.write_text(html,encoding="utf-8")

print(f"Generated index + compatibility file for {len(index)} NCISM plants and {len(urls)} sitemap URLs")
