import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Canonical names from the NCISM 97-plant master index.
NAME_FIXES = {
    'Sarapagandha': 'Sarpagandha',
}

plants = json.loads(DATA.read_text(encoding='utf-8'))
changed = 0
for plant in plants:
    identity = plant.get('identity')
    if not isinstance(identity, dict):
        continue
    name = identity.get('name')
    if name in NAME_FIXES:
        identity['name'] = NAME_FIXES[name]
        changed += 1

if changed:
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Normalized {changed} NCISM canonical plant names')
