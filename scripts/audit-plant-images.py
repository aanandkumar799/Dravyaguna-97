import json, re, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'plant-index.json'
PLANTS = ROOT / 'plants.json'
MANIFEST = ROOT / 'data' / 'curated-image-manifest.json'
REPORT = ROOT / 'data' / 'image-audit-report.json'
PARTS = ['whole_plant','habit','root','stem','leaf','flower','fruit','seed','bark']
PART_WORDS = {
 'root': ['root','roots'], 'stem':['stem','stems','twig','twigs'],
 'leaf':['leaf','leaves','foliage'], 'flower':['flower','flowers','inflorescence','blossom'],
 'fruit':['fruit','fruits','pod','pods','berry','berries','capsule'],
 'seed':['seed','seeds','nut','nuts'], 'bark':['bark','trunk','trunks'],
 'whole_plant':['whole plant','entire plant','plant specimen','habit','tree','shrub','herb','climber','vine'],
 'habit':['habit','growth form','tree','shrub','herb','climber','vine']
}
EXCLUDE = re.compile(r'\b(diagram|map|microscope|illustration|drawing|icon|logo|chart|anatomy|cross[- ]section|section|herbarium sheet|poster)\b', re.I)
LICENSE_OK = re.compile(r'^(cc\s*by(?:-sa)?(?:\s*\d(?:\.\d)?)?|cc0|public domain|pd|pdm)$', re.I)


def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent':'Dravyaguna-97-image-auditor/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def norm(s):
    return re.sub(r'[^a-z0-9]+',' ', str(s or '').lower()).strip()


def exact_species(title, botanical):
    tokens = re.findall(r'[A-Za-z]{3,}', botanical or '')[:2]
    low = norm(title)
    return len(tokens) >= 2 and all(t.lower() in low.split() for t in tokens)


def candidate_score(title, botanical, part):
    low = norm(title)
    if not exact_species(title, botanical): return -999
    if EXCLUDE.search(title): return -999
    score = 100
    if part in ('root','stem','leaf','flower','fruit','seed','bark'):
        if not any(norm(w) in low for w in PART_WORDS[part]): return -999
        score += 40
    elif part == 'whole_plant':
        if any(norm(w) in low for p in ('root','stem','leaf','flower','fruit','seed','bark') for w in PART_WORDS[p]): return -999
        score += 25 if any(norm(w) in low for w in PART_WORDS[part]) else 0
    elif part == 'habit':
        if any(norm(w) in low for p in ('root','stem','leaf','flower','fruit','seed','bark') for w in PART_WORDS[p]): return -999
        score += 25 if any(norm(w) in low for w in PART_WORDS['habit']) else 0
    return score


def commons_candidates(botanical, part):
    query = f'"{botanical}" ' + (part.replace('_',' ') if part not in ('whole_plant','habit') else ('whole plant' if part=='whole_plant' else 'habit growth form'))
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':30,
        'prop':'imageinfo','iiprop':'url|extmetadata|mime','iiurlwidth':1200,'format':'json','origin':'*'
    })
    data = fetch_json(url)
    out=[]
    for p in (data.get('query',{}).get('pages',{}) or {}).values():
        info=(p.get('imageinfo') or [{}])[0]
        title=str(p.get('title') or '')
        mime=str(info.get('mime') or '')
        lic=str((info.get('extmetadata') or {}).get('LicenseShortName',{}).get('value') or '').strip()
        score=candidate_score(title, botanical, part)
        if score < 0 or not mime.startswith('image/') or not LICENSE_OK.search(re.sub(r'\s+',' ',lic)):
            continue
        u=info.get('thumburl') or info.get('url')
        if not u: continue
        out.append({'score':score,'url':u,'page':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),
                    'title':title.replace('File:','',1),'license':lic,
                    'author':str((info.get('extmetadata') or {}).get('Artist',{}).get('value') or '').strip(),
                    'source':'Wikimedia Commons'})
    return sorted(out,key=lambda x:x['score'],reverse=True)


def inaturalist_candidate(botanical, part):
    if part not in ('whole_plant','habit'): return None
    url='https://api.inaturalist.org/v1/observations?'+urllib.parse.urlencode({'taxon_name':botanical,'photos':'true','photo_license':'cc0,cc-by,cc-by-sa','per_page':40,'order_by':'quality_grade','order':'desc'})
    data=fetch_json(url)
    for obs in data.get('results',[]):
        tax=((obs.get('taxon') or {}).get('name') or '').strip().lower()
        if tax != botanical.lower(): continue
        for ph in obs.get('photos',[]):
            lic=str(ph.get('license_code') or '').lower()
            if lic not in ('cc0','cc-by','cc-by-sa'): continue
            u=str(ph.get('url') or '').replace('/square.','/medium.')
            if not u.startswith('http'): continue
            return {'score':90,'url':u,'page':'https://www.inaturalist.org/observations/'+str(obs.get('id')),
                    'title':'iNaturalist observation','license':lic.upper(),'author':str(ph.get('attribution') or ''),'source':'iNaturalist'}
    return None


