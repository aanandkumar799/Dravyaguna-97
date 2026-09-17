document.addEventListener('DOMContentLoaded', () => {
  const plantList = document.getElementById('plant-list');
  const searchInput = document.getElementById('searchInput') || document.getElementById('search');
  if (!plantList) return;

  const url = file => new URL(file, window.location.href).href;
  const INDEX_URL = url('data/plants-index.json?v=97');
  const INDEX_FALLBACK = url('plant-index.json?v=97');
  const MANIFEST_URL = url('data/curated-image-manifest.json?v=2');

  let masterPlants = [];
  let mode = 'grid';
  let categoryFilter = 'all';
  let showAll = false;
  const initialLimit = 24;

  const esc = value => String(value ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#039;');
  const normalize = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').replace(/\s+/g,' ').trim();
  const text = value => Array.isArray(value) ? value.map(text).join(' ') : (value && typeof value === 'object' ? Object.values(value).map(text).join(' ') : String(value ?? ''));
  const name = p => p?.name || p?.identity?.name || p?.classical_sanskrit_name?.split(' (')[0] || '';
  const sanskrit = p => p?.sanskrit_name || p?.identity?.sanskrit_name || p?.classical_sanskrit_name || '';
  const botanical = p => p?.botanical_name || p?.identity?.botanical_name || '';
  const family = p => p?.family || p?.identity?.family || '';
  const order = p => Number.isFinite(Number(p?.order)) ? Number(p.order) : 9999;
  const category = p => String(p?.category || p?.syllabus_marker || '').toUpperCase() === 'NCISM-97' ? 'NCISM-97' : '';

  function score(p, query) {
    const q = normalize(query); if (!q) return 0;
    const fields = [[name(p),1200],[sanskrit(p),1100],[p.transliteration,1050],[botanical(p),1000],[p.english_name||p.identity?.english_name||p.english_common_name,900],[family(p),800],[p.id,750],[p.search_text,200]];
    let total = 0;
    for (const [value, points] of fields) {
      const x = normalize(value); if (!x) continue;
      if (x === q) total += points;
      else if (x.startsWith(q)) total += Math.floor(points * .65);
      else if (x.includes(q)) total += Math.floor(points * .45);
    }
    return total;
  }

  function filtered(query='') {
    let list = masterPlants.filter(p => categoryFilter === 'all' || category(p) === categoryFilter);
    if (!normalize(query)) return list;
    return list.map(p => ({p, score: score(p, query)})).filter(x => x.score > 0).sort((a,b) => b.score-a.score || order(a.p)-order(b.p)).map(x => x.p);
  }

  function fallbackSvg(label) {
    const safe = String(label||'Plant').replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#039;'}[c]||c));
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf5ef"/><text x="400" y="220" text-anchor="middle" font-family="Arial,sans-serif" font-size="76">🌿</text><text x="400" y="305" text-anchor="middle" font-family="Arial,sans-serif" font-size="30" fill="#1b4332">${safe}</text><text x="400" y="350" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#6b756f">Verified cover photo not yet approved</text></svg>`;
    return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
  }

  // STRICT COVER PHOTO RULE:
  // Cover cards may display ONLY an approved WHOLE-PLANT image from the curated registry.
  // Never use habit, leaf, bark, flower, fruit, root or stem as a cover fallback.
  // Never perform live keyword image searches here. Never use an unverified candidate.
  // Never reuse another plant's image. If no approved image exists, show a placeholder.
  let coverRegistry = new Map();

  async function loadCoverRegistry() {
    try {
      const r = await fetch(MANIFEST_URL, {cache:'no-store', headers:{Accept:'application/json'}});
      if (!r.ok) return;
      const manifest = await r.json();
      for (const rec of (Array.isArray(manifest?.records) ? manifest.records : [])) {
        if (!rec || String(rec.part) !== 'whole_plant') continue;
        if (!rec.image_path || !/^https?:\/\//i.test(String(rec.image_path))) continue;
        if (!['verified','verified-external'].includes(String(rec.verification_status))) continue;
        if (!rec.source_url || !rec.source_name || !rec.verified_botanical_name) continue;
        const pid = String(rec.plant_id || '');
        if (pid && !coverRegistry.has(pid)) coverRegistry.set(pid, rec);
      }
    } catch (e) { /* strict empty registry is intentional */ }
  }

  function coverFor(p) {
    const rec = coverRegistry.get(String(p?.id || ''));
    if (!rec) return null;
    if (normalize(rec.verified_botanical_name) !== normalize(botanical(p))) return null;
    return rec;
  }

  function card(p) {
    const n = name(p), id = String(p.id||'');
    const rec = coverFor(p);
    const imageHtml = rec
      ? `<img src="${esc(rec.image_path)}" alt="${esc(n)} — verified whole-plant photograph" loading="lazy" decoding="async" data-plant-id="${esc(id)}" data-cover-verified="true" title="Verified whole-plant photograph • ${esc(rec.source_name)}">`
      : `<img src="${fallbackSvg(n || 'Plant')}" alt="${esc(n||'Plant')} — verified whole-plant photograph unavailable" loading="lazy" data-plant-id="${esc(id)}" data-cover-unavailable="true">`;
    return `<article class="plant-card" data-plant-id="${esc(id)}"><div class="plant-image">${imageHtml}</div><div class="plant-card-content"><div class="plant-card-top"><span class="plant-number">#${order(p)}</span><span class="syllabus-marker">NCISM-97</span></div><h3>${esc(n)}</h3>${sanskrit(p)?`<p class="plant-sanskrit">${esc(sanskrit(p))}</p>`:''}${botanical(p)?`<p class="plant-botanical"><em>${esc(botanical(p))}</em></p>`:''}${p.english_name||p.english_common_name?`<p class="plant-english">${esc(p.english_name||p.english_common_name)}</p>`:''}${family(p)?`<p class="plant-family"><strong>Family:</strong> ${esc(family(p))}</p>`:''}<a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">Open Full Dossier →</a></div></article>`;
  }

  function flashcard(p) {
    const n=name(p), s=sanskrit(p), rasa=text(p.rasa)||text(p.dravya_guna?.rasa)||'—', guna=text(p.guna)||text(p.dravya_guna?.guna)||'—';
    const virya=p.virya||p.dravya_guna?.virya||'—', vipaka=p.vipaka||p.dravya_guna?.vipaka||'—', useful=text(p.useful_part)||text(p.identity?.useful_part)||'—';
    return `<article class="flashcard" tabindex="0" aria-label="Flashcard for ${esc(n)}"><div class="flash-inner"><div class="flash-face"><div class="plant-number">#${order(p)}</div><h3>${esc(n)}</h3><div class="big-sanskrit">${esc(s||'Sanskrit name unavailable')}</div><p>${esc(botanical(p))}</p><small>Tap / click to flip</small></div><div class="flash-face flash-back"><h3>${esc(n)}</h3><p><strong>Rasa:</strong> ${esc(rasa)}</p><p><strong>Guna:</strong> ${esc(guna)}</p><p><strong>Virya:</strong> ${esc(virya)}</p><p><strong>Vipaka:</strong> ${esc(vipaka)}</p><p><strong>Useful part:</strong> ${esc(useful)}</p><a class="view-plant" href="./plant.html?id=${encodeURIComponent(p.id)}">Open Full Dossier →</a></div></div></article>`;
  }

  function render(query='') {
    const results = filtered(query);
    const info = document.getElementById('search-result-info');
    if (info) info.textContent = query ? `${results.length} result${results.length===1?'':'s'} found for “${query}”` : `${results.length} record${results.length===1?'':'s'} in ${categoryFilter==='all'?'the NCISM-97 library':categoryFilter}`;
    if (!results.length) { plantList.className='plant-grid'; plantList.innerHTML='<div class="no-results"><div style="font-size:3rem">🔎</div><h3>No plants found</h3><p>Try a Sanskrit name, Roman name, botanical name, family, or NCISM number.</p></div>'; return; }
    const visible = query || showAll ? results : results.slice(0, initialLimit);
    if (mode === 'flash') {
      plantList.className='flash-grid'; plantList.innerHTML=visible.map(flashcard).join('');
      plantList.querySelectorAll('.flashcard').forEach(c=>{const flip=()=>c.classList.toggle('flipped');c.addEventListener('click',e=>{if(!e.target.closest('a'))flip()});c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();flip()}});});
    } else {
      plantList.className='plant-grid';
      plantList.innerHTML=visible.map(card).join('') + (!query&&!showAll&&results.length>initialLimit ? `<div class="plant-list-actions"><p>Showing ${initialLimit} of ${results.length} records.</p><button type="button" id="show-all-plants">Show all ${results.length}</button></div>` : '');
      plantList.querySelectorAll('img[data-cover-verified]').forEach(img=>img.addEventListener('error',()=>{const alt=img.alt.replace(/ — verified whole-plant photograph$/,'');img.src=fallbackSvg(alt);img.removeAttribute('data-cover-verified');img.dataset.coverUnavailable='true';img.alt=alt+' — verified whole-plant photograph unavailable';},{once:true}));
      document.getElementById('show-all-plants')?.addEventListener('click',()=>{showAll=true;render(query)});
    }
  }

  async function load() {
    plantList.setAttribute('aria-busy','true');
    try {
      const [indexResponse] = await Promise.all([
        fetch(INDEX_URL,{cache:'no-store',headers:{Accept:'application/json'}}),
        loadCoverRegistry()
      ]);
      let data = indexResponse.ok ? await indexResponse.json() : null;
      if (!data) {
        const r=await fetch(INDEX_FALLBACK,{cache:'no-store',headers:{Accept:'application/json'}});
        if(r.ok) data=await r.json();
      }
      const raw = Array.isArray(data?.plants) ? data.plants : [];
      masterPlants = raw.filter(p=>category(p)==='NCISM-97' && order(p)>=1 && order(p)<=97).sort((a,b)=>order(a)-order(b));
      if (masterPlants.length !== 97) throw new Error(`Expected 97 NCISM records, received ${masterPlants.length}`);
      categoryFilter='all';
      render('');
    } catch (e) {
      plantList.innerHTML='<div class="plant-error"><h3>Plant database unavailable</h3><p>The canonical NCISM-97 index could not be loaded. Please refresh after deployment.</p></div>';
    } finally { plantList.setAttribute('aria-busy','false'); }
  }

  document.querySelectorAll('[data-mode]').forEach(btn=>btn.addEventListener('click',()=>{mode=btn.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'');}));
  document.querySelectorAll('[data-category]').forEach(btn=>btn.addEventListener('click',()=>{categoryFilter=btn.dataset.category;showAll=false;document.querySelectorAll('[data-category]').forEach(x=>x.classList.toggle('active',x===btn));render(searchInput?.value||'');}));
  searchInput?.addEventListener('input',()=>{showAll=false;clearTimeout(window.__dgSearchTimer);window.__dgSearchTimer=setTimeout(()=>render(searchInput.value),80);});
  document.getElementById('jumpButton')?.addEventListener('click',()=>{const n=Number(document.getElementById('ncismJump')?.value);if(n>=1&&n<=97){const p=masterPlants.find(x=>order(x)===n);if(p)location.href=`./plant.html?id=${encodeURIComponent(p.id)}`;}});
  document.getElementById('ncismJump')?.addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('jumpButton')?.click();});

  load();
});
