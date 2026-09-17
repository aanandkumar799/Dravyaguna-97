(()=>{
  const $=id=>document.getElementById(id);
  const clean=v=>String(v??'').trim();
  const arr=v=>Array.isArray(v)?v.map(clean).filter(Boolean):(clean(v)?[clean(v)]:[]);
  const esc=v=>clean(v).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\':'&#039;','"':'&quot;'}[c]||c));
  const label=p=>p.name||p.identity?.name||p.classical_sanskrit_name||p.id;
  const sans=p=>p.sanskrit_name||p.identity?.sanskrit_name||'';
  const bot=p=>p.botanical_name||p.identity?.botanical_name||'';
  const get=(p,path,alt='')=>{let v=p;for(const k of path.split('.'))v=v?.[k];return v??alt};
  const sel=$('plant'),search=$('search'),work=$('work'); if(!sel||!work)return;
  const fields=[
    ['whole_plant','Whole plant / habit','Overall habit, size and distinctive plant form.'],
    ['root','Root','Shape, colour, texture and diagnostic root features.'],
    ['stem','Stem','Type, surface, branching, nodes and other features.'],
    ['leaf','Leaf','Arrangement, shape, margin, venation and surface.'],
    ['flower','Flower','Colour, arrangement, inflorescence and diagnostic features.'],
    ['fruit','Fruit','Type, shape, colour, surface and distinguishing features.'],
    ['seed','Seed','Shape, size, colour, surface and diagnostic characters.'],
    ['bark','Bark','Colour, texture, thickness and diagnostic characters.']
  ];
  let plants=[];
  function populate(list,keep=''){
    sel.innerHTML='<option value="">Select a plant…</option>'+list.map(p=>`<option value="${esc(p.id)}">#${p.order||''} — ${esc(label(p))}${sans(p)?' — '+esc(sans(p)):''}</option>`).join('');
    if(keep&&list.some(p=>p.id===keep))sel.value=keep;
  }
  async function detail(id,indexRecord){
    try{const r=await fetch(`data/plants/${encodeURIComponent(id)}.json`,{cache:'no-store'});if(r.ok)return await r.json()}catch(e){}
    try{const r=await fetch('plants.json',{cache:'no-store'});const data=await r.json();const list=Array.isArray(data)?data:data.plants||[];return list.find(p=>p?.id===id)||indexRecord}catch(e){return indexRecord}
  }
  function render(p){
    if(!p){work.innerHTML='<div class="empty">Select a plant to begin practical identification.</div>';return}
    const d=p.identification||{},c=p.classification||{},i=p.identity||{},meta=p.metadata||{};
    const grahya=arr(d.grahya_lakshana||d.grahyaLakshana||d.identification_points);
    const checks=fields.map(([k,t,h])=>{const v=d[k]||c[k]||h;return `<label class="check"><input type="checkbox" data-feature="${k}"><span><strong>${t}</strong><small>${esc(v)}</small></span></label>`}).join('');
    const organ=arr(d.organoleptic||d.organoleptic_characters||d.organoleptic_features);
    const organHtml=organ.length?`<div class="panel" style="margin-top:16px;padding:15px;background:#f7faf7"><strong style="color:#1b4332">Rupa • Sparsha • Gandha • Rasa / Organoleptic notes</strong><p>${esc(organ.join(' • '))}</p></div>`:'';
    const grahyaHtml=grahya.length?`<div class="panel" style="margin-top:16px;padding:15px;background:#fffaf0;border-left:4px solid #d4a373"><strong style="color:#1b4332">✓ Grahya Lakshana / Key identification points</strong><ul style="margin-bottom:0">${grahya.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`:'';
    const images=p.images||{};
    const imageParts=[['whole_plant','Whole plant'],['habit','Habit'],['root','Root'],['stem','Stem'],['leaf','Leaf'],['flower','Flower'],['fruit','Fruit'],['seed','Seed'],['bark','Bark']].filter(([k])=>images[k]);
    const gallery=imageParts.length?`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:16px">${imageParts.map(([k,t])=>`<figure style="margin:0;border:1px solid #dfe8df;border-radius:10px;padding:8px;background:#fff"><img src="${esc(images[k])}" alt="${esc(label(p)+' '+t)}" loading="lazy" style="width:100%;height:130px;object-fit:cover;border-radius:7px"><figcaption style="font-size:.82rem;color:#66736b;margin-top:5px">${esc(t)}</figcaption></figure>`).join('')}</div>`:'';
    work.innerHTML=`<div class="plant-head"><div><span class="badge">NCISM #${esc(p.order||'')}</span><h2>${esc(label(p))}</h2><div>${esc(sans(p))}${bot(p)?' • '+esc(bot(p)):''}</div></div><span class="score" id="score">0 / 8 checked</span></div><p><strong>Identification description:</strong> ${esc(d.description||'No detailed identification description recorded yet.')}</p>${grahyaHtml}<div class="check-grid">${checks}</div>${organHtml}${gallery}<div class="actions"><a class="btn primary" href="plant.html?id=${encodeURIComponent(p.id)}">Open Full Plant Dossier →</a><button class="btn outline" id="reset" type="button">Reset checklist</button></div><p style="margin-top:14px;color:#66736b;font-size:.85rem">Data status: ${esc(meta.status||'working draft')}. Confirm morphological characters with authoritative botany/pharmacognosy sources and specimens.</p>`;
    const boxes=[...work.querySelectorAll('[data-feature]')],score=$('score');
    const update=()=>{if(score)score.textContent=`${boxes.filter(x=>x.checked).length} / ${boxes.length} checked`};
    boxes.forEach(x=>x.addEventListener('change',update));$('reset')?.addEventListener('click',()=>{boxes.forEach(x=>x.checked=false);update()});
  }
  function bind(){
    sel.onchange=async()=>{const p=plants.find(x=>String(x.id)===sel.value);if(!p)return;work.innerHTML='<div class="empty">Loading detailed practical features…</div>';render(await detail(p.id,p))};
    search.oninput=()=>{const q=clean(search.value).toLowerCase();const filtered=plants.filter(p=>[label(p),sans(p),bot(p),p.family,p.identity?.family].join(' ').toLowerCase().includes(q));populate(filtered);};
  }
  Promise.all([fetch('plant-index.json',{cache:'no-store'}).then(r=>r.json()),fetch('plants.json',{cache:'no-store'}).then(r=>r.json())])
   .then(([idx,data])=>{
     const index=Array.isArray(idx)?idx:idx.plants||[], full=Array.isArray(data)?data:data.plants||[], fm=new Map(full.map(p=>[p.id,p]));
     plants=index.filter(p=>p&&p.category==='NCISM-97'&&Number(p.order)>=1&&Number(p.order)<=97).sort((a,b)=>Number(a.order)-Number(b.order)).map(p=>({...p,...(fm.get(p.id)||{})}));
     populate(plants);bind();
     const wanted=new URLSearchParams(location.search).get('id');if(wanted&&plants.some(p=>p.id===wanted)){sel.value=wanted;sel.onchange()}
   }).catch(()=>{sel.innerHTML='<option>NCISM plant database unavailable</option>';work.innerHTML='<div class="empty">Unable to load the practical identification database.</div>'});
})();