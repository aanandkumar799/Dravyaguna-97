import json, re, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'plant-index.json'
PLANTS_DIR = ROOT / 'data' / 'plants'
MANIFEST = ROOT / 'data' / 'curated-image-manifest.json'
REPORT = ROOT / 'data' / 'image-audit-report.json'
IMAGE_ROOT = ROOT / 'images' / 'plants'
PARTS = ['whole_plant','habit','root','stem','leaf','flower','fruit','seed','bark']
PART_WORDS = {'root':['root','roots'],'stem':['stem','stems','twig','twigs'],'leaf':['leaf','leaves','foliage'],'flower':['flower','flowers','inflorescence','blossom'],'fruit':['fruit','fruits','pod','pods','berry','berries','capsule'],'seed':['seed','seeds','nut','nuts'],'bark':['bark','trunk','trunks'],'whole_plant':['whole plant','entire plant','plant specimen'],'habit':['habit','growth form','tree','shrub','herb','climber','vine']}
PART_EXCLUDE = {'whole_plant':['leaf','flower','fruit','seed','root','bark','stem','twig','trunk'],'habit':['leaf','flower','fruit','seed','root','bark','stem','twig','trunk']}
BAD = re.compile(r'\b(diagram|map|microscope|illustration|drawing|icon|logo|chart|anatomy|cross[- ]section|histology|chemical|medicine|tablet|capsule|powder|poster|herbarium\s+sheet)\b', re.I)
LICENSE_OK = re.compile(r'^(cc\s*by(?:-sa)?(?:\s*\d(?:\.\d)?)?|cc0|public domain|pd|pdm)$', re.I)


def fetch_json(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent':'Dravyaguna-97-image-auditor/4.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()


def species_tokens(botanical):
    return [x for x in re.findall(r'[a-z]{3,}', norm(botanical))[:2]]


def exact_species(title, botanical):
    low = norm(title).split(); tk = species_tokens(botanical)
    return len(tk) == 2 and all(t in low for t in tk)


def part_ok(title, part):
    low = norm(title)
    if BAD.search(title):
        return False
    if part in PART_EXCLUDE:
        return not any(w in low.split() for w in PART_EXCLUDE[part])
    return any(norm(w) in low.split() for w in PART_WORDS.get(part, []))


def commons_candidates(botanical, part):
    query = f'"{botanical}" ' + ('whole plant' if part == 'whole_plant' else 'habit growth form' if part == 'habit' else part)
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':40,
        'prop':'imageinfo','iiprop':'url|extmetadata|mime','iiurlwidth':1600,'format':'json','origin':'*'
    })
    data = fetch_json(url); out = []
    for p in (data.get('query', {}).get('pages', {}) or {}).values():
        info = (p.get('imageinfo') or [{}])[0]
        title = str(p.get('title') or '')
        mime = str(info.get('mime') or '')
        lic = str((info.get('extmetadata') or {}).get('LicenseShortName', {}).get('value') or '').strip()
        if mime not in ('image/jpeg','image/png','image/webp') or not LICENSE_OK.search(re.sub(r'\s+',' ',lic)):
            continue
        if not exact_species(title, botanical) or not part_ok(title, part):
            continue
        u = info.get('thumburl') or info.get('url')
        if u:
            out.append({
                'url':u,
                'page':'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ','_')),
                'title':title.replace('File:','',1),
                'license':lic,
                'author':str((info.get('extmetadata') or {}).get('Artist',{}).get('value') or '').strip(),
                'source':'Wikimedia Commons'
            })
    return out


def local_path(pid, part, ext='jpg'):
    return IMAGE_ROOT / pid / part / f'image.{ext}'


