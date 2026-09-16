import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Gemini IDs are matched by drug name, not NCISM order. Only standalone drugs
# that are part of the NCISM 97-drug database are applied.
# Gunja, Jayapala and Dhattura are not separate entries in the NCISM 97 list.
BATCH = {
    'Chitraka': {
        'identity': {
            'botanical_name': 'Plumbago zeylanica L.',
            'family': 'Plumbaginaceae',
            'english_name': 'Leadwort / White Leadwort',
            'synonyms': ['Agni', 'Dahana', 'Anala', 'Pachaka', 'Chitraka', 'Vyala']
        },
        'therapeutics': {
            'useful_part': ['root bark'],
            'indications': ['Agnimandya', 'Grahani', 'Arsha', 'Shotha', 'Shoola', 'Udara Roga']
        },
        'dravya_guna': {
            'rasa': ['katu'],
            'guna': ['laghu', 'ruksha', 'tikshna'],
            'virya': 'ushna',
            'vipaka': 'katu',
            'prabhava': 'Agrya Deepaniya / Pachana',
            'karma': ['Deepana', 'Pachana', 'Grahi', 'Kushtaghna', 'Shothahara', 'Arshoghna', 'Krimighna']
        },
        'dosha': {'vata': 'may increase when excessive', 'pitta': 'may increase when excessive', 'kapha': 'pacifies'},
        'formulations': [
            {'name': 'Chitrakadi Vati'},
            {'name': 'Chitraka Haritaki'},
            {'name': 'Chitrakadi Churna'},
            {'name': 'Chitraka Ghrita'},
            {'name': 'Kankayana Vati'}
        ],
        'identification': {
            'description': 'Perennial shrub with cylindrical root; root bark is the principal medicinal material and has a characteristic pungent, irritant taste.'
        },
        'classical_reference': {
            'shlokas': [
                'चित्रकोऽनलनामा च पाठी व्यालस्तथोषणः ।\nचित्रकः कटुकः पाके वह्निकृत्पाचनो लघुः ।\nरूक्षोष्णो ग्रहणीकुष्ठशोथार्शःकृमिकासनुत् ।\nवातश्लेष्महरो ग्राही वातर्शःश्लेष्मपित्तहृत् ॥'
            ],
            'nighantu_references': [
                'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 64 in the searchable recension; numbering varies by edition.'
            ],
            'samhita_references': [],
            'shloka_reference_status': 'verified against searchable Bhavaprakasha text; edition numbering should be checked against the selected printed edition',
            'reference_hubs': ['TDU Indian Medicinal Plants Database — Shlokas']
        },
        'metadata': {'status': 'classical_text_checked_batch_84_88'}
    },
    'Bhallataka': {
        'identity': {
            'botanical_name': 'Semecarpus anacardium L.f.',
            'family': 'Anacardiaceae',
            'english_name': 'Marking Nut / Clearing Nut',
            'synonyms': ['Arushkara', 'Arushkaraka', 'Agnika', 'Agnimukhi', 'Bhalli', 'Viravriksha', 'Shophakrit']
        },
        'therapeutics': {
            'useful_part': ['ripe fruit pulp/pericarp after proper purification'],
            'indications': ['Arsha', 'Kushta', 'Shotha', 'Gulma', 'Grahani', 'Anaha', 'Jwara', 'Krimi']
        },
        'dravya_guna': {
            'rasa': ['madhura', 'kashaya'],
            'guna': ['laghu', 'snigdha', 'tikshna'],
            'virya': 'ushna',
            'vipaka': 'madhura',
            'prabhava': 'Rasayana / Chedana-Bhedana',
            'karma': ['Deepana', 'Pachana', 'Chedana', 'Bhedana', 'Rasayana', 'Kushtaghna', 'Krimighna']
        },
        'dosha': {'vata': 'pacifies', 'pitta': 'may increase when excessive', 'kapha': 'pacifies'},
        'formulations': [
            {'name': 'Bhallataka Rasayana'},
            {'name': 'Amrita Bhallataka Lehya'},
            {'name': 'Bhallatakadi Ghrita'},
            {'name': 'Bhallatakadi Taila'},
            {'name': 'Bhallatakadi Asava'}
        ],
        'identification': {
            'description': 'Black ovoid drupe seated on an orange-yellow fleshy receptacle; pericarp contains a strongly irritant, vesicant oil and therefore requires proper purification before internal use.'
        },
        'classical_reference': {
            'shlokas': [
                'भल्लातकं त्रिषु प्रोक्तमरुष्कोऽग्निरोऽग्निकः ।\nतथैवाग्निमुखी भल्ली वीरवृक्षश्च शोफकृत् ॥\nभल्लातकफलं पक्वं स्वादुपाकरसं लघु ।\nकषायं पाचनं स्निग्धं तीक्ष्णोष्णं छेदि भेदनम् ॥\nमेध्यं वह्निकरं हन्ति कफवातव्रणोदरम् ।\nकुष्ठार्शो ग्रहणीगुल्मशोफानाहज्वरकृमीन् ॥'
            ],
            'nighantu_references': [
                'Bhavaprakasha Nighantu, Haritakyadi Varga, Bhallataka entry; searchable Chaukhambha/BharatKosha text. Verse numbering varies by edition.'
            ],
            'samhita_references': [],
            'shloka_reference_status': 'verified against searchable Bhavaprakasha text; supplied batch verse was corrected to the searchable recension and edition numbering should be checked',
            'reference_hubs': ['TDU Indian Medicinal Plants Database — Shlokas']
        },
        'metadata': {'status': 'classical_text_checked_batch_84_88'}
    }
}

with DATA.open('r', encoding='utf-8') as f:
    plants = json.load(f)

by_name = {p.get('identity', {}).get('name', '').strip().lower(): p for p in plants}

for name, patch in BATCH.items():
    key = name.lower()
    if key not in by_name:
        raise KeyError(f'NCISM database record not found for {name}')
    plant = by_name[key]
    for section, values in patch.items():
        if section == 'metadata':
            plant.setdefault('metadata', {}).update(values)
            continue
        if section == 'classical_reference':
            plant.setdefault('classical_reference', {}).update(values)
            continue
        plant.setdefault(section, {})
        for field, value in values.items():
            plant[section][field] = value

with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('Applied NCISM-matching Gemini batch 84-88: Chitraka, Bhallataka')
print('Skipped non-NCISM standalone drugs: Gunja, Jayapala, Dhattura')
