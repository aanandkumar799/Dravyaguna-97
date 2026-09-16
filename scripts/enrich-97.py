import json
import re
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'plants.json'
IMG = ROOT / 'images' / 'plants'
IMG.mkdir(parents=True, exist_ok=True)

WIKI_API = 'https://commons.wikimedia.org/w/api.php'
HERB_DATA = 'https://raw.githubusercontent.com/sciencewithsaucee-sudo/herb-database/main/herb.json'
USER_AGENT = 'Dravyaguna97/1.3 educational database'


def get_json(url, timeout=30):
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def download(url, path):
    req = Request(url, headers={'User-Agent': USER_AGENT})
    with urlopen(req, timeout=30) as r:
        data = r.read()
    if len(data) < 1000:
        return False
    path.write_bytes(data)
    return True


def slug(value):
    return re.sub(r'[^a-z0-9_-]+', '-', value.lower()).strip('-')


def norm(value):
    return re.sub(r'[^a-z0-9]+', '', str(value).lower())


def first_two_botanical(value):
    parts = re.sub(r'[^A-Za-z]+', ' ', str(value)).lower().split()
    return ' '.join(parts[:2]) if len(parts) >= 2 else ''


def empty(value):
    return value is None or value == '' or value == [] or value == {}


def merge_external(p, ext):
    identity = p.setdefault('identity', {})
    dg = p.setdefault('dravya_guna', {})
    therapy = p.setdefault('therapeutics', {})
    dosha = p.setdefault('dosha', {})
    student = p.setdefault('student', {})
    modern = p.setdefault('modern_information', {})

    for dst, src in [('botanical_name','botanical_name'), ('family','family'), ('english_name','english_name')]:
        if empty(identity.get(dst)) and ext.get(src):
            identity[dst] = ext[src]
    if empty(identity.get('synonyms')) and ext.get('sanskrit_synonyms'):
        identity['synonyms'] = ext['sanskrit_synonyms']
    if empty(therapy.get('useful_part')) and ext.get('part_used'):
        therapy['useful_part'] = ext['part_used']
    if empty(therapy.get('indications')) and ext.get('main_indications'):
        therapy['indications'] = ext['main_indications']
    for dst, src in [('rasa','rasa'), ('guna','guna'), ('virya','virya'), ('vipaka','vipaka'), ('prabhava','prabhav')]:
        if empty(dg.get(dst)) and ext.get(src):
            dg[dst] = ext[src]
    if empty(student.get('quick_revision')) and ext.get('preview'):
        student['quick_revision'] = ext['preview']
    if empty(modern.get('evidence_summary')) and ext.get('preview'):
        modern['evidence_summary'] = ext['preview']
    pacify = [str(x).lower() for x in ext.get('pacify', [])]
    aggravate = [str(x).lower() for x in ext.get('aggravate', [])]
    for dosha_name in ('vata','pitta','kapha'):
        if empty(dosha.get(dosha_name)):
            if dosha_name in pacify:
                dosha[dosha_name] = 'pacified'
            elif dosha_name in aggravate:
                dosha[dosha_name] = 'aggravated'
            else:
                dosha[dosha_name] = 'not specifically documented in imported dataset'


