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
USER_AGENT = 'Dravyaguna97/1.2 educational database'


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
            sources.append({
                'type': 'open_ayurveda_dataset',
                'title': 'Amidha Ayurveda Herb Database v2.0',
                'url': 'https://github.com/sciencewithsaucee-sudo/herb-database',
                'license': 'CC BY 4.0',
                'note': 'Used only to populate blank structured fields; verify against classical editions before clinical or textual claims.'
            })

    botanical = identity.get('botanical_name', '').strip()
    common = identity.get('english_name') or identity.get('name') or p.get('id', '')
    query = botanical or common
    if query and not images.get('whole_plant'):
        try:
            params = ('?action=query&generator=search&gsrsearch=' + quote(query) +
                      '&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=900&format=json')
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
    classical.setdefault('shloka_reference_status','source-hub-added; exact verse/edition requires text-level verification')
    classical.setdefault('reference_hubs', [])
    if not any('TDU' in x for x in classical['reference_hubs']):
        classical['reference_hubs'].append('TDU Indian Medicinal Plants Database — Shlokas')
    p.setdefault('metadata', {})['last_enrichment'] = 'structured-field + image + reference enrichment'
    p['metadata']['version'] = '1.2'
    time.sleep(0.03)

DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Enriched {len(plants)} records with structured fields, images and reference hubs')
