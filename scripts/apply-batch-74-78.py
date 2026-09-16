import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Gemini batch IDs are matched by drug name, not NCISM order. Karpura is not one
# of the 97 NCISM II BAMS Dravyaguna drugs, so it is intentionally not inserted.
BATCH = {
    'Jatamansi': {
        'identity': {'botanical_name': 'Nardostachys jatamansi (D.Don) DC.', 'family': 'Caprifoliaceae (Valerianaceae)', 'english_name': 'Spikenard / Indian Nard', 'synonyms': ['Mansi', 'Tapasvini', 'Jatila', 'Nalada', 'Bhutajata']},
        'therapeutics': {'useful_part': ['rhizome/root'], 'indications': ['Anidra', 'Unmada', 'Apasmara', 'Manas disorders', 'Shiroshoola', 'Hridroga']},
        'dravya_guna': {'rasa': ['tikta', 'kashaya', 'madhura'], 'guna': ['laghu', 'snigdha'], 'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Medhya / Nidrajanana / Manasadoshahara', 'karma': ['Medhya', 'Nidrajanana', 'Manasadoshahara', 'Hridya', 'Kushtaghna', 'Dahaprashamana', 'Keshya', 'Vishaghna']},
        'dosha': {'vata': 'generally pacifies', 'pitta': 'pacifies', 'kapha': 'generally pacifies'},
        'identification': {'description': 'Aromatic perennial herb with a short rhizome bearing dense fibrous rootlets and remnants of leaf bases; Himalayan drug.'},
        'formulations': [{'name': 'Jatamansi Churna'}, {'name': 'Jatamansyarka'}, {'name': 'Mansyadi Kwatha'}, {'name': 'Saraswatarishta'}, {'name': 'Mahakalyanaka Ghrita'}],
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Karpuradi Varga, verse 75 (Chunekar/2015 edition citation reported in searchable source)'], 'shloka_reference_status': 'reference located; exact Devanagari verse requires text-level transcription check'}
    },
    'Vacha': {
        'identity': {'botanical_name': 'Acorus calamus L.', 'family': 'Acoraceae', 'english_name': 'Sweet Flag / Calamus', 'synonyms': ['Ugragandha', 'Shadgrantha', 'Golomi', 'Mangalya', 'Jatila']},
        'therapeutics': {'useful_part': ['rhizome'], 'indications': ['Unmada', 'Apasmara', 'Swarabheda', 'Smritibhramsha', 'Agnimandya', 'Vibandha']},
        'dravya_guna': {'rasa': ['katu', 'tikta'], 'guna': ['laghu', 'tikshna'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Medhya / Sanjnasthapana / Swarya', 'karma': ['Medhya', 'Sanjnasthapana', 'Swarya', 'Vamana', 'Deepana', 'Pachana', 'Kaphaghna', 'Unmadahara']},
        'dosha': {'vata': 'pacifies', 'pitta': 'may increase when excessive', 'kapha': 'pacifies'},
        'identification': {'description': 'Aromatic, branched rhizome with characteristic leaf scars and fibrous rootlets; interior is pale and spongy.'},
        'formulations': [{'name': 'Saraswata Churna'}, {'name': 'Vachadi Churna'}, {'name': 'Brahmi Ghrita'}, {'name': 'Sanjivani Vati'}, {'name': 'Vachadi Taila'}],
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga — exact verse number/transcription requires edition-level verification'], 'shloka_reference_status': 'needs_verification'}
    },
    'Sarpagandha': {
        'identity': {'botanical_name': 'Rauvolfia serpentina (L.) Benth. ex Kurz', 'family': 'Apocynaceae', 'english_name': 'Indian Snakeroot / Serpentina', 'synonyms': ['Nakuli', 'Chandrika', 'Sarpakshi', 'Dhavala', 'Bhujangakshi']},
        'therapeutics': {'useful_part': ['root'], 'indications': ['Raktachapa / hypertension', 'Anidra', 'Unmada', 'Bhrama', 'Sarpa-visha context in traditional literature']},
        'dravya_guna': {'rasa': ['tikta'], 'guna': ['ruksha'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Nidrajanana / Unmadahara', 'karma': ['Nidrajanana', 'Raktachapahara', 'Unmadahara', 'Hrid-shamana', 'Vedanasthapana']},
        'dosha': {'vata': 'may pacify in appropriate context', 'pitta': 'requires context-specific use', 'kapha': 'generally reduces'},
        'identification': {'description': 'Perennial shrub with tapering, tortuous, cylindrical roots; roots are the principal medicinal part.'},
        'formulations': [{'name': 'Sarpagandha Churna'}, {'name': 'Sarpagandha Vati'}, {'name': 'Sarpagandhadi Churna'}, {'name': 'Sarpagandha Ghrita'}],
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Classical Dravyaguna sources should be checked for the exact Sarpagandha verse; the supplied modern hypertension verse is not treated as a classical quotation.'], 'shloka_reference_status': 'needs_verification'}
    },
    'Ativisha': {
        'identity': {'botanical_name': 'Aconitum heterophyllum Wall. ex Royle', 'family': 'Ranunculaceae', 'english_name': 'Indian Atees', 'synonyms': ['Shuklakanda', 'Bhangura', 'Vishva', 'Aruna', 'Shringi']},
        'therapeutics': {'useful_part': ['tuberous root'], 'indications': ['Atisara', 'Amaatisara', 'Jwara', 'Agnimandya', 'Chhardi', 'Balaroga']},
        'dravya_guna': {'rasa': ['tikta', 'katu'], 'guna': ['laghu', 'ruksha'], 'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Deepana / Pachana / Atisarahara', 'karma': ['Deepana', 'Pachana', 'Grahi', 'Amapachana', 'Jwarahara', 'Krimighna', 'Vishaghna', 'Atisarahara']},
        'dosha': {'vata': 'generally not aggravating when appropriately used', 'pitta': 'generally pacifies in classical context', 'kapha': 'pacifies'},
        'identification': {'description': 'Small ovoid/conical tuberous roots, pale greyish-white internally; distinguished from highly toxic aconites used as Vatsanabha.'},
        'formulations': [{'name': 'Balachaturbhadra Churna'}, {'name': 'Ativishadi Churna'}, {'name': 'Gangadhara Churna'}, {'name': 'Sudarshana Churna'}],
        'classical_reference': {'shlokas': [], 'nighantu_references': ['Bhavaprakasha Nighantu, Haritakyadi Varga — exact verse should be checked against the NIIMH/e-Nighantu text before quotation'], 'shloka_reference_status': 'reference hub located; supplied verse not treated as verified'}
    }
}

with DATA.open('r', encoding='utf-8') as f:
    plants = json.load(f)

by_name = {p.get('identity', {}).get('name', '').strip().lower(): p for p in plants}
for name, patch in BATCH.items():
    p = by_name.get(name.lower())
    if not p:
        continue
    for section, values in patch.items():
        if section == 'classical_reference':
            cr = p.setdefault('classical_reference', {})
            for key, value in values.items():
                if key == 'shlokas':
                    # Never overwrite a previously verified classical quotation.
                    if not cr.get('shlokas'):
                        cr['shlokas'] = value
                elif key == 'nighantu_references':
                    existing = cr.setdefault('nighantu_references', [])
                    for ref in value:
                        if ref not in existing:
                            existing.append(ref)
                else:
                    cr[key] = value
        elif section in ('identity', 'therapeutics', 'dravya_guna', 'dosha', 'identification'):
            dst = p.setdefault(section, {})
            for key, value in values.items():
                if not dst.get(key):
                    dst[key] = value
        elif section == 'formulations':
            existing = p.setdefault('formulations', [])
            names = {x.get('name') for x in existing if isinstance(x, dict)}
            for item in values:
                if item['name'] not in names:
                    existing.append(item)

    p.setdefault('metadata', {})['last_enrichment'] = 'structured-field + classical-reference review + curated batch 74-78'
    p['metadata']['status'] = 'curated_batch_added_classical_text_verification_pending'

# Preserve the 97-record NCISM structure; no Karpura record is created.
assert len(plants) == 97
assert len({p.get('id') for p in plants}) == 97
with DATA.open('w', encoding='utf-8') as f:
    json.dump(plants, f, ensure_ascii=False, indent=2)
    f.write('\n')
