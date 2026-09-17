(()=>{
  const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
  const esc=v=>clean(v).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\':'&#039;','"':'&quot;'}[c]||c));
  const tokens=s=>clean(s).toLowerCase().replace(/[()]/g,'').split(/\s+/).filter(x=>x.length>2);
  const partWords={whole_plant:[],habit:['tree','shrub','herb','climber','vine','habit','growth'],root:['root','roots'],stem:['stem','stems','twig','twigs'],leaf:['leaf','leaves','foliage'],flower:['flower','flowers','inflorescence'],fruit:['fruit','fruits'],seed:['seed','seeds'],bark:['bark','trunk']};
  const excluded=/\b(map|diagram|microscope|cross[- ]?section|histology|chemical|medicine|tablet|capsule|powder|painting|logo|flag|person|animal)\b/i;
  const api=async(species,part,used)=>{
    const speciesClean=clean(species);if(!speciesClean)return null;
    const exact=speciesClean.replace(/\s*\([^)]*\)/g,'').trim();
    const categories=[`Category:${exact}`,`Category:${exact} (${part==='fruit'?'fruit':part})`];
    for(const cat of categories){
      try{
        const u='https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+encodeURIComponent(cat)+'&cmtype=file&cmlimit=80&format=json&origin=*';
        const r=await fetch(u,{cache:'force-cache'});if(!r.ok)continue;const j=await r.json();const members=j.query?.categorymembers||[];
        if(!members.length)continue;
        const pages=members.map(x=>x.pageid).filter(Boolean).join('|');
        if(!pages)continue;
        const infoUrl='https://commons.wikimedia.org/w/api.php?action=query&pageids='+pages+'&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=1200&format=json&origin=*';
        const ir=await fetch(infoUrl,{cache:'force-cache'});if(!ir.ok)continue;const ij=await ir.json();
        const tk=tokens(exact),wanted=partWords[part]||[];
        const candidates=Object.values(ij.query?.pages||{}).map(p=>({p,info:p.imageinfo?.[0]})).filter(x=>{
          const title=clean(x.p?.title||'').toLowerCase(),info=x.info;
          if(!info||String(info.mime||'').startsWith('video/'))return false;
          const url=info.thumburl||info.url;if(!/^https?:\/\//i.test(url)||used.has(url))return false;
          if(excluded.test(title))return false;
          const speciesScore=tk.filter(t=>title.includes(t)).length;
          if(speciesScore<Math.min(2,tk.length))return false;
          if(part==='whole_plant')return !/(leaf|flower|fruit|seed|root|bark|stem|twig|trunk)/i.test(title);
          if(part==='habit')return /(tree|shrub|herb|climber|vine|habit|growth)/i.test(title)&&!/(leaf|flower|fruit|seed|root|bark|stem|twig|trunk)/i.test(title);
          return wanted.some(w=>title.includes(w));
        }).sort((a,b)=>{
          const wa=(partWords[part]||[]).filter(w=>String(a.p.title).toLowerCase().includes(w)).length;
          const wb=(partWords[part]||[]).filter(w=>String(b.p.title).toLowerCase().includes(w)).length;
          return wb-wa;
        });
        const x=candidates[0];if(x){const url=x.info.thumburl||x.info.url;used.add(url);return{url,title:x.p.title,page:'https://commons.wikimedia.org/wiki/'+encodeURIComponent(String(x.p.title).replace(/ /g,'_')),source:'Wikimedia Commons'}}
      }catch(e){}
    }
    return null;
  };
  async function buildGallery(){
    const host=document.getElementById('plant-gallery-host');if(!host)return;
    let id=new URLSearchParams(location.search).get('id');if(!id)return;
    let p;try{const r=await fetch(`data/plants/${encodeURIComponent(id)}.json`,{cache:'no-store'});if(r.ok)p=await r.json()}catch(e){}
    if(!p)return;
    const species=p.identity?.botanical_name||p.botanical_name||'';if(!species)return;
    const name=p.identity?.name||p.name||id,used=new Set();
    const pairs=[['whole_plant','Whole plant','Overall habit and plant form'],['habit','Habit / growth form','Growth form / field appearance'],['bark','Bark','Bark / trunk character'],['leaf','Leaf','Leaf morphology'],['flower','Flower','Flower / inflorescence'],['fruit','Fruit','Fruit morphology'],['seed','Seed','Seed / dried fruit if specifically documented'],['root','Root','Root morphology'],['stem','Stem (Twig)','Stem / twig character']];
    host.innerHTML='<div class="image-loading" style="grid-column:1/-1">🔎 Verifying species-specific botanical images…</div>';
    const cards=[];
    for(const [part,label,note] of pairs){
      const result=await api(species,part,used);
      if(result){cards.push(`<figure class="gallery-item botanical-verified"><img src="${esc(result.url)}" alt="${esc(name+' '+label)}" loading="lazy" class="plant-gallery-image"><figcaption>${esc(label)}<small>${esc(note)}</small><a class="gallery-source" href="${esc(result.page)}" target="_blank" rel="noopener noreferrer">Source: Wikimedia Commons ↗</a></figcaption></figure>`)}
      else cards.push(`<figure class="gallery-item botanical-missing"><div class="image-loading">No species-specific image verified yet</div><figcaption>${esc(label)}<small>${esc(note)}</small></figcaption></figure>`);
    }
    host.innerHTML=cards.join('');
    host.querySelectorAll('.plant-gallery-image').forEach(img=>img.addEventListener('error',()=>{const f=img.closest('.gallery-item');if(f){f.classList.remove('botanical-verified');f.classList.add('botanical-missing');f.innerHTML='<div class="image-loading">Image failed verification</div><figcaption>Species-specific image unavailable</figcaption>'}}));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',buildGallery);else buildGallery();
})();