def gbif_candidate(botanical, part):
    if part not in ('whole_plant','habit'): return None
    url='https://api.gbif.org/v1/occurrence/search?'+urllib.parse.urlencode({'scientificName':botanical,'media_type':'StillImage','limit':40})
    data=fetch_json(url)
    for rec in data.get('results',[]):
        if str(rec.get('scientificName') or '').lower() != botanical.lower(): continue
        lic=str(rec.get('license') or '').lower()
        if lic and not re.search(r'creativecommons\.org/licenses/(by|by-sa)|cc0|publicdomain',lic): continue
        for media in rec.get('media',[]) or []:
            u=str(media.get('identifier') or '')
            if not u.startswith('http'): continue
            return {'score':80,'url':u,'page':'https://www.gbif.org/occurrence/'+str(rec.get('key')),
                    'title':'GBIF occurrence media','license':rec.get('license') or 'See source','author':media.get('creator') or rec.get('recordedBy') or '', 'source':'GBIF'}
    return None


def main():
    idx=json.loads(INDEX.read_text(encoding='utf-8'))
    plants=json.loads(PLANTS.read_text(encoding='utf-8'))
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {'version':2,'parts':PARTS,'records':[],'policy':{}}
    records=manifest.setdefault('records',[])
    by_key={(str(r.get('plant_id')),str(r.get('part'))):r for r in records}
    plant_by_id={str(p.get('id')):p for p in plants if isinstance(p,dict)}
    changed=False; filled=[]; unresolved=[]
    core=[x for x in idx.get('plants',[]) if x.get('category')=='NCISM-97']
    for ref in core:
        pid=str(ref.get('id')); p=plant_by_id.get(pid,{})
        botanical=(p.get('identity') or {}).get('botanical_name') or ref.get('botanical_name') or ''
        for part in PARTS:
            r=by_key.get((pid,part))
            if not r:
                r={'plant_id':pid,'ncism_order':ref.get('order'),'plant_name':ref.get('name'),'botanical_name':botanical,'part':part,'image_path':'','source_url':'','source_name':'','license':'','author':'','verified_botanical_name':'','verification_status':'missing-queued'}
                records.append(r);by_key[(pid,part)]=r;changed=True
            if r.get('image_path') or r.get('verification_status')=='verified':
                continue
            best=None
            try:
                cs=commons_candidates(botanical,part)
                if cs: best=cs[0]
                if not best: best=inaturalist_candidate(botanical,part)
                if not best: best=gbif_candidate(botanical,part)
            except Exception as e:
                unresolved.append({'plant_id':pid,'part':part,'reason':'source-check-error','detail':str(e)})
                continue
            accepted = bool(best and ((best.get('source')=='Wikimedia Commons' and best.get('score',0)>=100 and exact_species(best.get('title',''),botanical)) or (best.get('source')=='iNaturalist' and part in ('whole_plant','habit')) or (best.get('source')=='GBIF' and part in ('whole_plant','habit'))))
            if accepted:
                r.update({'image_path':best['url'],'source_url':best['page'],'source_name':best['source'],'license':best['license'],'author':best.get('author',''),'verified_botanical_name':botanical,'verification_status':'verified-external','last_checked':datetime.now(timezone.utc).isoformat()})
                changed=True;filled.append({'plant_id':pid,'part':part,'source':best['source'],'title':best['title']})
            else:
                r['last_checked']=datetime.now(timezone.utc).isoformat();unresolved.append({'plant_id':pid,'part':part,'reason':'no-high-confidence-image'})
    manifest['records']=sorted(records,key=lambda r:(int(r.get('ncism_order') or 9999),PARTS.index(r.get('part')) if r.get('part') in PARTS else 99))
    if changed: MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'plants_checked':len(core),'slots_checked':len(core)*len(PARTS),'filled_this_run':filled,'unresolved':unresolved,'remaining_missing':sum(1 for r in manifest['records'] if r.get('verification_status') not in ('verified','verified-external') and not r.get('image_path'))}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'changed':changed,'filled':len(filled),'remaining_missing':report['remaining_missing']},indent=2))

if __name__=='__main__': main()
