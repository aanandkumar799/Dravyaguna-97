import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'

# Full Gemini records supplied by the user for batches 74-78.
# The complete source object is retained under `gemini_source_data`; mapped fields
# are also merged into the normal master-record schema. Core NCISM drugs are merged
# into their existing records; Karpura remains a supplementary record.
GEMINI_74_78 = [
  {
    "id": 74,
    "classical_sanskrit_name": "Karpura (कर्पूर)",
    "botanical_name": "Cinnamomum camphora (L.) J.Presl",
    "family": "Lauraceae",
    "english_common_name": "Camphor",
    "sanskrit_synonyms": ["Ghanasara (घनसारा)", "Himavaluka (हिमवालुका)", "Chandra (चन्द्र)", "Sphatika (स्फटिक)", "Subhra (शुभ्र)"],
    "useful_part": "Crystalline Extract / Sublimated Niryasa (Karpura)",
    "rasa": ["Tikta", "Katu", "Madhura"],
    "guna": ["Laghu", "Tikshna", "Snigdha"],
    "virya": "Sheeta",
    "vipaka": "Katu",
    "prabhava": "Hridya / Chakshushya / Vedanasthapana",
    "dosha_karma": "Tridoshashamaka (Specially Kapha-Pittashamaka)",
    "pharmacological_therapeutic_karma": ["Hridya", "Vedanasthapana", "Chakshushya", "Chedana", "Kasahara", "Mukhadurgandhahara", "Dahaprashamana", "Krimighna"],
    "important_indications": ["Hridroga (Heart disease / Functional cardiac weakness)", "Shwasa / Kasa (Dyspnea / Cough)", "Mukharoga (Oral infections / Dental pain)", "Trishna (Excessive thirst)", "Daha (Burning sensation)", "Sandhishoola (Joint pain / Arthralgia)"],
    "important_formulations": ["Karpuradi Churna", "Karpuradi Taila", "Karpura Rasa", "Amritdhara", "Karpurasava"],
    "identification_characters": "White translucent crystalline masses or powder, highly volatile at room temperature, characteristic penetrating aromatic odor, cool pungent taste followed by a cooling sensation.",
    "classical_shloka": "कर्पूरः शीतलो हृद्यश्चक्षुष्यो लेपनो लघुः।\nतिक्तो मधुरः कटुकः सुगन्धिः कफपित्तहा॥",
    "shloka_source": {"text_grantha_name": "Bhavaprakasha Nighantu", "sthana_section": "Nighantu Sthana", "adhyaya": "N/A", "varga_chapter": "Karpuradi Varga", "shloka_number": "Verse 2-3", "edition_publisher": "Chowkhamba Bharati Academy, Varanasi", "page_number": "Needs checking against physical copy for exact page"},
    "verification_status": "A. Directly verified classical reference"
  },
  {
    "id": 75,
    "classical_sanskrit_name": "Jatamansi (जटामांसी)",
    "botanical_name": "Nardostachys jatamansi (D.Don) DC.",
    "family": "Caprifoliaceae (Valerianaceae)",
    "english_common_name": "Spikenard / Indian Nard",
    "sanskrit_synonyms": ["Mansi (मांसी)", "Tapasvini (तपस्विनी)", "Jatila (जटिला)", "Nalada (नलदा)", "Bhutajata (भूतजटा)"],
    "useful_part": "Rhizome / Root (Kanda / Mula)",
    "rasa": ["Tikta", "Kashaya", "Madhura"],
    "guna": ["Laghu", "Snigdha"],
    "virya": "Sheeta",
    "vipaka": "Katu",
    "prabhava": "Medhya / Nidrajanana / Manasadoshahara",
    "dosha_karma": "Tridoshashamaka (Specially Kapha-Pittashamaka)",
    "pharmacological_therapeutic_karma": ["Medhya", "Nidrajanana", "Manasadoshahara", "Hridya", "Kushtaghna", "Dahaprashamana", "Keshya", "Vishaghna"],
    "important_indications": ["Anidra (Insomnia)", "Unmada (Psychosis / Mania)", "Apasmara (Epilepsy)", "Manasaroga (Anxiety / Psychiatric disorders)", "Shiro-shoola (Headache)", "Hridroga (Cardiac neurosis / Palpitations)"],
    "important_formulations": ["Jatamansi Churna", "Jatamansyark", "Mansyadi Kwatha", "Saraswatarishta", "Mahakalyanaka Ghrita"],
    "identification_characters": "Dark brown highly fibrous woody rhizomes crowned with dense reddish-brown tufts of fibrous leaf-remnants, intensely aromatic heavy musky-earthy odor, bitter acrid taste.",
    "classical_shloka": "मांसी तिक्ता कषाया च स्वाद्वी शीता च दाहहृत्।\nमेध्या कान्तिबलायुष्या कफपित्तविषापहा॥",
    "shloka_source": {"text_grantha_name": "Bhavaprakasha Nighantu", "sthana_section": "Nighantu Sthana", "adhyaya": "N/A", "varga_chapter": "Karpuradi Varga", "shloka_number": "Verse 88-89", "edition_publisher": "Chowkhamba Bharati Academy, Varanasi", "page_number": "Needs checking against physical copy for exact page"},
    "verification_status": "A. Directly verified classical reference"
  },
  {
    "id": 76,
    "classical_sanskrit_name": "Vacha (वचा)",
    "botanical_name": "Acorus calamus L.",
    "family": "Acoraceae (Araceae)",
    "english_common_name": "Sweet Flag / Calamus",
    "sanskrit_synonyms": ["Ugragandha (उग्रगन्धा)", "Shadgrantha (षड्ग्रन्था)", "Golomi (गोलोमी)", "Mangalya (मङ्गल्या)", "Jatila (जटिला)"],
    "useful_part": "Rhizome (Kanda)",
    "rasa": ["Katu", "Tikta"],
    "guna": ["Laghu", "Tikshna"],
    "virya": "Ushna",
    "vipaka": "Katu",
    "prabhava": "Medhya / Sanjnasthapana / Swarya (Agrya Sanjnasthapana Dravya)",
    "dosha_karma": "Kapha-Vatashamaka",
    "pharmacological_therapeutic_karma": ["Medhya", "Sanjnasthapana", "Swarya", "Vamana", "Deepana", "Pachana", "Kaphaghna", "Unmadahara"],
    "important_indications": ["Unmada (Psychosis / Mental confusion)", "Apasmara (Epilepsy)", "Swarabheda (Hoarseness of voice)", "Smritibhramsha (Memory impairment)", "Agnimandya (Loss of appetite)", "Vibandha (Constipation / Abdominal distension)"],
    "important_formulations": ["Saraswata Churna", "Vachadi Churna", "Brahmi Ghrita", "Sanjivani Vati", "Vachadi Taila"],
    "identification_characters": "Sub-cylindrical tortuous branched rhizomes marked with triangular leaf scars and rootlets, brownish exterior and whitish spongy interior, strong peculiar aromatic odor and warm pungent bitter taste.",
    "classical_shloka": "वचा उग्रा कटुका तिक्ता तीक्ष्णोष्णा वमनकृत् सरः।\nमेध्या वह्निकरः कण्ठ्या उन्मादापस्मारापहः॥",
    "shloka_source": {"text_grantha_name": "Bhavaprakasha Nighantu", "sthana_section": "Nighantu Sthana", "adhyaya": "N/A", "varga_chapter": "Haritakyadi Varga", "shloka_number": "Verse 102-103", "edition_publisher": "Chowkhamba Bharati Academy, Varanasi", "page_number": "Needs checking against physical copy for exact page"},
    "verification_status": "A. Directly verified classical reference"
  },
  {
    "id": 77,
    "classical_sanskrit_name": "Sarpagandha (सर्पगन्धा)",
    "botanical_name": "Rauvolfia serpentina (L.) Benth. ex Kurz",
    "family": "Apocynaceae",
    "english_common_name": "Serpentina Root / Snakeroot",
    "sanskrit_synonyms": ["Nakuli (नाकुली)", "Chandrika (चन्द्रिका)", "Sarpakshi (सर्पाक्षी)", "Dhavala (धवला)", "Bhujangakshi (भुजङ्गाक्षी)"],
    "useful_part": "Root (Mula)",
    "rasa": ["Tikta"],
    "guna": ["Ruksha"],
    "virya": "Ushna",
    "vipaka": "Katu",
    "prabhava": "Nidrajanana / Raktavatashamaka / Unmadahara",
    "dosha_karma": "Kapha-Vatashamaka (Reduces Vata & Pitta in Manovaha Srotas)",
    "pharmacological_therapeutic_karma": ["Nidrajanana", "Raktachapahara (Antihypertensive)", "Unmadahara", "Hrid-shamak", "Vishaghna", "Vedanasthapana", "Kamoddepaka"],
    "important_indications": ["Raktachapa (Hypertension / High blood pressure)", "Anidra (Insomnia / Sleep deprivation)", "Unmada (Mania / Severe anxiety / Agitation)", "Bhrama (Vertigo)", "Sarpa-visha (Snakebite / Envenomation)"],
    "important_formulations": ["Sarpagandha Churna", "Sarpagandha Vati", "Sarpagandhadi Churna", "Sarpagandha Ghrita"],
    "identification_characters": "Tapering tortuous cylindrical roots with pale greyish-brown corky bark bearing longitudinal fissures, bitter persistent taste, odorless.",
    "classical_shloka": "सर्पगन्धा तिक्तरसा रूक्षोष्णा कफवातहृत्।\nनिद्राप्रदा मदघ्नी च रक्तचापविनाशिनी॥",
    "shloka_source": {"text_grantha_name": "Dravyaguna Vigyan (P.V. Sharma)", "sthana_section": "Nighantu Sthana", "adhyaya": "N/A", "varga_chapter": "Modern Compilation Reference", "shloka_number": "N/A", "edition_publisher": "Chowkhamba Bharati Academy, Varanasi", "page_number": "Needs checking against physical copy for exact page"},
    "verification_status": "A. Directly verified classical reference"
  },
  {
    "id": 78,
    "classical_sanskrit_name": "Ativisha (अतिविषा)",
    "botanical_name": "Aconitum heterophyllum Wall. ex Royle",
    "family": "Ranunculaceae",
    "english_common_name": "Indian Atees",
    "sanskrit_synonyms": ["Shuklakanda (शुक्लकन्दा)", "Bhangura (भङ्गुरा)", "Vishva (विश्वा)", "Aruna (अरुणा)", "Shringi (शृङ्गी)"],
    "useful_part": "Tuberous Root (Kanda / Mula)",
    "rasa": ["Tikta", "Katu"],
    "guna": ["Laghu", "Ruksha"],
    "virya": "Ushna",
    "vipaka": "Katu",
    "prabhava": "Deepana / Pachana / Atisarahara / Bala-rogahara (Agrya Atisarahara in Children)",
    "dosha_karma": "Kapha-Pittashamaka",
    "pharmacological_therapeutic_karma": ["Deepana", "Pachana", "Grahi", "Amapachana", "Jwarahara", "Krimighna", "Vishaghna", "Atisarahara"],
    "important_indications": ["Atisara (Diarrhea / Pediatric diarrhea)", "Amaatisara (Dysentery / Infective diarrhea)", "Jwara (Fever / Intermittent fever)", "Agnimandya (Dyspepsia / Loss of appetite)", "Chhardi (Vomiting)", "Balaroga (Pediatric gastrointestinal disorders)"],
    "important_formulations": ["Balachaturbhadra Churna", "Ativishadi Churna", "Gangadhara Churna", "Kutajarishta", "Sudarshana Churna"],
    "identification_characters": "Ovoid or conical small tuberous roots (2-4 cm), light greyish-white chalky fracture, non-poisonous (nirvisha), pure intense bitter taste without numbness of tongue.",
    "classical_shloka": "अतिविषा कटुः तिक्ता उष्णोष्णा दीपनी परा।\nअतिसारज्वरच्छर्दिकफपित्तविषापहा॥",
    "shloka_source": {"text_grantha_name": "Bhavaprakasha Nighantu", "sthana_section": "Nighantu Sthana", "adhyaya": "N/A", "varga_chapter": "Haritakyadi Varga", "shloka_number": "Verse 153-154", "edition_publisher": "Chowkhamba Bharati Academy, Varanasi", "page_number": "Needs checking against physical copy for exact page"},
    "verification_status": "A. Directly verified classical reference"
  }
]

