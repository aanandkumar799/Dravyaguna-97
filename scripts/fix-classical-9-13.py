import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'
with DATA.open('r', encoding='utf-8') as f:
    plants = json.load(f)

FIXES = {
    'shunthi': {
        'shloka': 'शुण्ठी रुच्यामवातघ्नी पाचनी कटुका लघुः ।\nस्निग्धोष्णा मधुरा पाके कफवातविबन्धनुत् ॥४५॥',
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verse 45; related therapeutic continuation in verse 46. Independently searchable recension; edition numbering may vary.',
        'status': 'verified_reference_text_corrected',
    },
    'maricha': {
        'shloka': 'मरिचं कटुकं तीक्ष्णं दीपनं कफवातजित् ।\nउष्णं पित्तकरं रूक्षं श्वासशूलकृमीन् हरेत् ॥६०॥',
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 59–61; verse 59 gives synonyms and verses 60–61 properties/ardraka comparison. Independently searchable recension; edition numbering may vary.',
        'status': 'verified_reference_text_corrected',
    },
    'guggulu': {
        'reference': 'Bhavaprakasha Nighantu, Karpuradi Varga. The searchable recension places Guggulu after the five varieties (verses 29–30) and its properties in the following verses; exact verse numbering is edition-dependent. The unverified 33–35 citation is removed.',
        'status': 'reference_identified_numbering_needs_edition_verification',
    },
    'eranda': {
        'reference': 'Bhavaprakasha Nighantu, Guduchyadi Varga. Exact verse numbering and quotation require edition-level verification; the previously supplied 60–61 citation is not retained as verified.',
        'status': 'needs_verification',
    },
    'punarnava': {
        'reference': 'Bhavaprakasha Nighantu, Guduchyadi Varga. Exact verse numbering and quotation require edition-level verification; the previously supplied 231–232 citation is not retained as verified.',
        'status': 'needs_verification',
    },
}

for p in plants:
    key = str(p.get('id', '')).lower()
    if key not in FIXES:
        continue
    c = p.setdefault('classical_reference', {})
    fix = FIXES[key]
    if 'shloka' in fix:
        c['shlokas'] = [fix['shloka']]
    c['nighantu_references'] = [fix['reference']]
    c['shloka_reference_status'] = fix['status']
    c['reference_hubs'] = list(dict.fromkeys(c.get('reference_hubs', []) + ['TDU Indian Medicinal Plants Database — Shlokas']))
    p.setdefault('metadata', {})['classical_review_batch'] = '9-13 corrected 2026-09-16'

with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('Corrected classical-reference fields for IDs 9–13.')
