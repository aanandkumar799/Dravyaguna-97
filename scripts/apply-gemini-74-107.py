import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Consolidates later Gemini batches without creating duplicate master records.
# NCISM-97 drugs are merged into their existing records. Other useful drugs are
# retained as supplementary records for teachers, doctors/practitioners and general reference.
CORE_PATCHES = {
    'jatamansi': {'teacher_note': 'Gemini batch 75: supplementary teaching and classical-reference material retained; exact shloka requires text-level verification.'},
    'vacha': {'teacher_note': 'Gemini batch 76: supplementary teaching and classical-reference material retained; exact shloka requires text-level verification.'},
    'sarpagandha': {'teacher_note': 'Gemini batch 77: modern pharmacology material retained. The supplied verse containing modern terminology is not labelled as a classical quotation.'},
    'ativisha': {'teacher_note': 'Gemini batch 78: structured identity, guna and therapeutic material retained; classical verse requires primary-text verification.'},
    'vatsanabha': {'teacher_note': 'Gemini batches 79, 103 and 107 merged into this single NCISM-97 master record; duplicate records are not created.'},
    'katuki': {'teacher_note': 'Gemini batches 56 and 80 merged. Classical verse/reference remains subject to primary-text verification.'},
    'bhringaraja': {'teacher_note': 'Gemini batches 61 and 82 merged. Classical verse requires primary-text verification.'},
    'kumkum': {'teacher_note': 'Gemini batch 83 retained; classical reference requires primary-text verification.'},
    'chitraka': {'teacher_note': 'Gemini batch 84 retained; supplied classical verse requires primary-text verification.'},
    'bhallataka': {'teacher_note': 'Gemini batches 63 and 85 merged; use verified classical passages rather than unverified paraphrases.'},
    'ahiphena': {'teacher_note': 'Gemini batches 90, 101 and 104 merged into NCISM-97 #41; duplicate records are not created. Toxic-drug information should be handled with safety context.'},
    'kampillaka': {'teacher_note': 'Gemini batch 96 retained; classical references require primary-text verification.'},
    'latakaranja': {'teacher_note': 'Gemini batch 98 retained; classical references require primary-text verification.'},
}

SUPPLEMENTARY = [
    ('karpura', 'Karpura', 'कर्पूर', 'Cinnamomum camphora (L.) J.Presl', 'Lauraceae', 'Camphor', 'Gemini batch 74'),
    ('tejapatra', 'Tejapatra', 'तेजपत्त्र', 'Cinnamomum tamala (Buch.-Ham.) T.Nees & Eberm.', 'Lauraceae', 'Indian bay leaf', 'Gemini batch 70'),
    ('kankola', 'Kankola', 'कङ्कोल', 'Cubeba officinalis Miq.', 'Piperaceae', 'Cubeb', 'Gemini batch 73'),
    ('kiratatikta', 'Kiratatikta', 'किराततिक्त', 'Swertia chirata (Roxb. ex Flem.) Karsten', 'Gentianaceae', 'Chirata', 'Gemini batch 81'),
    ('gunja', 'Gunja', 'गुञ्जा', 'Abrus precatorius L.', 'Fabaceae', 'Rosary pea', 'Gemini batches 86 and 99'),
    ('jayapala', 'Jayapala', 'जयपाल', 'Croton tiglium L.', 'Euphorbiaceae', 'Purging croton', 'Gemini batch 87'),
    ('dhattura', 'Dhattura', 'धत्तूर', 'Datura metel L.', 'Solanaceae', 'Datura', 'Gemini batches 88 and 102'),
    ('bhanga', 'Bhanga', 'भङ्गा', 'Cannabis sativa L.', 'Cannabaceae', 'Cannabis', 'Gemini batches 89, 100 and 105'),
    ('arka', 'Arka', 'अर्क', 'Calotropis gigantea (L.) Dryand.', 'Apocynaceae', 'Crown flower', 'Gemini batch 91'),
    ('snuhi', 'Snuhi', 'स्नुही', 'Euphorbia neriifolia L.', 'Euphorbiaceae', 'Indian spurge tree', 'Gemini batches 92 and 106'),
    ('langali', 'Langali', 'लाङ्गली', 'Gloriosa superba L.', 'Colchicaceae', 'Gloriosa lily', 'Gemini batch 93'),
    ('karavira', 'Karavira', 'करवीर', 'Nerium oleander L.', 'Apocynaceae', 'Oleander', 'Gemini batch 94'),
    ('kupilu', 'Kupilu', 'कुपीलु', 'Strychnos nux-vomica L.', 'Loganiaceae', 'Nux-vomica', 'Gemini batch 95'),
    ('parasika-yavani', 'Parasika Yavani', 'पारसीक यवानी', '', 'Apiaceae', 'Persian ajwain', 'Gemini batch 97'),
]


