import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Gemini batch IDs are matched by drug name, not NCISM order number.
# Only drugs that are actually part of the NCISM 97-drug database are applied.
# Tejapatra and Kankola are not separate entries in the NCISM 97 list, so they
# are intentionally not inserted as new records.
BATCH = {
    'Nagkeshar': {
        'identity': {
            'botanical_name': 'Mesua ferrea L.',
            'family': 'Calophyllaceae (Guttiferae)',
            'english_name': "Cobra's Saffron / Ironwood Tree",
            'synonyms': ['Nagapushpa', 'Naga', 'Kesara', 'Nagakeshara', 'Champaka', 'Nagakinjalka']
        },
        'therapeutics': {
            'useful_part': ['stamen / flower stamens (Pumkeshara)'],
            'indications': ['Jwara', 'Kandu', 'Trishna', 'Swedadhikya', 'Chhardi', 'Hridroga/Hrillasa', 'Kushta', 'Raktapitta']
        },
        'dravya_guna': {
            'rasa': ['kashaya', 'tikta'],
            'guna': ['laghu', 'ruksha'],
            'virya': 'ushna',
            'vipaka': 'katu',
            'prabhava': 'Amapachana / Vishaghna',
            'karma': ['Amapachana', 'Kandughna', 'Trishnahara', 'Chhardighna', 'Kushtaghna', 'Vishaghna']
        },
        'dosha': {'vata': 'context dependent', 'pitta': 'may pacify', 'kapha': 'pacifies'},
        'formulations': [{'name': 'Chaturjata'}, {'name': 'Pushyanuga Churna'}, {'name': 'Khadiradi Vati'}],
        'identification': {'description': 'Golden-yellow stamens of Mesua ferrea flower; the dried stamens are the principal drug material.'},
        'classical_reference': {
            'shlokas': ['नागपुष्पं कषायोष्णं रूक्षं लघ्वामपाचनम् ।\nज्वरकण्डूतृषास्वेदच्छर्दिहृल्लासनाशनम् ।\nदौर्गन्ध्यकुष्ठवीसर्पकफपित्तविषापहम् ॥'],
            'nighantu_references': ['Bhavaprakasha Nighantu, Karpuradi Varga, verses 69–71 in the searchable recension; numbering varies by edition.'],
            'samhita_references': [],
            'shloka_reference_status': 'verified against searchable Bhavaprakasha text; edition numbering/page should be checked against the selected printed edition',
            'reference_hubs': ['TDU Indian Medicinal Plants Database — Shlokas']
        },
        'metadata': {'status': 'classical_text_checked_batch_69_73'}
    },
    'Lavanga': {
        'identity': {
            'botanical_name': 'Syzygium aromaticum (L.) Merr. & L.M.Perry',
            'family': 'Myrtaceae',
            'english_name': 'Clove',
            'synonyms': ['Devakusuma', 'Shrisanjna', 'Shriprasunaka', 'Sekhara']
        },
        'therapeutics': {
            'useful_part': ['dried flower bud'],
            'indications': ['Kasa', 'Shwasa', 'Chhardi', 'Trishna', 'Adhmana', 'Shoola', 'Hikka', 'Agnimandya']
        },
        'dravya_guna': {
            'rasa': ['katu', 'tikta'],
            'guna': ['laghu'],
            'virya': 'sheeta',
            'vipaka': 'katu',
            'prabhava': 'Chhardighna / Shoolahara / Kasahara',
            'karma': ['Deepana', 'Pachana', 'Rochana', 'Kaphapittahara', 'Chhardighna', 'Shoolahara', 'Kasahara']
        },
        'dosha': {'vata': 'context dependent', 'pitta': 'may pacify', 'kapha': 'pacifies'},
        'formulations': [{'name': 'Lavangadi Vati'}, {'name': 'Lavangadi Churna'}, {'name': 'Eladi Churna'}, {'name': 'Khadiradi Vati'}],
        'identification': {'description': 'Dark reddish-brown nail-shaped dried flower buds with four calyx teeth and an unopened rounded corolla.'},
        'classical_reference': {
            'shlokas': ['लवङ्गं देवकुसुमं श्रीसंज्ञं श्रीप्रसूनकम् ।\nलवङ्गं कटुकं तिक्तं लघु नेत्रहितं हिमम् ।\nदीपनं पाचनं रुच्यं कफपित्तास्रनाशकृत् ।\nतृष्णां छर्दिं तथाध्मानं शूलमाशु विनाशयेत् ।\nकासं श्वासञ्च हिक्काञ्च क्षयं क्षययति ध्रुवम् ॥'],
            'nighantu_references': ['Bhavaprakasha Nighantu, Karpuradi Varga, verses 58–59 in the searchable recension; numbering varies by edition.'],
            'samhita_references': [],
            'shloka_reference_status': 'verified against searchable Bhavaprakasha text; supplied batch verse was corrected to the searchable recension',
            'reference_hubs': ['TDU Indian Medicinal Plants Database — Shlokas']
        },
        'metadata': {'status': 'classical_text_checked_batch_69_73'}
    },
    'Jatiphala': {
        'identity': {
            'botanical_name': 'Myristica fragrans Houtt.',
            'family': 'Myristicaceae',
            'english_name': 'Nutmeg',
            'synonyms': ['Jatikosha', 'Jatisasya', 'Malatiphala', 'Jatisara', 'Majasara']
        },
        'therapeutics': {
            'useful_part': ['seed kernel (Bija)', 'aril (Jatipatri is a separate drug part)'],
            'indications': ['Atisara', 'Grahani', 'Aruchi', 'Mukha-vairasya', 'Kasa', 'Shwasa', 'Pinas', 'Kaphavata disorders']
        },
        'dravya_guna': {
            'rasa': ['tikta', 'katu'],
            'guna': ['laghu', 'tikshna'],
            'virya': 'ushna',
            'vipaka': 'katu',
            'prabhava': 'Grahi / Deepana / Rochana',
            'karma': ['Deepana', 'Grahi', 'Rochana', 'Swarya', 'Kaphavatahara', 'Mukhadurgandhahara']
        },
        'dosha': {'vata': 'pacifies', 'pitta': 'may increase when excessive', 'kapha': 'pacifies'},
        'formulations': [{'name': 'Jatiphaladi Churna'}, {'name': 'Jatiphaladi Vati'}, {'name': 'Brihat Gangadhara Churna'}, {'name': 'Jatiphala Taila'}],
        'identification': {'description': 'Ovoid hard seed with marbled/ruminate brown endosperm and strong characteristic aromatic odor; mace is the separate aril.'},
        'classical_reference': {
            'shlokas': ['जातीफलं जातिकोशं मालतीफलमित्यपि ।\nजातीफलं रसे तिक्तं तीक्ष्णोष्णं रोचनं लघु ।\nकटुकं दीपनं ग्राहि स्वर्यं श्लेष्मानिलापहम् ॥\nनिहन्ति मुखवैरस्यं मलदौर्गन्ध्यकृष्णताः ।\nकृमिकासवमिश्वासशोषपीनसहृद्रुजः ॥'],
            'nighantu_references': ['Bhavaprakasha Nighantu, Karpuradi Varga, verses 48–49 in the searchable recension; numbering varies by edition.'],
            'samhita_references': [],
            'shloka_reference_status': 'verified against searchable Bhavaprakasha text; supplied batch verse was corrected to the searchable recension',
            'reference_hubs': ['TDU Indian Medicinal Plants Database — Shlokas']
        },
        'metadata': {'status': 'classical_text_checked_batch_69_73'}
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
        if isinstance(values, dict):
            for field, value in values.items():
                plant[section][field] = value

with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('Applied NCISM-matching Gemini batch 69-73: Nagkeshar, Lavanga, Jatiphala')
print('Skipped non-NCISM standalone drugs from this Gemini batch: Tejapatra, Kankola')
