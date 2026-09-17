#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'plant-index.json'
MANIFEST = ROOT / 'data' / 'curated-image-manifest.json'
PARTS = ['whole_plant','habit','root','stem','leaf','flower','fruit','seed','bark']

index = json.loads(INDEX.read_text(encoding='utf-8'))
manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
ncism = {int(p['order']): p for p in index.get('plants', []) if p.get('category') == 'NCISM-97' and 1 <= int(p.get('order', 0)) <= 97}
records = manifest.get('records', [])
errors, warnings = [], []

if len(ncism) != 97:
    errors.append(f'Expected 97 NCISM records in plant-index.json, found {len(ncism)}')

seen = set()
for r in records:
    key = (str(r.get('plant_id','')).lower(), int(r.get('ncism_order', 0) or 0), r.get('part'))
    if key in seen:
        errors.append(f'Duplicate manifest record: {key}')
    seen.add(key)
    order = int(r.get('ncism_order', 0) or 0)
    plant = ncism.get(order)
    if not plant:
        errors.append(f'Manifest record points to non-NCISM order: {key}')
        continue
    if r.get('plant_id') != plant.get('id'):
        errors.append(f'Order {order}: manifest id {r.get("plant_id")} != index id {plant.get("id")}')
    if r.get('part') not in PARTS:
        errors.append(f'Invalid part at order {order}: {r.get("part")}')
    status = str(r.get('verification_status') or '')
    image_path = str(r.get('image_path') or '')
    if status == 'verified-local':
        asset = ROOT / image_path
        if not image_path.startswith('images/plants/') or not asset.exists() or asset.stat().st_size < 2048:
            errors.append(f'Missing/invalid local image asset: {key} -> {image_path}')
    elif status in ('verified','verified-external'):
        if not image_path.startswith('http') or not r.get('source_url') or not r.get('verified_botanical_name'):
            errors.append(f'Invalid external verified record: {key}')
        warnings.append(f'Awaiting local materialization: {key}')
    elif status not in ('missing-queued','duplicate-rejected','download-failed'):
        warnings.append(f'Unmaterialized registry status: {status} ({key})')

registered = {(str(r.get('plant_id')), str(r.get('part'))) for r in records}
for order, plant in ncism.items():
    for part in PARTS:
        key = (str(plant.get('id')), part)
        if key not in registered:
            errors.append(f'Missing registry entry: {key}')

print(f'NCISM plants: {len(ncism)}')
print(f'Manifest records: {len(records)}')
print(f'Warnings: {len(warnings)}')
print(f'Errors: {len(errors)}')
for w in warnings[:50]: print('WARNING:', w)
for e in errors: print('ERROR:', e)
raise SystemExit(1 if errors else 0)