# Curated user-supplied data, with classical quotations corrected against
# searchable Bhavaprakasha text where independently verified. These patches
# intentionally overwrite the corresponding fields so the website reflects
# the reviewed batch rather than the unverified Gemini wording.
CURATED = {
    'Haridra': {
        'botanical_name': 'Curcuma longa L.', 'family': 'Zingiberaceae', 'english_name': 'Turmeric',
        'synonyms': ['Kanchani', 'Nisha', 'Gauri', 'Krimighni', 'Varavarnini'],
        'useful_part': ['rhizome'], 'rasa': ['tikta', 'katu'], 'guna': ['ruksha', 'laghu'],
        'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Varnya / Vishaghna / Pramehara',
        'dosha_karma': 'Kapha-Pittashamaka',
        'therapeutic_actions': ['Varnya', 'Krimighna', 'Kushtaghna', 'Vishaghna', 'Pramehara', 'Vranaropana', 'Raktashodhaka'],
        'indications': ['Prameha', 'Kushta', 'Pandu', 'Vrana', 'Sheetapitta', 'Pratishyaya'],
        'formulations': ['Haridra Khanda', 'Nisha Amalaki Churna', 'Haridradi Ghrita', 'Nimbadi Churna'],
        'identification': 'Primary ovate or secondary cylindrical branched rhizomes, deep orange-yellow interior, characteristic strong aromatic odor, bitter and pungent taste.',
        'shloka': 'हरिद्रा काञ्चनी पीता निशाख्या वरवर्णिनी ।\nकृमिघ्ना हलदी योषित्प्रिया हट्टविलासिनी ॥१९६॥\nहरिद्रा कटुका तिक्ता रूक्षोष्णा कफपित्तनुत् ।\nवर्ण्या त्वग्दोषमेहास्रशोथपाण्डुव्रणापहा ॥१९७॥',
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 196–197 (numbering of searchable recension; edition numbering may vary).',
        'status': 'verified_reference_text_corrected'
    },
    'Aragwadha': {
        'botanical_name': 'Cassia fistula L.', 'family': 'Fabaceae (Caesalpiniaceae)', 'english_name': 'Golden shower tree / Purging cassia',
        'synonyms': ['Rajavriksha', 'Shampaka', 'Chaturangula', 'Kritamala', 'Vyadhighata'],
        'useful_part': ['fruit pulp', 'stem bark'], 'rasa': ['madhura'], 'guna': ['guru', 'mridu', 'snigdha'],
        'virya': 'sheeta', 'vipaka': 'madhura', 'prabhava': 'Mridu Virechana / Sramsana',
        'dosha_karma': 'Kapha-Pittashamaka',
        'therapeutic_actions': ['Mridu Virechana', 'Sramsana', 'Kushtaghna', 'Jwarahara', 'Hridya', 'Kandughna'],
        'indications': ['Vibandha', 'Kushta', 'Jwara', 'Hridroga', 'Udarashula'],
        'formulations': ['Aragvadharishta', 'Aragvadhadi Kwatha', 'Aragvadhadi Leha', 'Maha Manjisthadi Kwatha'],
        'identification': 'Long cylindrical pendulous dark brown pods with transverse septa and one-seeded compartments containing sticky dark pulp.',
        'shloka': 'कर्णिकारो दीर्घफलः स्वर्णाङ्गः स्वर्णभूषणः ।\nआरग्वधो गुरुः स्वादुः शीतलः स्रंसनोत्तमः ॥१४९॥\nज्वरहृद्रोगपित्तास्रवातोदावर्त्तशूलनुत् ।\nतत्फलं स्रंसनं रुच्यं कुष्ठपित्तकफापहम् ॥१५०॥\nज्वरे तु सततं पथ्यं कोष्ठशुद्धिकरं परम् ॥१५१॥',
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 149–151.',
        'status': 'verified_reference_text_corrected'
    },
    'Katuki': {
        'botanical_name': 'Picrorhiza kurroa Royle ex Benth.', 'family': 'Plantaginaceae (Scrophulariaceae)', 'english_name': 'Picrorhiza / Kutki',
        'synonyms': ['Tikta', 'Katurohini', 'Matsyashakala', 'Chakrangi', 'Shataparva'],
        'useful_part': ['rhizome', 'root'], 'rasa': ['tikta'], 'guna': ['laghu', 'ruksha'],
        'virya': 'sheeta', 'vipaka': 'katu', 'prabhava': 'Bhedana', 'dosha_karma': 'Kapha-Pittashamaka',
        'therapeutic_actions': ['Bhedana', 'Deepana', 'Pachana', 'Jwarahara', 'Kamalahara', 'Hridya'],
        'indications': ['Kamala', 'Jwara', 'Kushta', 'Prameha', 'Vibandha'],
        'formulations': ['Arogyavardhini Vati', 'Katutrayadi Kwatha', 'Katukadi Churna', 'Mahatiktaka Ghrita'],
        'identification': 'Cylindrical greyish-brown rhizomes with dark scale-leaf crowns and root scars; intensely bitter persistent taste.',
        'shloka': 'कट्वी तु कटुका तिक्ता कृष्णभेदा कटम्भरा ।\nअशोका मत्स्यशकला चक्राङ्गी शकुलादनी ।\nमत्स्यपित्ता काण्डरुहा रोहिणी कटुरोहिणी ॥१५२॥\nकट्वी तु कटुका पाके तिक्ता रूक्षा हिमा लघुः ।\nभेदिनी दीपनी हृद्या कफपित्तज्वरापहा ।\nप्रमेहश्वासकासास्रदाहकुष्ठकृमिप्रणुत् ॥१५३॥',
        'reference': 'Bhavaprakasha Nighantu, Haritakyadi Varga, verses 152–153.',
        'status': 'verified_reference_text_corrected'
    },
    'Trivrit': {
        'botanical_name': 'Operculina turpethum (L.) Silva Manso', 'family': 'Convolvulaceae', 'english_name': 'Indian jalap / Turpeth',
        'synonyms': ['Triputa', 'Sarala', 'Nishotra', 'Kumbha', 'Kuta'],
        'useful_part': ['root bark'], 'rasa': ['tikta', 'katu'], 'guna': ['laghu', 'ruksha', 'tikshna'],
        'virya': 'ushna', 'vipaka': 'katu', 'prabhava': 'Sukha-Virechana', 'dosha_karma': 'Kapha-Pitta shamaka; Vata may be affected depending on form/dose',
        'therapeutic_actions': ['Virechana', 'Sukha-Virechana', 'Kaphahara', 'Pittahara', 'Shothahara'],
        'indications': ['Vibandha', 'Udara Roga', 'Shotha', 'Arsha', 'Pandu'],
        'formulations': ['Avipattikara Churna', 'Trivrit Lehyam', 'Trivritadi Kwatha', 'Abhayarishta'],
        'identification': 'Long fleshy roots with separable outer bark and central woody core; longitudinally furrowed dark reddish-brown surface and bitter taste.',
        'shloka': 'श्वेतात्रिवृता भण्डी स्यात् त्रिवृता त्रिपुटापि च ।\nसर्वानुभूतिः सरला निशोत्रा रेचनीति च ॥१६५॥\nश्वेता त्रिवृद्रेचनी स्यात्स्वादुरुष्णा समीरहृत् ।\nरूक्षा पित्तज्वरश्लेष्मपित्तशोथोदरापहा ॥१६६॥',
        'reference': 'Bhavaprakasha Nighantu, Guduchyadi Varga, verses 165–166.',
        'status': 'verified_reference_text_corrected'
    },
    'Kumari': {
        'botanical_name': 'Aloe vera (L.) Burm.f. (syn. Aloe barbadensis Mill.)', 'family': 'Asphodelaceae (Liliaceae)', 'english_name': 'Indian aloe / Aloe vera',
        'synonyms': ['Kanya', 'Grihakanya', 'Tarani', 'Vipulasrava'],
        'useful_part': ['leaf pulp/gel', 'dried leaf juice (Kumari sara/Elua)'], 'rasa': ['tikta', 'madhura'],
        'guna': ['guru', 'snigdha', 'picchila'], 'virya': 'sheeta', 'vipaka': 'madhura',
        'prabhava': 'Bhedana / Artavajanana / Rasayana', 'dosha_karma': 'Vata-Pitta shamaka; classical use includes Vata- and Vishaghna actions',
        'therapeutic_actions': ['Bhedana', 'Brimhana', 'Vrishya', 'Rasayana', 'Artavajanana', 'Yakrit-Pliha supportive use', 'Chakshushya'],
        'indications': ['Artavadosha / Rajorodha', 'Yakrit-Pliha roga', 'Gulma', 'Vrana', 'Kushta'],
        'formulations': ['Kumariasava', 'Rajapravartini Vati', 'Kumari Ghrita', 'Kumari Taila'],
        'identification': 'Sessile rosette succulent with thick fleshy lanceolate leaves, spiny margins and abundant translucent mucilaginous gel with bitter yellow exudate.',
        'shloka': 'कुमारी गृहकन्या च कन्या घृतकुमारिका ।\nकुमारी भेदनी शीता तिक्ता नेत्र्या रसायनी ॥२२९॥\nमधुरा बृंहणी बल्या वृष्या वातविषप्रणुत् ।\nगुल्मप्लीहयकृद्वृद्धिकफज्वरहरी हरेत् ।\nग्रन्थ्यग्निदग्धविस्फोटपित्तरक्तत्वगामयान् ॥२३०॥',
        'reference': 'Bhavaprakasha Nighantu, Guduchyadi Varga, verses 229–230.',
        'status': 'verified_reference_text_corrected'
    }
}


