import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / 'plants.json').read_text(encoding='utf-8'))
core = [p for p in plants if p.get('category') == 'NCISM-97']

errors = []
warnings = []

if len(core) != 97:
    errors.append(f'Expected exactly 97 NCISM-97 records; found {len(core)}')

names = [p.get('identity', {}).get('name', '').strip() for p in core]
ids = [p.get('id', '').strip() for p in core]
orders = [p.get('order') for p in core]
for label, values in [('name', names), ('id', ids), ('order', orders)]:
    dupes = sorted(k for k, n in Counter(values).items() if k and n > 1)
    if dupes:
        errors.append(f'Duplicate {label} values: {dupes}')

required_strings = [
    ('identity.name', lambda p: p.get('identity', {}).get('name')),
    ('identity.botanical_name', lambda p: p.get('identity', {}).get('botanical_name')),
    ('identity.family', lambda p: p.get('identity', {}).get('family')),
    ('dravya_guna.virya', lambda p: p.get('dravya_guna', {}).get('virya')),
    ('dravya_guna.vipaka', lambda p: p.get('dravya_guna', {}).get('vipaka')),
]
for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    for field, getter in required_strings:
        value = getter(p)
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{name}: missing {field}')
    rasa = p.get('dravya_guna', {}).get('rasa')
    guna = p.get('dravya_guna', {}).get('guna')
    useful = p.get('therapeutics', {}).get('useful_part')
    if not isinstance(rasa, list) or not rasa:
        errors.append(f'{name}: rasa must be a non-empty list')
    if not isinstance(guna, list) or not guna:
        errors.append(f'{name}: guna must be a non-empty list')
    if not isinstance(useful, list) or not useful:
        errors.append(f'{name}: therapeutics.useful_part must be a non-empty list')

    # Never allow an exact classical quotation to be labelled verified without a reference.
    cr = p.get('classical_reference', {})
    shlokas = cr.get('shlokas') or []
    status = str(cr.get('shloka_reference_status', '')).lower()
    refs = cr.get('nighantu_references') or []
    if shlokas and not refs:
        errors.append(f'{name}: shloka present without nighantu/classical reference')
    if 'verified' in status and not refs:
        errors.append(f'{name}: classical status says verified but reference list is empty')

    # Flag placeholder/generated provenance for manual review; do not silently treat it as authoritative.
    gem = p.get('gemini_source_data')
    if isinstance(gem, dict) and gem:
        source_text = json.dumps(gem, ensure_ascii=False).lower()
        if 'direct verified' in source_text or 'verified' in source_text and 'source' not in source_text:
            warnings.append(f'{name}: Gemini provenance contains verification language; manual source check recommended')

    # Validate local image paths that are explicitly present.
    for field, rel in (p.get('images') or {}).items():
        if not rel:
            continue
        if rel.startswith('http://') or rel.startswith('https://'):
            continue
        if not (ROOT / rel).exists():
            warnings.append(f'{name}: image path does not exist: {rel}')

# Botanical names should not be silently duplicated among the 97 records.
botanical = [p.get('identity', {}).get('botanical_name', '').strip().lower() for p in core]
for value, count in Counter(botanical).items():
    if value and count > 1:
        warnings.append(f'Duplicate botanical name among NCISM records: {value} ({count} records)')

# Report records still explicitly marked as requiring classical verification.
needs_review = [
    p.get('identity', {}).get('name', p.get('id', '?'))
    for p in core
    if 'needs_classical_source_verification' in str(p.get('metadata', {}).get('status', '')).lower()
    or 'needs text' in str(p.get('classical_reference', {}).get('shloka_reference_status', '')).lower()
    or 'requires text' in str(p.get('classical_reference', {}).get('shloka_reference_status', '')).lower()
]

print(f'QUALITY AUDIT: {len(core)} NCISM records, {len(errors)} errors, {len(warnings)} warnings')
if warnings:
    print('WARNINGS:')
    for item in warnings[:200]:
        print(f' - {item}')
print(f'CLASSICAL REVIEW QUEUE: {len(needs_review)} records')
if needs_review:
    print(' - ' + ', '.join(needs_review))

if errors:
    print('ERRORS:')
    for item in errors:
        print(f' - {item}')
    raise SystemExit(1)
