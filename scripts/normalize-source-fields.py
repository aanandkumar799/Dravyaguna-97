import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'
with DATA.open('r', encoding='utf-8') as f:
    plants = json.load(f)

changed = 0
for plant in plants:
    sources = plant.get('sources', [])
    if not isinstance(sources, list):
        plant['sources'] = []
        changed += 1
        continue
    for source in sources:
        if not isinstance(source, dict):
            continue
        for field in ('type', 'title', 'url', 'author', 'edition', 'year', 'page', 'note', 'license_note'):
            if field in source and not isinstance(source[field], str):
                source[field] = '' if source[field] is None else str(source[field])
                changed += 1

with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'Normalized source metadata fields; converted {changed} non-string values.')
