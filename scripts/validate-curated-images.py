#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'plant-index.json'
MANIFEST = ROOT / 'data' / 'curated-image-manifest.json'

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
    if r.get('part') not in manifest.get('parts', []):
        errors.append(f'Invalid part at order {order}: {r.get("part")}')
    for raw in r.get('image_path_candidates', []) or []:
        path = ROOT / raw
        if not path.exists():
            warnings.append(f'Missing candidate asset: {raw} ({r.get("plant_id")}/{r.get("part")})')

registered_orders = {int(r.get('ncism_order',0)) for r in records if r.get('part') == 'whole_plant'}
missing = sorted(set(range(1,98)) - registered_orders)
if missing:
    errors.append('Missing whole_plant registry entries for NCISM orders: ' + ', '.join(map(str, missing)))

print(f'NCISM plants: {len(ncism)}')
print(f'Manifest records: {len(records)}')
print(f'Warnings: {len(warnings)}')
print(f'Errors: {len(errors)}')
for w in warnings[:50]: print('WARNING:', w)
for e in errors: print('ERROR:', e)

raise SystemExit(1 if errors else 0)