def apply_curated(p):
    name = p.get('identity', {}).get('name', '')
    patch = CURATED.get(name)
    if not patch:
        return
    identity = p.setdefault('identity', {})
    dg = p.setdefault('dravya_guna', {})
    therapy = p.setdefault('therapeutics', {})
    dosha = p.setdefault('dosha', {})
    classical = p.setdefault('classical_reference', {})
    student = p.setdefault('student', {})
    modern = p.setdefault('modern_information', {})

    for key in ('botanical_name', 'family', 'english_name', 'synonyms'):
        if key in patch:
            identity[key] = patch[key]
    if 'identification' in patch:
        p.setdefault('identification', {})['description'] = patch['identification']
    for key in ('rasa', 'guna', 'virya', 'vipaka', 'prabhava'):
        if key in patch:
            dg[key] = patch[key]
    if 'useful_part' in patch:
        therapy['useful_part'] = patch['useful_part']
    if 'therapeutic_actions' in patch:
        therapy['therapeutic_actions'] = patch['therapeutic_actions']
    if 'indications' in patch:
        therapy['indications'] = patch['indications']
    if 'dosha_karma' in patch:
        p.setdefault('metadata', {})['dosha_karma_note'] = patch['dosha_karma']
    if 'formulations' in patch:
        p['formulations'] = [{'name': x, 'dosage_form': '', 'indication': '', 'reference': ''} for x in patch['formulations']]
    classical['shlokas'] = [patch['shloka']]
    classical['nighantu_references'] = [patch['reference']]
    classical['shloka_reference_status'] = patch['status']
    classical['reference_hubs'] = classical.get('reference_hubs', [])
    if 'TDU Indian Medicinal Plants Database — Shlokas' not in classical['reference_hubs']:
        classical['reference_hubs'].append('TDU Indian Medicinal Plants Database — Shlokas')
    p.setdefault('metadata', {})['status'] = patch['status']
    p['metadata']['version'] = '1.3'
    student['quick_revision'] = f"{name}: curated batch data added; classical reference reviewed against searchable Bhavaprakasha text."
    modern['evidence_summary'] = modern.get('evidence_summary') or 'Classical Ayurvedic drug profile; modern evidence should be interpreted separately from classical claims.'


