import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# High-confidence Rasa-Panchaka corrections for records that were structurally
# incomplete in the automated audit. These values are applied after enrichment
# so third-party imports cannot leave required fields blank.
PATCHES = {
    'Kutaja': {
        'botanical_name': 'Holarrhena pubescens Wall. ex G.Don',
        'family': 'Apocynaceae',
        'useful_part': ['stem bark', 'seed (Indrayava)'],
        'rasa': ['tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'],
        'virya': 'sheeta', 'vipaka': 'katu',
    },
    'Ajamoda': {
        # NCISM/Dravyaguna usage may identify Ajamoda with Apium leptophyllum;
        # keep the repository's existing botanical identity and correct only the
        # pharmacodynamic fields here.
        'rasa': ['katu', 'tikta'], 'guna': ['laghu', 'ruksha', 'tikshna'],
        'virya': 'ushna', 'vipaka': 'katu',
    },
    'Madanphala': {
        'botanical_name': 'Randia dumetorum (Retz.) Lam.',
        'family': 'Rubiaceae',
        'useful_part': ['fruit', 'seed'],
        'rasa': ['madhura', 'tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'],
        'virya': 'ushna', 'vipaka': 'katu',
    },
    'Meshashrungi': {
        'botanical_name': 'Gymnema sylvestre (Retz.) R.Br. ex Sm.',
        'family': 'Apocynaceae',
        'useful_part': ['leaf', 'root'],
        'rasa': ['tikta', 'kashaya'], 'guna': ['laghu', 'ruksha'],
        'virya': 'ushna', 'vipaka': 'katu',
    },
    'Shalmali (Mocharasa)': {
        'botanical_name': 'Bombax ceiba L.',
        'family': 'Malvaceae',
        'useful_part': ['gum (Mocharasa)', 'bark', 'flower', 'root'],
        'rasa': ['madhura', 'kashaya'], 'guna': ['guru', 'snigdha', 'picchila'],
        'virya': 'sheeta', 'vipaka': 'madhura',
    },
    'Tulasi': {
        'botanical_name': 'Ocimum tenuiflorum L.',
        'family': 'Lamiaceae',
        'useful_part': ['leaf', 'whole plant'],
        'rasa': ['katu', 'tikta'], 'guna': ['laghu', 'ruksha'],
        'virya': 'ushna', 'vipaka': 'katu',
    },
}

plants = json.loads(DATA.read_text(encoding='utf-8'))
updated = []
for p in plants:
    name = p.get('identity', {}).get('name', '')
    patch = PATCHES.get(name)
    if not patch:
        continue
    identity = p.setdefault('identity', {})
    dg = p.setdefault('dravya_guna', {})
    therapy = p.setdefault('therapeutics', {})
    for key in ('botanical_name', 'family'):
        if patch.get(key):
            identity[key] = patch[key]
    if patch.get('useful_part'):
        therapy['useful_part'] = patch['useful_part']
    for key in ('rasa', 'guna', 'virya', 'vipaka'):
        dg[key] = patch[key]
    p.setdefault('metadata', {})['panchaka_correction'] = '2026-09-16 audit correction; source-reviewed classical profile'
    updated.append(name)

DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Applied missing Rasa-Panchaka corrections:', ', '.join(updated))
assert len(updated) == len(PATCHES), f'Expected {len(PATCHES)} corrections, applied {len(updated)}'
