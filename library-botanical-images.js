(()=>{
  const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
  const tokens=s=>clean(s).toLowerCase().replace(/[()]/g,'').split(/\s+/).filter(x=>x.length>2);
  const excluded=/\b(map|diagram|microscope|cross[- ]?section|histology|chemical|medicine|tablet|capsule|powder|painting|logo|flag|person|animal|leaf|flower|fruit|seed|root|bark|stem|twig|trunk)\b/i;
  const cache=new Map();
  async function find(species){
    if(cache.has(species))return cache.get(species);const promise=(async()=>{try{
      const exact=clean(species).replace(/\s*\([^)]*\)/g,'').trim();const u='https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+encodeURIComponent('Category:'+exact)+'&cmtype=file&cmlimit=80&format=json&origin=*';
      const r=await fetch(u,{cache:'force-cache'});if(!r.ok)return null;const j=await r.json();const members=j.query?.categorymembers||[];if(!members.length)return null;const ids=members.map(x=>x.pageid).filter(Boolean).join('|');if(!ids)return null;
      const ir=await fetch('https://commons.wikimedia.org/w/api.php?action=query&pageids='+ids+'&prop=imageinfo&iiprop=url|mime&iiurlwidth=1000&format=json&origin=*',{cache:'force-cache'});if(!ir.ok)return null;const ij=await ir.json();const tk=tokens(exact);
      const candidates=Object.values(ij.query?.pages||{}).map(p=>({p,i:p.imageinfo?.[0]})).filter(x=>{const title=String(x.p?.title||'').toLowerCase(),i=x.i;if(!i||String(i.mime||'').startsWith('video/'))return false;if(excluded.test(title))return false;if(tk.filter(t=>title.includes(t)).length<Math.min(2,tk.length))return false;const u=i.thumburl||i.url;return /^https?:\/\//i.test(u)});
      const x=candidates[0],i=x?.i;if(!i)return null;return{url:i.thumburl||i.url,page:'https://commons.wikimedia.org/wiki/'+encodeURIComponent(String(x.p.title).replace(/ /g,'_'))};
    }catch(e){return null}})();cache.set(species,promise);return promise;
  }
  async function verify(){
    const imgs=[...document.querySelectorAll('#plant-list img[data-botanical]')];await Promise.all(imgs.map(async img=>{if(img.dataset.verified==='true')return;const species=clean(img.dataset.botanical);if(!species)return;const r=await find(species);if(r){img.src=r.url;img.dataset.verified='true';img.dataset.source=r.page;img.title='Species-specific botanical image • Wikimedia Commons'}else{img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — species-specific image unavailable';img.parentElement.innerHTML='<div class="library-image-missing">🌿<span>Verified image unavailable</span></div>'}}));
  }
  let scheduled=false;const run=()=>{if(scheduled)return;scheduled=true;setTimeout(()=>{scheduled=false;verify()},120)};new MutationObserver(run).observe(document.getElementById('plant-list')||document.body,{childList:true,subtree:true});if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();