plants = json.loads(DATA.read_text(encoding='utf-8'))
try:
    external = get_json(HERB_DATA, timeout=45)
except Exception as exc:
    external = []
    print('External herb dataset unavailable:', exc)

by_name = {}
by_botanical = {}
for h in external if isinstance(external, list) else []:
    if h.get('name'):
        by_name[norm(h['name'])] = h
    if h.get('botanical_name'):
        by_botanical[first_two_botanical(h['botanical_name'])] = h

for p in plants:
    identity = p.setdefault('identity', {})
    images = p.setdefault('images', {})
    sources = p.setdefault('sources', [])
    classical = p.setdefault('classical_reference', {})

    ext = by_name.get(norm(identity.get('name', '')))
    botanical = identity.get('botanical_name', '').strip()
    if not ext and botanical:
        ext = by_botanical.get(first_two_botanical(botanical))
    if not ext:
        ext = by_name.get(norm(p.get('id', '')))
    if ext:
        merge_external(p, ext)
        if not any(s.get('type') == 'open_ayurveda_dataset' for s in sources):
            sources.append({'type': 'open_ayurveda_dataset', 'title': 'Amidha Ayurveda Herb Database v2.0', 'url': 'https://github.com/sciencewithsaucee-sudo/herb-database', 'license': 'CC BY 4.0', 'note': 'Used only to populate blank structured fields; verify against classical editions before clinical or textual claims.'})

    apply_curated(p)

    botanical = identity.get('botanical_name', '').strip()
    common = identity.get('english_name') or identity.get('name') or p.get('id', '')
    query = botanical or common
    if query and not images.get('whole_plant'):
        try:
            params = ('?action=query&generator=search&gsrsearch=' + quote(query) + '&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=900&format=json')
            result = get_json(WIKI_API + params)
            pages = list((result.get('query') or {}).get('pages', {}).values())
            chosen = None
            for page in pages:
                info = (page.get('imageinfo') or [{}])[0]
                mime = info.get('mime', '')
                title = page.get('title', '').lower()
                if mime.startswith('image/') and not any(x in title for x in ('map','distribution','icon','logo')):
                    chosen = info
                    break
            if chosen:
                extn = '.jpg' if 'jpeg' in chosen.get('mime', '') else '.png'
                local = IMG / (slug(p.get('id', common)) + extn)
                if not local.exists() and chosen.get('thumburl'):
                    download(chosen['thumburl'], local)
                if local.exists():
                    images['whole_plant'] = 'images/plants/' + local.name
                    images['habit'] = images['whole_plant']
                    sources.append({'type':'image','title':'Wikimedia Commons','url':chosen.get('descriptionurl','https://commons.wikimedia.org/'),'license_note':'Check the original file page for current license/attribution requirements.'})
        except Exception as exc:
            p.setdefault('metadata', {})['image_enrichment_note'] = str(exc)[:200]

    if not any(s.get('type') == 'tdu_classical_database' for s in sources):
        sources.append({'type':'tdu_classical_database','title':'TDU Indian Medicinal Plants Database — Ayurvedic identity and Shlokas','url':'https://www.tdu.edu.in/outreach/indian-medicinal-plants-database','note':'Use the Shlokas module to verify exact Devanagari verse and edition/page before treating a verse as a quotation.'})
    classical.setdefault('reference_hubs', [])
    if not any('TDU' in x for x in classical['reference_hubs']):
        classical['reference_hubs'].append('TDU Indian Medicinal Plants Database — Shlokas')
    p.setdefault('metadata', {})['last_enrichment'] = 'structured-field + image + reference enrichment + curated batch'
    time.sleep(0.03)

DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Enriched {len(plants)} records with structured fields, images, reference hubs and curated data')
