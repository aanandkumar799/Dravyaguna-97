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
USER_AGENT = 'Dravyaguna97/1.0 educational database'


def get_json(url):
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urlopen(req, timeout=20) as r:
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

plants = json.loads(DATA.read_text(encoding='utf-8'))
for p in plants:
    identity = p.setdefault('identity', {})
    images = p.setdefault('images', {})
    sources = p.setdefault('sources', [])
    classical = p.setdefault('classical_reference', {})

    botanical = identity.get('botanical_name', '').strip()
    common = identity.get('english_name') or identity.get('name') or p.get('id', '')
    query = botanical or common

    # 1) Find an openly licensed Wikimedia Commons image for plant identification.
    if query and not images.get('whole_plant'):
        try:
            params = (
                '?action=query&generator=search&gsrsearch=' + quote(query) +
                '&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=900&format=json'
            )
            result = get_json(WIKI_API + params)
            pages = list((result.get('query') or {}).get('pages', {}).values())
            chosen = None
            for page in pages:
                info = (page.get('imageinfo') or [{}])[0]
                mime = info.get('mime', '')
                title = page.get('title', '').lower()
                if mime.startswith('image/') and not any(x in title for x in ('map', 'distribution', 'icon', 'logo')):
                    chosen = info
                    break
            if chosen:
                ext = '.jpg' if 'jpeg' in chosen.get('mime', '') else '.png'
                local = IMG / (slug(p.get('id', common)) + ext)
                if not local.exists() and chosen.get('thumburl'):
                    download(chosen['thumburl'], local)
                if local.exists():
                    images['whole_plant'] = 'images/plants/' + local.name
                    images['habit'] = images['whole_plant']
                    sources.append({
                        'type': 'image',
                        'title': 'Wikimedia Commons',
                        'url': chosen.get('descriptionurl', 'https://commons.wikimedia.org/'),
                        'license_note': 'Check the original file page for current license/attribution requirements.'
                    })
        except Exception as exc:
            p.setdefault('metadata', {})['image_enrichment_note'] = str(exc)[:200]

    # 2) Add authoritative reference hubs without inventing verse numbers.
    if not any(s.get('type') == 'tdu_classical_database' for s in sources):
        sources.append({
            'type': 'tdu_classical_database',
            'title': 'TDU Indian Medicinal Plants Database — Ayurvedic identity and Shlokas',
            'url': 'https://www.tdu.edu.in/outreach/indian-medicinal-plants-database',
            'note': 'Use the database Shlokas module to verify the exact Devanagari verse and edition/page before treating a verse as a quotation.'
        })
    classical.setdefault('shloka_reference_status', 'source-hub-added; exact verse/edition requires text-level verification')
    classical.setdefault('reference_hubs', [])
    if not any('TDU' in x for x in classical['reference_hubs']):
        classical['reference_hubs'].append('TDU Indian Medicinal Plants Database — Shlokas')

    p.setdefault('metadata', {})['last_enrichment'] = 'automated image/reference enrichment'
    p['metadata']['version'] = '1.1'
    time.sleep(0.05)

DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Enriched {len(plants)} records; image assets stored in {IMG.relative_to(ROOT)}')