def download_image(url, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent':'Dravyaguna-97-image-auditor/4.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
        content_type = str(r.headers.get_content_type() or '')
    if content_type not in ('image/jpeg','image/png','image/webp') or len(data) < 2048:
        raise ValueError(f'unsupported or empty image response: {content_type}, {len(data)} bytes')
    ext = {'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[content_type]
    final = destination.with_suffix('.' + ext)
    final.write_bytes(data)
    return final.relative_to(ROOT).as_posix(), len(data)


def materialize_record(r):
    src = str(r.get('image_path') or '')
    if src.startswith('images/plants/'):
        path = ROOT / src
        if path.exists() and path.stat().st_size > 2048:
            return src, 0
        src = str(r.get('source_media_url') or r.get('source_download_url') or '')
    if not src.startswith('http'):
        return '', 0
    return download_image(src, local_path(str(r['plant_id']), str(r['part'])))


def main():
    idx = json.loads(INDEX.read_text(encoding='utf-8'))
    old = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {'version':3,'records':[]}
    if int(old.get('version',0) or 0) < 3:
        old['records'] = []
    manifest = old
    records = manifest.setdefault('records', [])
    by_key = {(str(r.get('plant_id')),str(r.get('part'))):r for r in records}
    core = sorted([x for x in idx.get('plants',[]) if x.get('category')=='NCISM-97' and 1<=int(x.get('order',0) or 0)<=97], key=lambda x:int(x['order']))
    changed = False; filled = []; unresolved = []; used_sources = set(); used_local = set()
    for r in records:
        if r.get('source_url') and r.get('verification_status') in ('verified','verified-external','verified-local'):
            used_sources.add(str(r['source_url']))
        if r.get('image_path') and str(r['image_path']).startswith('images/plants/'):
            used_local.add(str(r['image_path']))

    for ref in core:
        pid = str(ref.get('id')); fp = PLANTS_DIR / f'{pid}.json'
        p = json.loads(fp.read_text(encoding='utf-8')) if fp.exists() else {}
        botanical = str((p.get('identity') or {}).get('botanical_name') or ref.get('botanical_name') or '').strip()
        for part in PARTS:
            r = by_key.get((pid,part))
            if not r:
                r = {'plant_id':pid,'ncism_order':ref.get('order'),'plant_name':ref.get('name'),'botanical_name':botanical,'part':part,'image_path':'','source_url':'','source_name':'','license':'','author':'','verified_botanical_name':'','verification_status':'missing-queued'}
                records.append(r); by_key[(pid,part)] = r; changed = True
            # Convert previously verified external images to local files first.
            if r.get('verification_status') in ('verified','verified-external') and r.get('image_path'):
                try:
                    old_url = str(r['image_path'])
                    if old_url.startswith('http'):
                        local, size = materialize_record(r)
                        if local:
                            r['source_media_url'] = old_url
                            r['image_path'] = local
                            r['verification_status'] = 'verified-local'
                            used_local.add(local); changed = True
                            filled.append({'plant_id':pid,'part':part,'action':'downloaded-approved-image','path':local,'bytes':size})
                    elif old_url.startswith('images/plants/') and (ROOT / old_url).exists():
                        r['verification_status'] = 'verified-local'; changed = True
                    continue
                except Exception as e:
                    unresolved.append({'plant_id':pid,'part':part,'reason':'download-failed','detail':str(e)})
                    r['image_path'] = ''
                    r['verification_status'] = 'download-failed'
                    changed = True
            if r.get('verification_status') == 'verified-local' and r.get('image_path'):
                if (ROOT / str(r['image_path'])).exists():
                    continue
            try:
                candidates = commons_candidates(botanical,part)
            except Exception as e:
                unresolved.append({'plant_id':pid,'part':part,'reason':'source-check-error','detail':str(e)}); continue
            best = next((x for x in candidates if x['page'] not in used_sources and x['url'] not in used_sources), None)
            if not best:
                unresolved.append({'plant_id':pid,'part':part,'reason':'no-high-confidence-unique-image'}); continue
            try:
                local, size = download_image(best['url'], local_path(pid,part))
            except Exception as e:
                unresolved.append({'plant_id':pid,'part':part,'reason':'download-failed','detail':str(e)}); continue
            used_sources.add(best['page']); used_sources.add(best['url']); used_local.add(local)
            r.update({'image_path':local,'source_media_url':best['url'],'source_url':best['page'],'source_name':best['source'],'license':best['license'],'author':best['author'],'verified_botanical_name':botanical,'verification_status':'verified-local','title':best['title']})
            changed = True; filled.append({'plant_id':pid,'part':part,'action':'downloaded-new-image','path':local,'bytes':size})

    # Rebuild the registry and reject duplicate source files or source pages.
    seen = {}; duplicates = []
    for r in records:
        key = str(r.get('source_url') or r.get('source_media_url') or '')
        if key: seen.setdefault(key, []).append((r.get('plant_id'),r.get('part')))
    for key, slots in seen.items():
        if len(slots) > 1:
            duplicates.append({'source':key,'slots':slots})
            for pid, part in slots[1:]:
                rr = by_key[(str(pid),str(part))]
                rr.update({'image_path':'','source_media_url':'','source_url':'','source_name':'','license':'','author':'','verification_status':'duplicate-rejected'}); changed = True

    manifest['version'] = 4
    manifest['parts'] = PARTS
    manifest['policy'] = {'exact_species_required':True,'part_specific_required':True,'source_license_required':True,'global_duplicates_forbidden':True,'ai_only_matches_forbidden':True,'wrong_image_preferred_over_missing':False,'old_registry_reverification_required':True,'local_assets_required':True}
    manifest['records'] = sorted(records, key=lambda r:(int(r.get('ncism_order') or 9999), PARTS.index(r.get('part')) if r.get('part') in PARTS else 99))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    remaining = sum(1 for r in manifest['records'] if not r.get('image_path') or r.get('verification_status') != 'verified-local')
    report = {'generated_at':datetime.now(timezone.utc).isoformat(),'plants_checked':len(core),'slots_checked':len(core)*len(PARTS),'filled_this_run':filled,'unresolved':unresolved,'duplicate_conflicts':duplicates,'remaining_missing':remaining,'local_asset_root':'images/plants/<plant>/<part>/image.*','policy':manifest['policy']}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'changed':changed,'filled':len(filled),'remaining_missing':remaining,'duplicate_conflicts':len(duplicates)},indent=2))

if __name__=='__main__':
    main()
