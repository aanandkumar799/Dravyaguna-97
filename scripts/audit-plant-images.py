import json, re, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]; INDEX=ROOT/'plant-index.json'; PLANTS_DIR=ROOT/'data'/'plants'; MANIFEST=ROOT/'data'/'curated-image-manifest.json'; REPORT=ROOT/'data'/'image-audit-report.json'; IMAGE_ROOT=ROOT/'images'/'plants'
PARTS=['whole_plant','habit','root','stem','leaf','flower','fruit','seed','bark']
PART_WORDS={'root':['root','roots'],'stem':['stem','stems','twig','twigs'],'leaf':['leaf','leaves','foliage'],'flower':['flower','flowers','inflorescence','blossom'],'fruit':['fruit','fruits','pod','pods','berry','berries','capsule'],'seed':['seed','seeds','nut','nuts'],'bark':['bark','trunk','trunks'],'whole_plant':['whole plant','entire plant','plant specimen'],'habit':['habit','growth form','tree','shrub','herb','climber','vine']}
PART_EXCLUDE={'whole_plant':['leaf','flower','fruit','seed','root','bark','stem','twig','trunk'],'habit':['leaf','flower','fruit','seed','root','bark','stem','twig','trunk']}
BAD=re.compile(r'\b(diagram|map|microscope|illustration|drawing|icon|logo|chart|anatomy|cross[- ]section|histology|chemical|medicine|tablet|capsule|powder|poster|herbarium\s+sheet)\b',re.I)
LICENSE_OK=re.compile(r'^(cc\s*by(?:-sa)?(?:\s*\d(?:\.\d)?)?|cc0|public domain|pd|pdm)$',re.I)
INAT_LICENSES={'cc-by':'CC BY','cc-by-sa':'CC BY-SA','cc0':'CC0'}
USER_AGENT='Dravyaguna-97-image-auditor/5.0'

def fetch_json(url,timeout=30):
    req=urllib.request.Request(url,headers={'User-Agent':USER_AGENT});
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def norm(s):return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()
def species_tokens(botanical):return [x for x in re.findall(r'[a-z]{3,}',norm(botanical))[:2]]
def species_in_text(text,botanical):
    low=norm(text); tk=species_tokens(botanical)
    return len(tk)==2 and all(t in low.split() for t in tk)
def part_ok(text,part):
    low=norm(text)
    if BAD.search(text):return False
    if part in PART_EXCLUDE:return not any(w in low.split() for w in PART_EXCLUDE[part])
    return any(norm(w) in low.split() for w in PART_WORDS.get(part,[]))

def commons_candidates(botanical,part):
    queries=[f'"{botanical}" {part.replace("_"," ")}',f'{botanical} {part.replace("_"," ")}',botanical]
    out=[]; seen=set()
    for query in queries:
        url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','generator':'search','gsrsearch':query,'gsrnamespace':6,'gsrlimit':50,'prop':'imageinfo','iiprop':'url|extmetadata|mime','iiurlwidth':1600,'format':'json','origin':'*'})
        try:data=fetch_json(url)
        except Exception:continue
        for p in (data.get('query',{}).get('pages',{}) or {}).values():
            info=(p.get('imageinfo') or [{}])[0]; title=str(p.get('title') or ''); mime=str(info.get('mime') or ''); meta=info.get('extmetadata') or {}
            lic=str(meta.get('LicenseShortName',{}).get('value') or '').strip(); desc=str(meta.get('ImageDescription',{}).get('value') or ''); cats=str(meta.get('Categories',{}).get('value') or '')
            blob=f'{title} {desc} {cats}'
            if mime not in ('image/jpeg','image/png','image/webp') or not LICENSE_OK.search(re.sub(r'\s+',' ',lic)):continue
            if not species_in_text(blob,botanical) or not part_ok(blob,part):continue
            u=info.get('thumburl') or info.get('url'); page='https://commons.wikimedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_'))
            if not u or page in seen:continue
            seen.add(page); out.append({'url':u,'page':page,'title':title.replace('File:','',1),'license':lic,'author':str(meta.get('Artist',{}).get('value') or '').strip(),'source':'Wikimedia Commons'})
        if len(out)>=25:break
    return out

def inat_candidates(botanical,part):
    if part not in ('whole_plant','habit'):return []
    out=[]; seen=set()
    for lic in ('CC-BY','CC-BY-SA'):
        params={'taxon_name':botanical,'photo_license':lic,'quality_grade':'research','photos':'true','per_page':100,'order_by':'votes','order':'desc'}
        try:data=fetch_json('https://api.inaturalist.org/v1/observations?'+urllib.parse.urlencode(params))
        except Exception:continue
        for obs in data.get('results',[]):
            tax=obs.get('taxon') or {}; taxname=str(tax.get('name') or '')
            if norm(taxname)!=norm(botanical):continue
            for photo in obs.get('photos') or []:
                code=str(photo.get('license_code') or '').lower();
                if code not in INAT_LICENSES:continue
                pid=str(photo.get('id') or ''); page=f"https://www.inaturalist.org/observations/{obs.get('id')}"; u=str(photo.get('url') or '')
                if not u or pid in seen:continue
                seen.add(pid); large=re.sub(r'/square\.(jpg|jpeg|png)$',r'/large.\1',u)
                out.append({'url':large,'page':page,'title':f"iNaturalist photo {pid}",'license':INAT_LICENSES[code],'author':str(photo.get('attribution') or '').strip(),'source':'iNaturalist'})
    return out