# Additional supplementary records retained from later Gemini batches. These are
# deliberately kept separate from the NCISM-97 student set.
SUPPLEMENTARY_META = [
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


def normalize_name(s):
    return str(s or '').strip().lower().replace('ā', 'a').replace('ī', 'i').replace('ū', 'u')


def find_master(plants, target):
    aliases = {
        'Jatamansi': ['jatamansi', 'jātamāṃsī'],
        'Vacha': ['vacha', 'vaca'],
        'Sarpagandha': ['sarpagandha'],
        'Ativisha': ['ativisha', 'ativisa'],
    }
    wanted = [normalize_name(target)] + [normalize_name(x) for x in aliases.get(target, [])]
    for p in plants:
        if normalize_name(p.get('identity', {}).get('name')) in wanted:
            return p
    return None


def merge_full_gemini(p, g, supplementary=False):
    if supplementary:
        p['category'] = 'Supplementary'
        p['syllabus_marker'] = 'Supplementary'
    else:
        p['category'] = 'NCISM-97'
        p['syllabus_marker'] = 'NCISM-97'

    ident = p.setdefault('identity', {})
    ident['botanical_name'] = g['botanical_name']
    ident['family'] = g['family']
    ident['english_name'] = g['english_common_name']
    ident['sanskrit_name'] = g['classical_sanskrit_name'].split(' (')[0]
    ident['synonyms'] = g['sanskrit_synonyms']

    dg = p.setdefault('dravya_guna', {})
    dg['rasa'] = [x.lower() for x in g['rasa']]
    dg['guna'] = [x.lower() for x in g['guna']]
    dg['virya'] = g['virya'].lower()
    dg['vipaka'] = g['vipaka'].lower()
    dg['prabhava'] = g['prabhava']
    dg['karma'] = g['pharmacological_therapeutic_karma']

    dosha = p.setdefault('dosha', {})
    dosha['summary'] = g['dosha_karma']

    ident_section = p.setdefault('identification', {})
    ident_section['description'] = g['identification_characters']
    ident_section['identification_points'] = [g['identification_characters']]

    th = p.setdefault('therapeutics', {})
    th['useful_part'] = [g['useful_part']]
    th['indications'] = g['important_indications']
    th['therapeutic_actions'] = g['pharmacological_therapeutic_karma']

    p['formulations'] = [{'name': x, 'dosage_form': '', 'indication': '', 'reference': ''} for x in g['important_formulations']]

    cr = p.setdefault('classical_reference', {})
    cr['shlokas'] = [g['classical_shloka']]
    cr['nighantu_references'] = [f"{g['shloka_source']['text_grantha_name']}, {g['shloka_source']['varga_chapter']}, {g['shloka_source']['shloka_number']}"]
    cr['shloka_reference_status'] = g['verification_status']
    cr['gemini_source_reference'] = g['shloka_source']

    p.setdefault('teacher', {}).setdefault('discussion_points', []).append(f"Full Gemini batch {g['id']} record merged; source object retained verbatim under gemini_source_data.")
    p.setdefault('metadata', {})['gemini_later_batches_reviewed'] = True
    p['metadata']['gemini_source_batches'] = sorted(set(p['metadata'].get('gemini_source_batches', []) + [g['id']]))
    p['gemini_source_data'] = g
    return p


plants = json.loads(DATA.read_text(encoding='utf-8'))

# Merge full records 75-78 into their existing NCISM masters.
for g in GEMINI_74_78:
    name = g['classical_sanskrit_name'].split(' (')[0]
    if name == 'Karpura':
        existing = next((p for p in plants if normalize_name(p.get('identity', {}).get('name')) == 'karpura'), None)
        if existing is None:
            existing = supplementary_record(('karpura', 'Karpura', 'कर्पूर', g['botanical_name'], g['family'], g['english_common_name'], 'Gemini batch 74'))
            plants.append(existing)
        merge_full_gemini(existing, g, supplementary=True)
    else:
        master = find_master(plants, name)
        if master is None:
            raise KeyError(f'Expected NCISM master record not found for Gemini batch {g["id"]}: {name}')
        merge_full_gemini(master, g, supplementary=False)

# Keep the other useful non-NCISM drugs as supplementary records.
for item in SUPPLEMENTARY_META:
    pid = item[0]
    existing = next((p for p in plants if p.get('id') == pid), None)
    if existing is None:
        plants.append(supplementary_record(item))

# Mark all syllabus records explicitly and preserve exactly one master per name/id.
for p in plants:
    if isinstance(p.get('order'), int) and 1 <= p['order'] <= 97:
        p['category'] = 'NCISM-97'
        p['syllabus_marker'] = 'NCISM-97'

seen_ids, seen_names, out = set(), set(), []
for p in plants:
    pid = str(p.get('id', '')).strip().lower()
    nm = str(p.get('identity', {}).get('name', '')).strip().lower()
    if not pid or pid in seen_ids or (nm and nm in seen_names):
        continue
    seen_ids.add(pid)
    if nm:
        seen_names.add(nm)
    out.append(p)

out.sort(key=lambda p: (0 if p.get('category') == 'NCISM-97' else 1, p.get('order') if isinstance(p.get('order'), int) else 9999, str(p.get('identity', {}).get('name', ''))))
assert sum(1 for p in out if p.get('category') == 'NCISM-97') == 97
assert any(p.get('id') == 'karpura' and p.get('gemini_source_data', {}).get('id') == 74 for p in out)
for expected in [75, 76, 77, 78]:
    assert any(p.get('gemini_source_data', {}).get('id') == expected for p in out)

DATA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Uploaded full Gemini batches 74-78: 97 NCISM-97 master records + {len(out)-97} supplementary records; no duplicate masters created.')
