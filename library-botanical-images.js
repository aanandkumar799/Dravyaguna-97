(()=>{
  const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
  const norm=v=>clean(v).toLowerCase().replace(/[^a-z0-9]+/g,' ').replace(/\s+/g,' ').trim();
  const core=s=>norm(clean(s).replace(/\s*\([^)]*\)/g,'')).split(' ').slice(0,2).join(' ');
  const cache=new Map();
  const excluded=/\b(map|diagram|microscope|cross[- ]?section|histology|chemical|medicine|tablet|capsule|powder|painting|logo|flag|person|animal|leaf|flower|fruit|seed|root|bark|stem|twig|trunk|poster|chart)\b/i;
  async function find(species){
    const key=core(species);if(!key)return null;if(cache.has(key))return cache.get(key);
    const promise=(async()=>{try{
      const u='https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch='+encodeURIComponent('"'+key+'"')+'&gsrnamespace=6&gsrlimit=40&prop=imageinfo&iiprop=url|mime|extmetadata&iiurlwidth=1200&format=json&origin=*';
      const r=await fetch(u,{cache:'force-cache'});if(!r.ok)return null;const j=await r.json(),tk=key.split(' ');
      const candidates=Object.values(j.query?.pages||{}).map(p=>({p,i:p.imageinfo?.[0]})).filter(x=>{
        const title=clean(x.p?.title||''),low=title.toLowerCase(),i=x.i;if(!i||String(i.mime||'').startsWith('video/'))return false;if(excluded.test(low))return false;
        if(tk.filter(t=>low.includes(t)).length<2)return false;const url=i.thumburl||i.url;return /^https?:\/\//i.test(url);
      }).sort((a,b)=>tk.filter(t=>String(b.p.title).toLowerCase().includes(t)).length-tk.filter(t=>String(a.p.title).toLowerCase().includes(t)).length);
      const x=candidates[0],i=x?.i;if(!i)return null;return{url:i.thumburl||i.url,page:'https://commons.wikimedia.org/wiki/'+encodeURIComponent(String(x.p.title).replace(/ /g,'_')),title:String(x.p.title)};
    }catch(e){return null}})();cache.set(key,promise);return promise;
  }
  async function verify(){
    const imgs=[...document.querySelectorAll('#plant-list img[data-botanical]')];
    await Promise.all(imgs.map(async img=>{if(img.dataset.verified==='true')return;const r=await find(img.dataset.botanical);if(r){img.src=r.url;img.dataset.verified='true';img.dataset.source=r.page;img.title='Species-specific image • Wikimedia Commons • '+r.title;}else{img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — species-specific image unavailable';img.parentElement.innerHTML='<div class="library-image-missing">🌿<span>Verified species image unavailable</span></div>';}}));
  }
  let scheduled=false;const run=()=>{if(scheduled)return;scheduled=true;setTimeout(()=>{scheduled=false;verify()},150)};
  const target=document.getElementById('plant-list')||document.body;new MutationObserver(run).observe(target,{childList:true,subtree:true});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();