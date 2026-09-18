import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'plants'
files = sorted(DB.glob('*.json'))
records = []
for path in files:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise SystemExit(f'{path}: plant record must be a JSON object')
    records.append(data)

core = sorted((p for p in records if p.get('category') == 'NCISM-97'), key=lambda p: p.get('order', 0))
supplementary = [p for p in records if p.get('category') == 'Supplementary']
errors, warnings = [], []

if len(core) != 97:
    errors.append(f'Expected exactly 97 NCISM-97 records; found {len(core)}')
if len(core) + len(supplementary) != len(records):
    errors.append('Every plant JSON must declare category NCISM-97 or Supplementary')

names = [str(p.get('identity', {}).get('name', '')).strip() for p in core]
ids = [str(p.get('id', '')).strip() for p in core]
orders = [p.get('order') for p in core]
for label, vals in [('name', names), ('id', ids), ('order', orders)]:
    dupes = sorted(k for k, n in Counter(vals).items() if k and n > 1)
    if dupes:
        errors.append(f'Duplicate {label} values: {dupes}')
if sorted(o for o in orders if isinstance(o, int)) != list(range(1, 98)):
    errors.append('NCISM order values must be exactly 1..97')

for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    required = {
        'identity.name': p.get('identity', {}).get('name'),
        'identity.botanical_name': p.get('identity', {}).get('botanical_name'),
        'identity.family': p.get('identity', {}).get('family'),
        'dravya_guna.virya': p.get('dravya_guna', {}).get('virya'),
        'dravya_guna.vipaka': p.get('dravya_guna', {}).get('vipaka'),
    }
    for field, value in required.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{name}: missing {field}')
    for field, value in [
        ('rasa', p.get('dravya_guna', {}).get('rasa')),
        ('guna', p.get('dravya_guna', {}).get('guna')),
        ('useful_part', p.get('therapeutics', {}).get('useful_part')),
    ]:
        if not isinstance(value, list) or not value:
            errors.append(f'{name}: {field} must be a non-empty list')
    cr = p.get('classical_reference', {}) or {}
    shlokas, refs = cr.get('shlokas') or [], cr.get('nighantu_references') or []
    if shlokas and not refs:
        warnings.append(f'{name}: shloka text exists but reference metadata is missing')
    if shlokas and any(not isinstance(s, (str, dict)) for s in shlokas):
        errors.append(f'{name}: invalid classical shloka item')
    for source in p.get('sources', []) or []:
        if not isinstance(source, dict):
            errors.append(f'{name}: source entry is not an object')


# Cross-record revision/content checks.
def norm_text(value):
    return " ".join(str(value or "").casefold().split())

question_seen = {}
for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    mcqs = p.get('mcqs') or []
    if not isinstance(mcqs, list):
        errors.append(f'{name}: mcqs must be a list')
        continue
    for i, q in enumerate(mcqs, 1):
        if not isinstance(q, dict):
            errors.append(f'{name}: MCQ {i} must be an object')
            continue
        question = norm_text(q.get('question'))
        options = q.get('options')
        answer = norm_text(q.get('answer'))
        if not question:
            errors.append(f'{name}: MCQ {i} missing question')
        if not isinstance(options, list) or len(options) < 2:
            errors.append(f'{name}: MCQ {i} must have at least 2 options')
            continue
        option_keys = [norm_text(x) for x in options]
        if any(not x for x in option_keys):
            errors.append(f'{name}: MCQ {i} contains an empty option')
        if len(option_keys) != len(set(option_keys)):
            errors.append(f'{name}: MCQ {i} has duplicate options')
        if answer not in option_keys:
            errors.append(f'{name}: MCQ {i} answer does not match any option')
        if question:
            question_seen.setdefault(question, []).append(f'{name} MCQ {i}')

for question, locations in question_seen.items():
    if len(locations) > 1:
        errors.append(f'Duplicate MCQ question across records: {locations}')

for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    formulations = p.get('formulations') or []
    if not isinstance(formulations, list):
        errors.append(f'{name}: formulations must be a list')
        continue
    seen_formulations = set()
    for i, f in enumerate(formulations, 1):
        if not isinstance(f, dict):
            errors.append(f'{name}: formulation {i} must be an object')
            continue
        key = (norm_text(f.get('name')), norm_text(f.get('dosage_form')), norm_text(f.get('indication')))
        if not key[0]:
            errors.append(f'{name}: formulation {i} missing name')
        if key in seen_formulations:
            errors.append(f'{name}: duplicate formulation entry "{f.get("name", "")}"')
        seen_formulations.add(key)

for path, p in zip(files, records):
    if path.stem != str(p.get('id', '')).strip():
        errors.append(f'{path.name}: filename does not match plant id "{p.get("id", "")}"')
    images = p.get('images') or {}
    if isinstance(images, dict):
        for part, value in images.items():
            if isinstance(value, str) and value.strip() and not value.startswith(('http://', 'https://', 'data:')):
                asset = ROOT / value
                if not asset.is_file():
                    errors.append(f'{p.get("id", path.stem)}: image path missing for {part}: {value}')

for p in supplementary:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    if not str(p.get('id', '')).strip():
        errors.append(f'Supplementary record {name}: missing id')
    if not str(p.get('identity', {}).get('name', '')).strip():
        errors.append(f'Supplementary record {p.get("id", "?")}: missing identity.name')
    if not str(p.get('identity', {}).get('botanical_name', '')).strip():
        warnings.append(f'{name}: missing botanical name')
    if not str(p.get('identity', {}).get('family', '')).strip():
        warnings.append(f'{name}: missing family')
    if not str(p.get('metadata', {}).get('status', '')).strip():
        warnings.append(f'{name}: missing metadata.status')

print(f'QUALITY AUDIT: {len(core)} NCISM records + {len(supplementary)} supplementary records in {len(files)} plant files, {len(errors)} blocking errors, {len(warnings)} warnings')
if warnings:
    print('WARNINGS:')
    for item in warnings[:250]:
        print(f' - {item}')
if errors:
    print('ERRORS:')
    for item in errors:
        print(f' - {item}')
    raise SystemExit(1)
print('QUALITY AUDIT PASSED: modular database structure is valid.')
