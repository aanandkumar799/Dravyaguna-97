(function(){
  const BATCHES=['plant-batch-24-28.json','plant-batch-29-33.json','plant-batch-34-38.json','plant-batch-39-43.json','plant-batch-44-48.json','plant-batch-49-53.json','plant-batch-54-58.json','plant-batch-59-63.json','plant-batch-64-68.json','plant-batch-69-73.json','plant-batch-74-78.json','plant-batch-79-83.json','plant-batch-84-88.json','plant-batch-89-93.json','plant-batch-94-98.json'];
  const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
  const text=v=>Array.isArray(v)?v.map(x=>typeof x==='object'?Object.values(x).join(' — '):String(x)).filter(Boolean).join(', '):typeof v==='object'&&v!==null?Object.entries(v).map(([k,x])=>`${k}: ${typeof x==='object'?text(x):x}`).join(' · '):String(v??'');
  const row=(k,v)=>{const s=text(v).trim();return s?`<div class="info-row"><div class="info-label">${esc(k)}</div><div class="info-value">${esc(s)}</div></div>`:''};
  const section=(title,icon,body)=>`<section class="plant-section"><div class="section-heading"><span class="section-icon" aria-hidden="true">${icon}</span><div><h2>${esc(title)}</h2></div></div><div class="identity-grid">${body}</div></section>`;
  async function get(url){try{const r=await fetch(url,{cache:'no-store',headers:{Accept:'application/json'}});return r.ok?await r.json():null}catch(e){return null}}
  async function find(){
    const id=new URLSearchParams(location.search).get('id'); if(!id)return null;
    const idx=await get('./plant-index.json'); const list=Array.isArray(idx?.plants)?idx.plants:[];
    const ref=list.find(x=>String(x.id||'').toLowerCase()===id.toLowerCase()||String(x.order||'')===id); if(!ref)return null;
    const names=new Set([String(ref.id||''),String(ref.name||'').toLowerCase(),String(ref.botanical_name||'').toLowerCase()].filter(Boolean));
    const batches=await Promise.all(BATCHES.map(x=>get('./'+x)));
    for(const batch of batches){if(!Array.isArray(batch))continue;for(const p of batch){const n=String(p?.identity?.name||p?.name||'').toLowerCase(),b=String(p?.identity?.botanical_name||p?.botanical_name||'').toLowerCase(),pid=String(p?.id||'').toLowerCase();if(names.has(n)||names.has(b)||names.has(pid))return {...ref,...p,identity:{...ref,...(p.identity||{})}}}}
    return ref;
  }
  function render(p){
    const root=document.getElementById('plant-content'); if(!root)return;
    const i=p.identity||{},c=p.classification||{},d=p.identification||{},g=p.dravya_guna||p.dravyaguna||{},t=p.therapeutics||{},cl=p.classical_reference||{},m=p.metadata||{};
    const name=i.name||p.name||'Plant', bot=i.botanical_name||p.botanical_name||'';
    const identity=[row('Sanskrit Name',i.sanskrit_name),row('Transliteration',i.transliteration),row('Botanical Name',bot),row('Family',i.family),row('English Name',i.english_name),row('Hindi Name',i.hindi_name),row('Regional Names',i.regional_names),row('Synonyms',i.synonyms)].join('');
    const classification=[row('Kingdom',c.kingdom),row('Habit',c.habit),row('Habitat',c.habitat),row('Distribution',c.distribution)].join('');
    const identification=[row('Description',d.description),row('Whole Plant',d.whole_plant),row('Root',d.root),row('Stem',d.stem),row('Leaf',d.leaf),row('Flower',d.flower),row('Fruit',d.fruit),row('Seed',d.seed),row('Bark',d.bark),row('Identification Points',d.identification_points)].join('');
    const dg=[row('Rasa',g.rasa),row('Guna',g.guna),row('Virya',g.virya),row('Vipaka',g.vipaka),row('Prabhava',g.prabhava),row('Karma',g.karma)].join('');
    const therapy=[row('Useful Part',t.useful_part),row('Indications',t.indications),row('Therapeutic Actions',t.therapeutic_actions||t.actions),row('Precautions',t.precautions||m.safety_note),row('Contraindications',t.contraindications)].join('');
    const classical=[row('Shlokas',cl.shlokas||cl.text),row('Nighantu References',cl.nighantu_references),row('Samhita References',cl.samhita_references)].join('');
    root.innerHTML=`<div class="plant-hero"><div><div class="eyebrow">DravyaGuna 97 · NCISM reference</div><h1>${esc(name)}</h1><p><em>${esc(bot)}</em></p><p class="status-badge">${esc(m.status||'Record loaded from verified plant database')}</p></div></div>${section('Identity','🌿',identity)}${section('Classification','🔬',classification)}${section('Practical Identification','🔎',identification)}${section('Dravya Guna','⚗️',dg)}${section('Therapeutics','🩺',therapy)}${section('Classical References','📜',classical)}<section class="plant-section"><div class="section-heading"><span class="section-icon">🖼️</span><div><h2>Plant-part image gallery</h2></div></div><div id="plant-gallery-host" class="gallery-grid"></div></section>`;
    root.setAttribute('aria-busy','false');
    window.dispatchEvent(new CustomEvent('dg-dossier-ready',{detail:{plant:p}}));
  }
  function start(){setTimeout(async()=>{const root=document.getElementById('plant-content');if(!root)return;const current=root.textContent||'';if(!/No plant selected|Plant data unavailable|Plant data not found|No data found|could not be loaded/i.test(current)&&!current.includes('Loading plant information'))return;const p=await find();if(p)render(p);else{root.innerHTML='<div class="error-box"><div class="error-icon">⚠️</div><h2>Plant record temporarily unavailable</h2><p>The plant index was reached, but its detailed record could not be matched. The background database audit will retry it automatically.</p><a href="plants.html" class="plant-button">← Back to Plant Library</a></div>';root.setAttribute('aria-busy','false')}},3500)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
