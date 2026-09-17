#!/usr/bin/env python3
"""DravyaGuna 97 website and modular database integrity checker."""
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parent
DB=ROOT/'data'/'plants'
INDEX=ROOT/'plant-index.json'
errors=[]

def fail(msg): errors.append(msg)

required=['index.html','plants.html','plant.html','compare.html','quiz.html','practical-lab.html','references.html','404.html','plant-index.json','script.js','style.css','manifest.json','sw.js','favicon.svg']
for f in required:
    if not (ROOT/f).is_file(): fail(f'Missing required file: {f}')

records=[]
for path in sorted(DB.glob('*.json')):
    if path.name in {'index.json','schema.json'}: continue
    try: data=json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: fail(f'{path}: invalid JSON: {exc}'); continue
    if not isinstance(data,dict): fail(f'{path}: root must be an object'); continue
    records.append(data)

core=[p for p in records if p.get('category')=='NCISM-97' and 1<=int(p.get('order',0) or 0)<=97]
if len(core)!=97: fail(f'Expected exactly 97 NCISM records, found {len(core)}')
ids=[str(p.get('id','')) for p in core]
if len(ids)!=len(set(ids)): fail('Duplicate NCISM plant IDs detected')
orders=sorted(int(p.get('order',0)) for p in core)
if orders!=list(range(1,98)): fail('NCISM orders must contain every number 1–97 exactly once')
for p in core:
    for field in ['identity','classification','identification','dravya_guna','therapeutics','classical_reference','student','metadata']:
        if field not in p: fail(f'{p.get("id")}: missing {field}')

try: idx=json.loads(INDEX.read_text(encoding='utf-8'))
except Exception as exc: idx={}; fail(f'plant-index.json invalid: {exc}')
rows=idx if isinstance(idx,list) else idx.get('plants',[])
indexed=[p for p in rows if p.get('category')=='NCISM-97' and 1<=int(p.get('order',0) or 0)<=97]
if len(indexed)!=97: fail(f'plant-index.json contains {len(indexed)} NCISM records; expected 97')
if {p.get('id') for p in indexed}!={p.get('id') for p in core}: fail('plant-index/detail ID mismatch')

manifest_path=ROOT/'data'/'curated-image-manifest.json'
if manifest_path.is_file():
    try: manifest=json.loads(manifest_path.read_text(encoding='utf-8')); rows=manifest.get('records',[])
    except Exception as exc: fail(f'curated image manifest invalid: {exc}'); rows=[]
    seen=set()
    for r in rows:
        key=(str(r.get('plant_id')),str(r.get('part')))
        if key in seen: fail(f'Duplicate image manifest slot: {key}')
        seen.add(key)
else: fail('Missing curated image manifest')

# Detect the known class of irrelevant duplicated cover assets without requiring image decoding.
# A single Git blob should not back multiple different NCISM cover filenames.
plant_image_dir=ROOT/'images'/'plants'
if plant_image_dir.is_dir():
    hashes={}
    for p in plant_image_dir.iterdir():
        if p.is_file(): hashes.setdefault(p.read_bytes().__hash__(),[]).append(p.name)
    for names in hashes.values():
        if len(names)>1: fail('Duplicate image content detected among: '+', '.join(sorted(names)))

for page in ROOT.rglob('*.html'):
    text=page.read_text(encoding='utf-8',errors='ignore')
    if 'images/favicon.png' in text or 'images/favicon.svg' in text: fail(f'{page}: stale favicon reference')

if errors:
    print('WEBSITE DOCTOR FAILED')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f'WEBSITE DOCTOR PASSED: {len(core)} NCISM records, {len(records)} modular records')