def local_path(pid,part,ext='jpg'):return IMAGE_ROOT/pid/part/f'image.{ext}'
def download_image(url,destination):
    destination.parent.mkdir(parents=True,exist_ok=True); req=urllib.request.Request(url,headers={'User-Agent':USER_AGENT})
    with urllib.request.urlopen(req,timeout=45) as r:data=r.read(); content_type=str(r.headers.get_content_type() or '')
    if content_type not in ('image/jpeg','image/png','image/webp') or len(data)<2048:raise ValueError(f'unsupported or empty image response: {content_type}, {len(data)} bytes')
    ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[content_type]; final=destination.with_suffix('.'+ext); final.write_bytes(data); return final.relative_to(ROOT).as_posix(),len(data)
def materialize_record(r):
    src=str(r.get('image_path') or '')
    if src.startswith('images/plants/'):
        p=ROOT/src
        if p.exists() and p.stat().st_size>2048:return src,0
        src=str(r.get('source_media_url') or '')
    if not src.startswith('http'):return '',0
    return download_image(src,local_path(str(r['plant_id']),str(r['part'])))

def main():
    idx=json.loads(INDEX.read_text(encoding='utf-8')); old=json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {'version':3,'records':[]}
    manifest=old; records=manifest.setdefault('records',[]); by_key={(str(r.get('plant_id')),str(r.get('part'))):r for r in records}; core=sorted([x for x in idx.get('plants',[]) if x.get('category')=='NCISM-97' and 1<=int(x.get('order',0) or 0)<=97],key=lambda x:int(x['order']))
    filled=[]; unresolved=[]; used_sources=set(); changed=False
    for r in records:
        for k in ('source_url','source_media_url'):
            if r.get(k):used_sources.add(str(r[k]))
    for ref in core:
        pid=str(ref['id']); fp=PLANTS_DIR/f'{pid}.json'; p=json.loads(fp.read_text(encoding='utf-8')) if fp.exists() else {}; botanical=str((p.get('identity') or {}).get('botanical_name') or ref.get('botanical_name') or '').strip()
        for part in PARTS:
            r=by_key.get((pid,part))
            if not r:
                r={'plant_id':pid,'ncism_order':ref.get('order'),'plant_name':ref.get('name'),'botanical_name':botanical,'part':part,'image_path':'','source_url':'','source_name':'','license':'','author':'','verified_botanical_name':'','verification_status':'missing-queued'}; records.append(r); by_key[(pid,part)]=r; changed=True
            if r.get('verification_status') in ('verified','verified-external') and r.get('image_path'):
                try:
                    local,size=materialize_record(r)
                    if local:r['source_media_url']=r.get('image_path'); r['image_path']=local; r['verification_status']='verified-local'; filled.append({'plant_id':pid,'part':part,'action':'downloaded-approved-image','path':local,'bytes':size}); changed=True
                    continue
                except Exception: r['verification_status']='download-failed'; r['image_path']=''; changed=True
            if r.get('verification_status')=='verified-local' and r.get('image_path') and (ROOT/str(r['image_path'])).exists():continue
            candidates=commons_candidates(botanical,part)
            if not candidates:candidates=inat_candidates(botanical,part)
            best=next((x for x in candidates if x['page'] not in used_sources and x['url'] not in used_sources),None)
            if not best:
                unresolved.append({'plant_id':pid,'part':part,'reason':'no-high-confidence-unique-image'});continue
            try:local,size=download_image(best['url'],local_path(pid,part))
            except Exception as e:unresolved.append({'plant_id':pid,'part':part,'reason':'download-failed','detail':str(e)});continue
            used_sources.update((best['page'],best['url'])); r.update({'image_path':local,'source_media_url':best['url'],'source_url':best['page'],'source_name':best['source'],'license':best['license'],'author':best['author'],'verified_botanical_name':botanical,'verification_status':'verified-local','title':best['title']}); filled.append({'plant_id':pid,'part':part,'action':'downloaded-new-image','path':local,'bytes':size}); changed=True
    manifest['version']=5; manifest['parts']=PARTS; manifest['policy']={'exact_species_required':True,'part_specific_required':True,'source_license_required':True,'global_duplicates_forbidden':True,'ai_only_matches_forbidden':True,'wrong_image_preferred_over_missing':False,'old_registry_reverification_required':True,'local_assets_required':True,'additional_sources':['Wikimedia Commons','iNaturalist']}; manifest['records']=sorted(records,key=lambda r:(int(r.get('ncism_order') or 9999),PARTS.index(r.get('part')) if r.get('part') in PARTS else 99)); MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    remaining=sum(1 for r in manifest['records'] if not r.get('image_path') or r.get('verification_status')!='verified-local')
    REPORT.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),'plants_checked':len(core),'slots_checked':len(core)*len(PARTS),'filled_this_run':filled,'unresolved':unresolved,'remaining_missing':remaining,'local_asset_root':'images/plants/<plant>/<part>/image.*','policy':manifest['policy']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'changed':changed,'filled':len(filled),'remaining_missing':remaining},indent=2))
if __name__=='__main__':main()
