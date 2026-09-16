import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / 'plants.json').read_text(encoding='utf-8'))
core = sorted((p for p in plants if p.get('category') == 'NCISM-97'), key=lambda p: p.get('order', 0))

errors = []
warnings = []

# ---------- Structural integrity ----------
if len(core) != 97:
    errors.append(f'Expected exactly 97 NCISM-97 records; found {len(core)}')

names = [p.get('identity', {}).get('name', '').strip() for p in core]
ids = [p.get('id', '').strip() for p in core]
orders = [p.get('order') for p in core]
for label, values in [('name', names), ('id', ids), ('order', orders)]:
    dupes = sorted(k for k, n in Counter(values).items() if k and n > 1)
    if dupes:
        errors.append(f'Duplicate {label} values: {dupes}')

expected_orders = list(range(1, 98))
if sorted(o for o in orders if isinstance(o, int)) != expected_orders:
    errors.append('NCISM order values must be exactly 1..97')

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

    # ---------- Classical-reference quality ----------
    cr = p.get('classical_reference', {})
    shlokas = cr.get('shlokas') or []
    refs = cr.get('nighantu_references') or []
    status = str(cr.get('shloka_reference_status', '')).lower()

    if shlokas and not refs:
        warnings.append(f'{name}: shloka text exists but classical reference metadata is missing')
    if ('verified' in status) and not refs:
        warnings.append(f'{name}: status claims verification but reference metadata is empty')
    if shlokas and any(not isinstance(s, str) or not s.strip() for s in shlokas):
        errors.append(f'{name}: classical_reference.shlokas contains an empty/non-string item')
    if refs and any(not isinstance(r, str) or not r.strip() for r in refs):
        errors.append(f'{name}: classical_reference.nighantu_references contains an empty/non-string item')

    # Gemini is a provenance trail, not an authority. Flag verification claims for review.
    gem = p.get('gemini_source_data')
    if isinstance(gem, dict) and gem:
        source_text = json.dumps(gem, ensure_ascii=False).lower()
        if 'direct verified' in source_text or ('verified' in source_text and 'source' not in source_text):
            warnings.append(f'{name}: Gemini provenance contains verification language; manual source check recommended')

    # ---------- Local image integrity ----------
    for field, rel in (p.get('images') or {}).items():
        if not rel:
            continue
        if rel.startswith(('http://', 'https://')):
            continue
        if not (ROOT / rel).exists():
            warnings.append(f'{name}: image path does not exist: {rel}')

    # ---------- Source metadata types ----------
    for source in p.get('sources', []) or []:
        if not isinstance(source, dict):
            errors.append(f'{name}: source entry is not an object')
            continue
        for field in ('type', 'title', 'url', 'author', 'edition', 'year', 'page'):
            if field in source and not isinstance(source[field], str):
                errors.append(f'{name}: source field {field} is not a string')

# Botanical names should not be silently duplicated among the 97 records.
botanical = [p.get('identity', {}).get('botanical_name', '').strip().lower() for p in core]
for value, count in Counter(botanical).items():
    if value and count > 1:
        warnings.append(f'Duplicate botanical name among NCISM records: {value} ({count} records)')

# Taxonomic strings that are useful to review but are not automatically errors.
for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    botanical_name = str(p.get('identity', {}).get('botanical_name', ''))
    family = str(p.get('identity', {}).get('family', ''))
    if '(' in family and ')' in family:
        warnings.append(f'{name}: family field contains legacy synonym notation; verify against current accepted taxonomy: {family}')
    if 'Eclipta alba' in botanical_name:
        warnings.append(f'{name}: botanical name uses Eclipta alba; verify accepted nomenclature before publication')
    if 'Emblica officinalis' in botanical_name:
        warnings.append(f'{name}: botanical name uses Emblica officinalis; verify accepted nomenclature before publication')

# Review queue is deliberately non-blocking. Classical verse verification is edition-sensitive.
needs_review = []
for p in core:
    name = p.get('identity', {}).get('name', p.get('id', '?'))
    status = str(p.get('metadata', {}).get('status', '')).lower()
    cr_status = str(p.get('classical_reference', {}).get('shloka_reference_status', '')).lower()
    if any(token in status for token in ('needs_classical_source_verification', 'working_draft')) or any(
        token in cr_status for token in ('needs text', 'requires text', 'source-hub-added')
    ):
        needs_review.append(name)

print(f'QUALITY AUDIT: {len(core)} NCISM records, {len(errors)} blocking errors, {len(warnings)} warnings')
print(f'CLASSICAL REVIEW QUEUE: {len(needs_review)} records')
if warnings:
    print('WARNINGS:')
    for item in warnings[:250]:
        print(f' - {item}')
if errors:
    print('ERRORS:')
    for item in errors:
        print(f' - {item}')
    raise SystemExit(1)

print('QUALITY AUDIT PASSED: structural data is valid; review-only findings remain non-blocking.')