def supplementary_record(item):
    pid, name, sanskrit, botanical, family, english, source_note = item
    return {
        'id': pid, 'order': None, 'category': 'Supplementary', 'syllabus_marker': 'Supplementary',
        'identity': {'name': name, 'sanskrit_name': sanskrit, 'transliteration': '', 'botanical_name': botanical, 'family': family, 'english_name': english, 'hindi_name': '', 'regional_names': [], 'synonyms': []},
        'classification': {'kingdom': 'Plantae', 'habit': '', 'habitat': '', 'distribution': ''},
        'identification': {'description': '', 'whole_plant': '', 'root': '', 'stem': '', 'leaf': '', 'flower': '', 'fruit': '', 'seed': '', 'bark': '', 'identification_points': []},
        'images': {'whole_plant': '', 'habit': '', 'root': '', 'stem': '', 'leaf': '', 'flower': '', 'fruit': '', 'seed': '', 'bark': ''},
        'dravya_guna': {'rasa': [], 'guna': [], 'virya': '', 'vipaka': '', 'prabhava': '', 'karma': []},
        'dosha': {'vata': '', 'pitta': '', 'kapha': ''},
        'therapeutics': {'useful_part': [], 'indications': [], 'therapeutic_actions': [], 'dose': '', 'anupana': '', 'duration': '', 'precautions': 'Supplementary reference only; verify identity, purification and safety before clinical use.', 'contraindications': ''},
        'formulations': [],
        'classical_reference': {'shlokas': [], 'nighantu_references': [], 'samhita_references': [], 'shloka_reference_status': 'requires text-level verification'},
        'phytochemistry': {'major_constituents': [], 'chemical_notes': ''},
        'modern_information': {'evidence_summary': '', 'recognized_uses': [], 'safety_notes': '', 'sources': []},
        'student': {'exam_points': [], 'viva_questions': [], 'identification_points': [], 'mnemonics': [], 'quick_revision': ''},
        'teacher': {'teaching_points': [f'Retained as supplementary material from {source_note}.'], 'discussion_points': [], 'practical_points': []},
        'doctor': {'quick_reference': 'Supplementary reference record; verify authoritative sources before clinical use.', 'important_indications': [], 'useful_part': '', 'dose': '', 'anupana': '', 'key_precautions': ['Use authoritative identification and safety references.']},
        'sources': [{'type': 'gemini_source_batch', 'title': source_note, 'url': ''}],
        'metadata': {'status': 'supplementary_needs_source_verification', 'source_batch': source_note, 'version': '1.0'}
    }

plants = json.loads(DATA.read_text(encoding='utf-8'))
by_name = {p.get('identity', {}).get('name', '').strip().lower(): p for p in plants}

for name, patch in CORE_PATCHES.items():
    if name not in by_name:
        raise KeyError(f'Expected NCISM master record not found: {name}')
    p = by_name[name]
    p['category'] = 'NCISM-97'
    if p.get('order') is not None:
        p.setdefault('syllabus_marker', 'NCISM-97')
    p.setdefault('teacher', {}).setdefault('discussion_points', []).append(patch['teacher_note'])
    p.setdefault('metadata', {})['gemini_later_batches_reviewed'] = True

# Mark every existing NCISM record explicitly, without changing its identity/order.
for p in plants:
    if isinstance(p.get('order'), int) and 1 <= p['order'] <= 97:
        p['category'] = 'NCISM-97'
        p.setdefault('syllabus_marker', 'NCISM-97')

for item in SUPPLEMENTARY:
    pid = item[0]
    existing = next((p for p in plants if p.get('id') == pid), None)
    if existing:
        existing.update(supplementary_record(item))
    else:
        plants.append(supplementary_record(item))

# Deduplicate by id and by normalized name; preserve the first master record.
seen_ids, seen_names, out = set(), set(), []
for p in plants:
    pid = str(p.get('id', '')).strip().lower()
    nm = str(p.get('identity', {}).get('name', '')).strip().lower()
    if not pid or pid in seen_ids or (nm and nm in seen_names):
        continue
    seen_ids.add(pid)
    if nm: seen_names.add(nm)
    out.append(p)

out.sort(key=lambda p: (0 if p.get('category') == 'NCISM-97' else 1, p.get('order') if isinstance(p.get('order'), int) else 9999, str(p.get('identity', {}).get('name', ''))))
assert sum(1 for p in out if p.get('category') == 'NCISM-97') == 97
DATA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Consolidated database: 97 NCISM-97 records + {len(out)-97} supplementary records; duplicates merged.')
