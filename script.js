document.addEventListener('DOMContentLoaded', () => {
  // Compatibility anchors for legacy/internal navigation. These IDs are created
  // before the page becomes interactive, so links such as #search and #student
  // remain valid while the markup can evolve independently.
  const anchorTargets = [
    ['search', document.querySelector('.search-panel')],
    ['student', [...document.querySelectorAll('.persona')].find(x => /student/i.test(x.textContent))],
    ['teacher', [...document.querySelectorAll('.persona')].find(x => /teacher/i.test(x.textContent))],
    ['doctor', [...document.querySelectorAll('.persona')].find(x => /doctor/i.test(x.textContent))]
  ];
  for (const [id, el] of anchorTargets) if (el && !el.id) el.id = id;

  const plantList = document.getElementById('plant-list');
  const searchInput = document.getElementById('searchInput') || document.getElementById('search');
  if (!plantList) return;

  const INDEX_URL = new URL('plant-index.json?v=99', location.href).href;
  const MANIFEST_URL = new URL('data/curated-image-manifest.json?v=4', location.href).href;
  const initialLimit = 24;
  const EXPECTED_NCISM_COUNT = 97;
  const FAVORITES_KEY = 'dg97-favourites-v1';
  let masterPlants = [], mode = 'grid', categoryFilter = 'all', showAll = false, coverRegistry = new Map(), favoritesOnly = false, dossierSearchReady = false, dossierSearchLoading = false;
  const filters = { rasa:'', guna:'', virya:'', vipaka:'' };

  const esc = v => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#039;');
  const norm = v => String(v ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').replace(/\s+/g,' ').trim();
  const text = v => Array.isArray(v) ? v.map(text).join(' ') : (v && typeof v === 'object' ? Object.values(v).map(text).join(' ') : String(v ?? ''));
  const name = p => p?.name || p?.identity?.name || '';
  const sanskrit = p => p?.sanskrit_name || p?.identity?.sanskrit_name || p?.classical_sanskrit_name || '';
  const botanical = p => p?.botanical_name || p?.identity?.botanical_name || '';
  const family = p => p?.family || p?.identity?.family || '';
  const order = p => Number.isFinite(Number(p?.order)) ? Number(p.order) : 9999;
  const isNCISM = p => String(p?.category || '').toUpperCase() === 'NCISM-97' && order(p) >= 1 && order(p) <= EXPECTED_NCISM_COUNT;
  const getFavorites = () => { try { const x=JSON.parse(localStorage.getItem(FAVORITES_KEY)||'[]'); return new Set(Array.isArray(x)?x.map(String):[]); } catch(_) { return new Set(); } };
  const saveFavorites = set => { try { localStorage.setItem(FAVORITES_KEY, JSON.stringify([...set])); } catch(_) {} };

  const dossierValue = v => Array.isArray(v) ? v.map(dossierValue).join(' ') : (v && typeof v === 'object' ? Object.values(v).map(dossierValue).join(' ') : String(v ?? ''));
  const dossierAreas = p => p?._searchAreas || {};
  const queryTokens = q => norm(q).split(' ').filter(Boolean);
  const score = (p, q) => {
    q = norm(q); if (!q) return 0;
    const tokens = queryTokens(q);
    const fields = [
      [name(p),1500,'Identity'],[sanskrit(p),1450,'Identity'],[p.transliteration,1350,'Identity'],
      [botanical(p),1300,'Botanical identity'],[p.english_name||p.identity?.english_name,1200,'Identity'],
      [family(p),1050,'Family'],[p.id,950,'Identity'],[text(p.useful_part),900,'Useful part'],
      [p.search_text,500,'Index']
    ];
    let total=0;
    for(const [v,points] of fields){
      const x=norm(v); if(!x) continue;
      if(x===q) total+=points;
      else if(x.startsWith(q)) total+=points*.72;
      else if(x.includes(q)) total+=points*.5;
      else if(tokens.length>1 && tokens.every(t=>x.includes(t))) total+=points*.42;
    }
    const areas=dossierAreas(p);
    for(const [area,value] of Object.entries(areas)){
      const x=norm(value); if(!x) continue;
      if(x.includes(q)) total+=area==='Formulations'?850:area==='Classical References'?800:area==='Identification'?760:area==='Therapeutics'?700:600;
      else if(tokens.length>1 && tokens.every(t=>x.includes(t))) total+=360;
    }
    return total;
  };
  const matchAreas = (p,q) => {
    const areas=dossierAreas(p), nq=norm(q);
    if(!nq)return [];
    return Object.entries(areas).filter(([,v])=>norm(v).includes(nq)).map(([k])=>k).slice(0,3);
  };
  const searchResult = (p,q) => ({p,s:score(p,q),areas:matchAreas(p,q)});
  const matchesFilter = (p,key,value) => !value || norm(text(p?.[key])).split(' ').includes(norm(value)) || norm(text(p?.[key])).includes(norm(value));

  const filtered = q => {
    let list = masterPlants.filter(p => categoryFilter === 'all' || String(p.category).toUpperCase() === categoryFilter);
    list = list.filter(p => Object.entries(filters).every(([k,v]) => matchesFilter(p,k,v)));
    if (favoritesOnly) { const fav=getFavorites(); list=list.filter(p=>fav.has(String(p.id))); }
    if (!norm(q)) return list;
    return list.map(p=>searchResult(p,q)).filter(x=>x.s>0).sort((a,b)=>b.s-a.s||order(a.p)-order(b.p)).map(x=>{x.p._searchMatchAreas=x.areas;return x.p;});
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
        if(rec?.part!=='whole_plant'||!rec.image_path) continue;
        if(!['verified','verified-external'].includes(String(rec.verification_status))||!rec.source_url||!rec.source_name||!rec.verified_botanical_name) continue;
        const id=String(rec.plant_id||''); if(id&&!coverRegistry.has(id)){ const resolved={...rec,image_path:new URL(String(rec.image_path),location.href).href}; coverRegistry.set(id,resolved); }
      }
    }catch(_){/* Images are optional; the library remains usable. */}
  }

  function card(p){
    const n=name(p), id=String(p.id||''), rec=coverRegistry.get(id), fav=getFavorites().has(id);
    const verified=rec && norm(rec.verified_botanical_name)===norm(botanical(p));
    const dynamicCover=new URL(`images/plants/${encodeURIComponent(id)}/whole_plant/image.jpg`,location.href).href;
    const coverSrc=verified ? rec.image_path : dynamicCover;
    const fallback=placeholder(n);
    const image=`<img src="${esc(coverSrc)}" alt="${esc(n)} — whole-plant photograph" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='${fallback}'">`;
    return `<article class="plant-card"><button class="favorite-btn ${fav?'active':''}" type="button" data-favorite="${esc(id)}" aria-label="${fav?'Remove':'Add'} ${esc(n)} ${fav?'from':'to'} favourites" aria-pressed="${fav}">${fav?'★':'☆'}</button><div class="plant-image">${image}</div><div class="plant-card-content"><div class="plant-card-top"><span class="plant-number">#${order(p)}</span><span class="syllabus-marker">NCISM-97</span></div><h3>${esc(n)}</h3>${sanskrit(p)?`<p class="plant-sanskrit">${esc(sanskrit(p))}</p>`:''}${botanical(p)?`<p class="plant-botanical"><em>${esc(botanical(p))}</em></p>`:''}${p.english_name?`<p class="plant-english">${esc(p.english_name)}</p>`:''}${family(p)?`<p class="plant-family"><strong>Family:</strong> ${esc(family(p))}</p>`:''}${Array.isArray(p._searchMatchAreas)&&p._searchMatchAreas.length?`<div class="search-match-badges" aria-label="Matching dossier sections">${p._searchMatchAreas.map(x=>`<span>${esc(x)}</span>`).join('')}</div>`:''}<a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">Open Full Dossier →</a></div></article>`;
  }

  function flashcard(p){
    const n=name(p), s=sanskrit(p), rasa=text(p.rasa)||'—', guna=text(p.guna)||'—', virya=p.virya||'—', vipaka=p.vipaka||'—', useful=text(p.useful_part)||'—';
    return `<article class="flashcard" tabindex="0"><div class="flash-inner"><div class="flash-face"><div class="plant-number">#${order(p)}</div><h3>${esc(n)}</h3><div class="big-sanskrit">${esc(s||'Sanskrit name unavailable')}</div><p>${esc(botanical(p))}</p><small>Tap / click to flip</small></div><div class="flash-face flash-back"><h3>${esc(n)}</h3><p><strong>Rasa:</strong> ${esc(rasa)}</p><p><strong>Guna:</strong> ${esc(guna)}</p><p><strong>Virya:</strong> ${esc(virya)}</p><p><strong>Vipaka:</strong> ${esc(vipaka)}</p><p><strong>Useful part:</strong> ${esc(useful)}</p><a class="view-plant" href="./plant.html?id=${encodeURIComponent(p.id)}">Open Full Dossier →</a></div></div></article>`;
  }

  function populateFilters(){
    const configs=[['rasaFilter','rasa','Rasa'],['gunaFilter','guna','Guna'],['viryaFilter','virya','Virya'],['vipakaFilter','vipaka','Vipaka']];
    for(const [id,key,label] of configs){
      const el=document.getElementById(id); if(!el) continue;
      const values=new Set(); masterPlants.forEach(p=>{ const raw=p?.[key]; (Array.isArray(raw)?raw:[raw]).forEach(v=>{if(String(v??'').trim()) values.add(String(v).trim());}); });
      [...values].sort((a,b)=>norm(a).localeCompare(norm(b))).forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;el.appendChild(o);});
      el.addEventListener('change',()=>{filters[key]=el.value;showAll=false;render(searchInput?.value||'');});
    }
  }

  function render(q=''){
    const results=filtered(q), info=document.getElementById('search-result-info');
    const favCount=getFavorites().size;
    if(info) info.textContent=q||Object.values(filters).some(Boolean)||favoritesOnly?`${results.length} result${results.length===1?'':'s'} • ${favCount} saved favourite${favCount===1?'':'s'}`:`${results.length} records in the NCISM-97 library`;
    if(!results.length){plantList.className='plant-grid';plantList.innerHTML='<div class="no-results"><div style="font-size:3rem">🔎</div><h3>No plants found</h3><p>Try a different search term, filter, or clear the filters.</p></div>';return;}
    const visible=q||Object.values(filters).some(Boolean)||favoritesOnly||showAll?results:results.slice(0,initialLimit);
    if(mode==='flash'){
      plantList.className='flash-grid';plantList.innerHTML=visible.map(flashcard).join('');
      plantList.querySelectorAll('.flashcard').forEach(c=>{const flip=()=>c.classList.toggle('flipped');c.addEventListener('click',e=>{if(!e.target.closest('a'))flip()});c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();flip()}})});
    }else{
      plantList.className='plant-grid';plantList.innerHTML=visible.map(card).join('')+(!q&&!Object.values(filters).some(Boolean)&&!favoritesOnly&&!showAll&&results.length>initialLimit?`<div class="plant-list-actions"><p>Showing ${initialLimit} of ${results.length} records.</p><button type="button" id="show-all-plants">Show all ${results.length}</button></div>`:'');
      document.getElementById('show-all-plants')?.addEventListener('click',()=>{showAll=true;render(q)});
      plantList.querySelectorAll('[data-favorite]').forEach(btn=>btn.addEventListener('click',()=>{const fav=getFavorites(),id=String(btn.dataset.favorite);fav.has(id)?fav.delete(id):fav.add(id);saveFavorites(fav);render(searchInput?.value||'');}));
    }
  }

  function showIndexNotice(total){
    const existing=document.getElementById('library-integrity-notice');existing?.remove();
    if(total===EXPECTED_NCISM_COUNT) return;
    const notice=document.createElement('div');notice.id='library-integrity-notice';notice.className='medical-disclaimer';notice.style.margin='0 0 18px';
    notice.innerHTML=`<strong>Library data notice:</strong> ${total} of ${EXPECTED_NCISM_COUNT} NCISM-97 records are currently indexed. Available records remain searchable; missing records are not hidden behind a database error.`;
    plantList.parentElement.insertBefore(notice,plantList);
  }

  function applyUrlState(){
    const params=new URLSearchParams(location.search); const q=params.get('q');
    if(q && searchInput) searchInput.value=q;
  }

  async function loadDossiersForSearch(){
    if(dossierSearchReady || dossierSearchLoading || !masterPlants.length) return;
    dossierSearchLoading=true;
    const hint=document.getElementById('search-help');
    if(hint) hint.textContent='Loading the full plant dossiers for deep search…';
    const concurrency=10;
    for(let i=0;i<masterPlants.length;i+=concurrency){
      const batch=masterPlants.slice(i,i+concurrency);
      await Promise.allSettled(batch.map(async p=>{
        try{
          const r=await fetch(`data/plants/${encodeURIComponent(p.id)}.json?v=2`,{cache:'force-cache',headers:{Accept:'application/json'}});
          if(!r.ok) return;
          const d=await r.json();
          p._searchAreas={
            Identity:d.identity, Classification:d.classification, Identification:d.identification,
            'Rasa Panchaka':d.dravyaguna, Dosha:d.dosha, Therapeutics:d.therapeutics,
            Formulations:d.formulations, 'Classical References':d.classical_reference,
            Phytochemistry:d.phytochemistry, 'Modern Information':d.modern_information,
            Student:d.student, Teacher:d.teacher, Doctor:d.doctor, Sources:d.sources
          };
          p._searchDossier=dossierValue(d);
        }catch(_){}
      }));
      const q=searchInput?.value||'';
      if(norm(q)) render(q);
    }
    dossierSearchReady=true; dossierSearchLoading=false;
    if(hint) hint.textContent='Deep search is ready: names, identity, morphology, Rasa Panchaka, indications, formulations, classical references, exam points and other dossier data.';
    render(searchInput?.value||'');
  }

  async function load(){
    plantList.setAttribute('aria-busy','true');
    try{
      const [ir]=await Promise.all([fetch(INDEX_URL,{cache:'no-store',headers:{Accept:'application/json'}}),loadCovers()]);
      if(!ir.ok) throw new Error(`Index request failed: ${ir.status}`);
      const data=await ir.json(); const rows=Array.isArray(data)?data:(Array.isArray(data?.plants)?data.plants:[]);
      masterPlants=rows.filter(isNCISM).sort((a,b)=>order(a)-order(b));
      if(!masterPlants.length) throw new Error('No valid NCISM-97 records found in plant-index.json');
      showIndexNotice(masterPlants.length);populateFilters();applyUrlState();render(searchInput?.value||'');
      if(norm(searchInput?.value||'')) await loadDossiersForSearch();
    }catch(e){
      console.error('DravyaGuna library load error:',e);
      plantList.innerHTML='<div class="plant-error"><h3>Plant database unavailable</h3><p>The plant index could not be loaded. Please refresh after deployment or check your connection.</p><button type="button" class="plant-list-actions" id="retry-library" style="border:0;background:#1b4332;color:#fff;border-radius:9px;padding:10px 16px;font:inherit;font-weight:700;cursor:pointer">Retry</button></div>';
      document.getElementById('retry-library')?.addEventListener('click',load);
    }finally{plantList.setAttribute('aria-busy','false');}
  }

  document.querySelectorAll('[data-mode]').forEach(btn=>btn.addEventListener('click',()=>{mode=btn.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'')}));
  document.querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{categoryFilter=String(btn.dataset.category||'all').toUpperCase();showAll=false;document.querySelectorAll('[data-category]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'')}));
  searchInput?.addEventListener('input',()=>{showAll=false;clearTimeout(window.__dgSearchTimer);window.__dgSearchTimer=setTimeout(async()=>{const q=searchInput.value;render(q);if(norm(q))await loadDossiersForSearch();},80)});
  document.getElementById('jumpButton')?.addEventListener('click',()=>{const n=Number(document.getElementById('ncismJump')?.value),p=masterPlants.find(x=>order(x)===n);if(p)location.href=`./plant.html?id=${encodeURIComponent(p.id)}`});
  document.getElementById('ncismJump')?.addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('jumpButton')?.click()});
  document.getElementById('favoritesToggle')?.addEventListener('click',()=>{favoritesOnly=!favoritesOnly;showAll=false;const b=document.getElementById('favoritesToggle');b.classList.toggle('active',favoritesOnly);b.textContent=favoritesOnly?'★ Favourites':'☆ Favourites';render(searchInput?.value||'')});
  document.getElementById('clearFilters')?.addEventListener('click',()=>{Object.keys(filters).forEach(k=>filters[k]='');document.querySelectorAll('.filter-select').forEach(x=>x.value='');favoritesOnly=false;showAll=false;categoryFilter='all';document.querySelectorAll('[data-category]').forEach(x=>x.classList.toggle('active',String(x.dataset.category||'all').toUpperCase()==='ALL'));const b=document.getElementById('favoritesToggle');if(b){b.classList.remove('active');b.textContent='☆ Favourites';}if(searchInput)searchInput.value='';render('');});
  load();
});
