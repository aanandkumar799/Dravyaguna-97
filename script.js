document.addEventListener('DOMContentLoaded', () => {
  const plantList = document.getElementById('plant-list');
  const searchInput = document.getElementById('searchInput') || document.getElementById('search');
  if (!plantList) return;
  const indexURL = new URL('plant-index.json', window.location.href).href;
  const fallbackURL = new URL('plants.json', window.location.href).href;
  const batchURLs = ['plant-batch-24-28.json', 'plant-batch-29-33.json', 'plant-batch-34-38.json', 'plant-batch-39-43.json'].map(x => new URL(x, window.location.href).href);
  let masterPlants = [];
  let searchTimer;
  let mode = 'grid';
  let categoryFilter = 'all';
  let showAll = false;
  const initialLimit = 24;
  const esc = v => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#039;');
  const normalize = v => String(v ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').replace(/\s+/g,' ').trim();
  const text = v => Array.isArray(v) ? v.map(text).join(' ') : (v && typeof v === 'object' ? Object.values(v).map(text).join(' ') : String(v ?? ''));
  const name = p => p.name || p.identity?.name || '';
  const sanskrit = p => p.sanskrit_name || p.identity?.sanskrit_name || '';
  const botanical = p => p.botanical_name || p.identity?.botanical_name || '';
  const family = p => p.family || p.identity?.family || '';
  const order = p => Number.isFinite(Number(p.order)) ? Number(p.order) : 9999;
  const category = p => p.category === 'Supplementary' ? 'Supplementary' : 'NCISM-97';
  const image = p => p.images?.whole_plant || p.images?.habit || p.images?.leaf || '';
  const libraryOrder = (a, b) => {
    const ca = category(a), cb = category(b);
    if (ca !== cb) return ca === 'NCISM-97' ? -1 : 1;
    if (ca === 'NCISM-97') return order(a) - order(b) || name(a).localeCompare(name(b));
    return name(a).localeCompare(name(b));
  };
  function score(p, q) {
    const query = normalize(q); if (!query) return 0;
    const fields = [[name(p),1200],[sanskrit(p),1100],[p.transliteration,1050],[botanical(p),1000],[p.english_name || p.identity?.english_name,900],[family(p),800],[p.id,750],[p.search_text,200]];
    let total = 0;
    for (const [value, points] of fields) {
      const x = normalize(value); if (!x) continue;
      if (x === query) total += points;
      else if (x.startsWith(query)) total += Math.floor(points * .65);
      else if (x.includes(query)) total += Math.floor(points * .45);
    }
    return total;
  }
  function filtered(q='') {
    let list = masterPlants.filter(p => categoryFilter === 'all' || category(p) === categoryFilter);
    if (!normalize(q)) return list;
    return list.map(p => ({p, s: score(p,q)})).filter(x => x.s > 0).sort((a,b) => b.s-a.s || libraryOrder(a.p,b.p)).map(x => x.p);
  }
  function fallbackSvg(label) {
    const safe = String(label || 'Plant').replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#039;'}[c]));
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf5ef"/><text x="400" y="235" text-anchor="middle" font-family="Arial,sans-serif" font-size="82">🌿</text><text x="400" y="330" text-anchor="middle" font-family="Arial,sans-serif" font-size="30" fill="#1b4332">${safe}</text><text x="400" y="375" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#6b756f">Image not available</text></svg>`;
    return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
  }
  function card(p) {
    const n=name(p), img=image(p), c=category(p), id=String(p.id||''), fallback=fallbackSvg(n || 'Plant');
    const imageHtml = img ? `<img src="${esc(img)}" alt="${esc(n)}" loading="lazy" data-fallback="${esc(fallback)}">` : `<img src="${fallback}" alt="${esc(n || 'Plant')} image placeholder" loading="lazy">`;
    return `<article class="plant-card"><div class="plant-image">${imageHtml}</div><div class="plant-card-content"><div class="plant-card-top"><span class="plant-number">${c==='NCISM-97'?'#'+order(p):'Supplementary'}</span><span class="syllabus-marker">${c}</span></div><h3>${esc(n)}</h3>${sanskrit(p)?`<p class="plant-sanskrit">${esc(sanskrit(p))}</p>`:''}${botanical(p)?`<p class="plant-botanical"><em>${esc(botanical(p))}</em></p>`:''}${p.english_name?`<p class="plant-english">${esc(p.english_name)}</p>`:''}${family(p)?`<p class="plant-family"><strong>Family:</strong> ${esc(family(p))}</p>`:''}<a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">Open Full Dossier →</a></div></article>`;
  }
  function flashcard(p) {
    const n=name(p), s=sanskrit(p), rasa=text(p.rasa)||'—', guna=text(p.guna)||'—', virya=p.virya||'—', vipaka=p.vipaka||'—', useful=text(p.useful_part)||'—';
    const badge = category(p)==='NCISM-97' ? '#'+order(p) : 'Supplementary';
    return `<article class="flashcard" tabindex="0" aria-label="Flashcard for ${esc(n)}"><div class="flash-inner"><div class="flash-face"><div class="plant-number">${badge}</div><h3>${esc(n)}</h3><div class="big-sanskrit">${esc(s||'Sanskrit name unavailable')}</div><p>${esc(p.botanical_name||p.identity?.botanical_name||'')}</p><small>Tap / click to flip</small></div><div class="flash-face flash-back"><h3>${esc(n)}</h3><p><strong>Rasa:</strong> ${esc(rasa)}</p><p><strong>Guna:</strong> ${esc(guna)}</p><p><strong>Virya:</strong> ${esc(virya)}</p><p><strong>Vipaka:</strong> ${esc(vipaka)}</p><p><strong>Useful part:</strong> ${esc(useful)}</p><a class="view-plant" href="./plant.html?id=${encodeURIComponent(p.id)}">Open Full Dossier →</a></div></div></article>`;
  }
  function render(q='') {
    const results=filtered(q), info=document.getElementById('search-result-info');
    if(info) info.textContent=q ? `${results.length} result${results.length===1?'':'s'} found for “${q}”` : `${results.length} record${results.length===1?'':'s'} in ${categoryFilter==='all'?'the library':categoryFilter}`;
    if(!results.length){plantList.className='plant-grid';plantList.innerHTML='<div class="no-results"><div style="font-size:3rem">🔎</div><h3>No plants found</h3><p>Try a Sanskrit name, Roman name, botanical name, family, or NCISM number.</p></div>';return;}
    const visible = q || showAll ? results : results.slice(0,initialLimit);
    if(mode==='flash'){
      plantList.className='flash-grid'; plantList.innerHTML=visible.map(flashcard).join('');
      plantList.querySelectorAll('.flashcard').forEach(c=>{const flip=()=>c.classList.toggle('flipped');c.addEventListener('click',e=>{if(e.target.closest('a'))return;flip();});c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();flip();}});});
    } else {
      plantList.className='plant-grid';
      plantList.innerHTML=visible.map(card).join('') + (!q&&!showAll&&results.length>initialLimit?`<div class="plant-list-actions"><p>Showing ${initialLimit} of ${results.length} records.</p><button type="button" id="show-all-plants">Show all ${results.length}</button></div>`:'');
      plantList.querySelectorAll('img[data-fallback]').forEach(img=>img.addEventListener('error',()=>{img.src=img.dataset.fallback;img.removeAttribute('data-fallback');},{once:true}));
      document.getElementById('show-all-plants')?.addEventListener('click',()=>{showAll=true;render(searchInput?.value||'');});
    }
  }
  function setupControls(){
    document.querySelectorAll('[data-mode]').forEach(btn=>btn.addEventListener('click',()=>{mode=btn.dataset.mode;showAll=true;document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));render(searchInput?.value||'');}));
    document.querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{categoryFilter=btn.dataset.category;showAll=false;document.querySelectorAll('[data-category]').forEach(b=>b.classList.toggle('active',b.dataset.category===categoryFilter));render(searchInput?.value||'');}));
    const jump=()=>{const n=Number(document.getElementById('ncismJump')?.value);if(!n)return;const p=masterPlants.find(x=>category(x)==='NCISM-97'&&order(x)===n);if(p)location.href=`./plant.html?id=${encodeURIComponent(p.id)}`;else alert('NCISM number not found in the current index.');};
    document.getElementById('jumpButton')?.addEventListener('click',jump); document.getElementById('ncismJump')?.addEventListener('keydown',e=>{if(e.key==='Enter')jump();});
  }
  const mergeRecord = (base, patch) => ({...base,...patch,identity:{...(base?.identity||{}),...(patch?.identity||{})},dravya_guna:{...(base?.dravya_guna||{}),...(patch?.dravya_guna||{})},therapeutics:{...(base?.therapeutics||{}),...(patch?.therapeutics||{})},metadata:{...(base?.metadata||{}),...(patch?.metadata||{})}});
  async function load(){
    try {
      let r=await fetch(indexURL,{cache:'no-store',headers:{Accept:'application/json'}});
      if(r.ok){const payload=await r.json();masterPlants=Array.isArray(payload)?payload:(payload.plants||[]);}
      if(masterPlants.length){
        const lookup=await fetch(fallbackURL,{cache:'no-store',headers:{Accept:'application/json'}});
        if(lookup.ok){const full=await lookup.json();if(Array.isArray(full)){const details=new Map(full.map(p=>[p.id,p]));masterPlants=masterPlants.map(item=>mergeRecord(item,details.get(item.id)||{}));}}
      }
      const batchResults = await Promise.all(batchURLs.map(async url => {
        try { const br=await fetch(url,{cache:'no-store',headers:{Accept:'application/json'}}); if(!br.ok) return []; const batch=await br.json(); return Array.isArray(batch) ? batch : []; }
        catch(batchError){ console.warn('Batch data unavailable', url, batchError); return []; }
      }));
      const byId=new Map(masterPlants.map(p=>[String(p.id),p]));
      batchResults.flat().forEach(p=>{const key=String(p.id);byId.set(key,mergeRecord(byId.get(key)||{},p));});
      masterPlants=Array.from(byId.values());
      if(!masterPlants.length){r=await fetch(fallbackURL,{cache:'no-store',headers:{Accept:'application/json'}});if(!r.ok)throw Error('HTTP '+r.status);const data=await r.json();if(!Array.isArray(data))throw Error('Invalid plant database');masterPlants=data;}
      masterPlants=masterPlants.filter(p=>p&&p.id).sort(libraryOrder);
      setupControls();plantList.setAttribute('aria-busy','false');render(searchInput?.value||'');
    } catch(e){console.error(e);plantList.innerHTML=`<div class="plant-error"><h3>Unable to load the plant library</h3><p>${esc(e.message||'Please refresh the page.')}</p></div>`;}
  }
  searchInput?.addEventListener('input',e=>{clearTimeout(searchTimer);showAll=false;searchTimer=setTimeout(()=>render(e.target.value),80);});
  setupControls(); load();
});
