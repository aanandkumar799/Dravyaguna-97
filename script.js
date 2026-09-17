document.addEventListener('DOMContentLoaded', () => {
  const plantList = document.getElementById('plant-list');
  const searchInput = document.getElementById('searchInput') || document.getElementById('search');
  if (!plantList) return;

  const INDEX_URL = new URL('plant-index.json?v=98', location.href).href;
  const MANIFEST_URL = new URL('data/curated-image-manifest.json?v=4', location.href).href;
  const initialLimit = 24;
  const EXPECTED_NCISM_COUNT = 97;
  let masterPlants = [], mode = 'grid', categoryFilter = 'all', showAll = false, coverRegistry = new Map();

  const esc = v => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#039;');
  const norm = v => String(v ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').replace(/\s+/g,' ').trim();
  const text = v => Array.isArray(v) ? v.map(text).join(' ') : (v && typeof v === 'object' ? Object.values(v).map(text).join(' ') : String(v ?? ''));
  const name = p => p?.name || p?.identity?.name || '';
  const sanskrit = p => p?.sanskrit_name || p?.identity?.sanskrit_name || p?.classical_sanskrit_name || '';
  const botanical = p => p?.botanical_name || p?.identity?.botanical_name || '';
  const family = p => p?.family || p?.identity?.family || '';
  const order = p => Number.isFinite(Number(p?.order)) ? Number(p.order) : 9999;
  const isNCISM = p => String(p?.category || '').toUpperCase() === 'NCISM-97' && order(p) >= 1 && order(p) <= EXPECTED_NCISM_COUNT;

  const score = (p, q) => {
    q = norm(q); if (!q) return 0;
    const fields = [[name(p),1200],[sanskrit(p),1100],[p.transliteration,1050],[botanical(p),1000],[p.english_name||p.identity?.english_name,900],[family(p),800],[p.id,750],[p.search_text,200]];
    return fields.reduce((total,[v,points]) => { const x=norm(v); if(!x) return total; return total+(x===q?points:x.startsWith(q)?points*.65:x.includes(q)?points*.45:0); },0);
  };

  const filtered = q => {
    let list = masterPlants.filter(p => categoryFilter === 'all' || String(p.category).toUpperCase() === categoryFilter);
    if (!norm(q)) return list;
    return list.map(p=>({p,s:score(p,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s||order(a.p)-order(b.p)).map(x=>x.p);
  };

  const placeholder = label => {
    const safe=esc(label||'Plant');
    const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf5ef"/><text x="400" y="220" text-anchor="middle" font-family="Arial" font-size="76">🌿</text><text x="400" y="305" text-anchor="middle" font-family="Arial" font-size="30" fill="#1b4332">${safe}</text><text x="400" y="350" text-anchor="middle" font-family="Arial" font-size="18" fill="#6b756f">Verified whole-plant photograph not yet approved</text></svg>`;
    return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
  };

  async function loadCovers(){
    try{
      const r=await fetch(MANIFEST_URL,{cache:'no-store',headers:{Accept:'application/json'}}); if(!r.ok) return;
      const m=await r.json();
      for(const rec of (Array.isArray(m?.records)?m.records:[])){
        if(rec?.part!=='whole_plant'||!rec.image_path||!/^https?:\/\//i.test(rec.image_path)) continue;
        if(!['verified','verified-external'].includes(String(rec.verification_status))||!rec.source_url||!rec.source_name||!rec.verified_botanical_name) continue;
        const id=String(rec.plant_id||''); if(id&&!coverRegistry.has(id)) coverRegistry.set(id,rec);
      }
    }catch(_){/* Images are optional; the library remains usable. */}
  }

  function card(p){
    const n=name(p), id=String(p.id||''), rec=coverRegistry.get(id);
    const verified=rec && norm(rec.verified_botanical_name)===norm(botanical(p));
    const image=verified ? `<img src="${esc(rec.image_path)}" alt="${esc(n)} — verified whole-plant photograph" loading="lazy" decoding="async">` : `<img src="${placeholder(n)}" alt="${esc(n)} — verified whole-plant photograph unavailable" loading="lazy">`;
    return `<article class="plant-card"><div class="plant-image">${image}</div><div class="plant-card-content"><div class="plant-card-top"><span class="plant-number">#${order(p)}</span><span class="syllabus-marker">NCISM-97</span></div><h3>${esc(n)}</h3>${sanskrit(p)?`<p class="plant-sanskrit">${esc(sanskrit(p))}</p>`:''}${botanical(p)?`<p class="plant-botanical"><em>${esc(botanical(p))}</em></p>`:''}${p.english_name?`<p class="plant-english">${esc(p.english_name)}</p>`:''}${family(p)?`<p class="plant-family"><strong>Family:</strong> ${esc(family(p))}</p>`:''}<a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">Open Full Dossier →</a></div></article>`;
  }

  function flashcard(p){
    const n=name(p), s=sanskrit(p), rasa=text(p.rasa)||'—', guna=text(p.guna)||'—', virya=p.virya||'—', vipaka=p.vipaka||'—', useful=text(p.useful_part)||'—';
    return `<article class="flashcard" tabindex="0"><div class="flash-inner"><div class="flash-face"><div class="plant-number">#${order(p)}</div><h3>${esc(n)}</h3><div class="big-sanskrit">${esc(s||'Sanskrit name unavailable')}</div><p>${esc(botanical(p))}</p><small>Tap / click to flip</small></div><div class="flash-face flash-back"><h3>${esc(n)}</h3><p><strong>Rasa:</strong> ${esc(rasa)}</p><p><strong>Guna:</strong> ${esc(guna)}</p><p><strong>Virya:</strong> ${esc(virya)}</p><p><strong>Vipaka:</strong> ${esc(vipaka)}</p><p><strong>Useful part:</strong> ${esc(useful)}</p><a class="view-plant" href="./plant.html?id=${encodeURIComponent(p.id)}">Open Full Dossier →</a></div></div></article>`;
  }

  function render(q=''){
    const results=filtered(q), info=document.getElementById('search-result-info');
    if(info) info.textContent=q?`${results.length} result${results.length===1?'':'s'} found for “${q}”`:`${results.length} records in the NCISM-97 library`;
    if(!results.length){plantList.className='plant-grid';plantList.innerHTML='<div class="no-results"><div style="font-size:3rem">🔎</div><h3>No plants found</h3><p>Try a Sanskrit name, Roman name, botanical name, family, or NCISM number.</p></div>';return;}
    const visible=q||showAll?results:results.slice(0,initialLimit);
    if(mode==='flash'){
      plantList.className='flash-grid';plantList.innerHTML=visible.map(flashcard).join('');
      plantList.querySelectorAll('.flashcard').forEach(c=>{const flip=()=>c.classList.toggle('flipped');c.addEventListener('click',e=>{if(!e.target.closest('a'))flip()});c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();flip()}})});
    }else{
      plantList.className='plant-grid';plantList.innerHTML=visible.map(card).join('')+(!q&&!showAll&&results.length>initialLimit?`<div class="plant-list-actions"><p>Showing ${initialLimit} of ${results.length} records.</p><button type="button" id="show-all-plants">Show all ${results.length}</button></div>`:'');
      document.getElementById('show-all-plants')?.addEventListener('click',()=>{showAll=true;render(q)});
    }
  }

  function showIndexNotice(total){
    const existing=document.getElementById('library-integrity-notice');
    existing?.remove();
    if(total===EXPECTED_NCISM_COUNT) return;
    const notice=document.createElement('div');
    notice.id='library-integrity-notice';
    notice.className='medical-disclaimer';
    notice.style.margin='0 0 18px';
    notice.innerHTML=`<strong>Library data notice:</strong> ${total} of ${EXPECTED_NCISM_COUNT} NCISM-97 records are currently indexed. Available records remain searchable; missing records are not hidden behind a database error.`;
    plantList.parentElement.insertBefore(notice,plantList);
  }

  async function load(){
    plantList.setAttribute('aria-busy','true');
    try{
      const [ir]=await Promise.all([fetch(INDEX_URL,{cache:'no-store',headers:{Accept:'application/json'}}),loadCovers()]);
      if(!ir.ok) throw new Error(`Index request failed: ${ir.status}`);
      const data=await ir.json();
      const rows=Array.isArray(data)?data:(Array.isArray(data?.plants)?data.plants:[]);
      masterPlants=rows.filter(isNCISM).sort((a,b)=>order(a)-order(b));
      if(!masterPlants.length) throw new Error('No valid NCISM-97 records found in plant-index.json');
      showIndexNotice(masterPlants.length);
      render('');
    }catch(e){
      console.error('DravyaGuna library load error:',e);
      plantList.innerHTML='<div class="plant-error"><h3>Plant database unavailable</h3><p>The plant index could not be loaded. Please refresh after deployment or check your connection.</p><button type="button" class="plant-list-actions" id="retry-library" style="border:0;background:#1b4332;color:#fff;border-radius:9px;padding:10px 16px;font:inherit;font-weight:700;cursor:pointer">Retry</button></div>';
      document.getElementById('retry-library')?.addEventListener('click',load);
    }finally{plantList.setAttribute('aria-busy','false');}
  }

  document.querySelectorAll('[data-mode]').forEach(btn=>btn.addEventListener('click',()=>{mode=btn.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'')}));
  document.querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{categoryFilter=String(btn.dataset.category||'all').toUpperCase();showAll=false;document.querySelectorAll('[data-category]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'')}));
  searchInput?.addEventListener('input',()=>{showAll=false;clearTimeout(window.__dgSearchTimer);window.__dgSearchTimer=setTimeout(()=>render(searchInput.value),80)});
  document.getElementById('jumpButton')?.addEventListener('click',()=>{const n=Number(document.getElementById('ncismJump')?.value),p=masterPlants.find(x=>order(x)===n);if(p)location.href=`./plant.html?id=${encodeURIComponent(p.id)}`});
  document.getElementById('ncismJump')?.addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('jumpButton')?.click()});
  load();
});
