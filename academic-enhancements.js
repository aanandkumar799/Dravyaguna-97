document.addEventListener('DOMContentLoaded',()=>{
 const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/'/g,'&#039;');
 const arr=v=>Array.isArray(v)?v.filter(Boolean):v?[v]:[];
 const norm=v=>String(v??'').toLowerCase().trim();
 const values=v=>arr(v).map(x=>typeof x==='object'?Object.values(x).join(' '):String(x)).filter(Boolean);
 const badge=(v,cls='dg-rasa')=>`<span class="dg-badge ${cls}">${esc(v)}</span>`;
 const plantURL=id=>`./plant.html?id=${encodeURIComponent(id)}`;

 // Library: multi-filter controls and two-plant comparison.
 const list=document.getElementById('plant-list');
 if(list){
  fetch(new URL('plant-index.json',location.href),{cache:'no-store'}).then(r=>r.json()).then(payload=>{
   const plants=Array.isArray(payload)?payload:(payload.plants||[]);
   const families=[...new Set(plants.map(p=>p.family).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));
   const habits=[...new Set(plants.map(p=>p.habit||p.classification?.habit).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));
   const actions=[...new Set(plants.flatMap(p=>values(p.karma||p.therapeutic_actions||p.dravya_guna?.karma)).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
   const panel=document.createElement('div');panel.className='filter-enhancement';panel.innerHTML=`<label>Family<select id="dgFamily"><option value="">All families</option>${families.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label><label>Habit<select id="dgHabit"><option value="">All habits</option>${habits.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label><label>Main Action / Karma<select id="dgAction"><option value="">All actions</option>${actions.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label>`;
   const searchPanel=document.querySelector('.search-panel'); if(searchPanel){const jump=searchPanel.querySelector('.jump-box'); searchPanel.insertBefore(panel,jump||searchPanel.querySelector('#search-result-info'));}
   const meta=new Map(plants.map(p=>[p.id,p]));
   const apply=()=>{const f=norm(document.getElementById('dgFamily')?.value),h=norm(document.getElementById('dgHabit')?.value),a=norm(document.getElementById('dgAction')?.value);list.querySelectorAll('.plant-card').forEach(card=>{const link=card.querySelector('.view-plant');const id=link?.href?new URL(link.href).searchParams.get('id'):'';const p=meta.get(id);if(!p){return}const pf=norm(p.family),ph=norm(p.habit||p.classification?.habit),pa=values(p.karma||p.therapeutic_actions||p.dravya_guna?.karma).join(' ').toLowerCase();card.style.display=(!f||pf.includes(f))&&(!h||ph.includes(h))&&(!a||pa.includes(a))?'':'none';});};
   ['dgFamily','dgHabit','dgAction'].forEach(id=>document.getElementById(id)?.addEventListener('change',apply));
   const decorate=()=>{list.querySelectorAll('.plant-card').forEach(card=>{if(card.dataset.enhanced)return;const link=card.querySelector('.view-plant');if(!link)return;const id=new URL(link.href).searchParams.get('id');const p=meta.get(id);if(!p)return;card.dataset.enhanced='1';const lab=document.createElement('label');lab.className='compare-check';lab.innerHTML=`<input type="checkbox" value="${esc(id)}"> Compare`;card.querySelector('.plant-card-content')?.prepend(lab);});apply();list.querySelectorAll('.compare-check input').forEach(cb=>cb.addEventListener('change',compareChanged));};
   const observer=new MutationObserver(decorate);observer.observe(list,{childList:true,subtree:true});decorate();
  }).catch(()=>{});
 }
 const selected=new Set(JSON.parse(localStorage.getItem('dg97_compare')||'[]').slice(0,2));
 function compareChanged(e){if(e.target.checked){if(selected.size>=2){e.target.checked=false;alert('Select only two plants for Dual Dossier comparison.');return}selected.add(e.target.value)}else selected.delete(e.target.value);localStorage.setItem('dg97_compare',JSON.stringify([...selected]));updateBar();}
 function updateBar(){document.querySelector('.compare-bar')?.remove();if(!selected.size)return;const bar=document.createElement('div');bar.className='compare-bar';bar.innerHTML=`<span>⚖️ ${selected.size}/2 selected</span>${selected.size===2?'<a href="compare.html">Compare plants →</a>':''}<button type="button" id="clearCompare">Clear</button>`;document.body.appendChild(bar);bar.querySelector('#clearCompare').onclick=()=>{selected.clear();localStorage.removeItem('dg97_compare');document.querySelectorAll('.compare-check input').forEach(x=>x.checked=false);bar.remove()};}updateBar();

 // Plant dossier: transform Rasa Panchaka and Classical References into visual cards.
 const id=new URLSearchParams(location.search).get('id');
 if(!id)return;
 const dossierURL=new URL('data/plants/'+encodeURIComponent(id)+'.json',location.href);
 fetch(dossierURL,{cache:'no-store'}).then(r=>r.ok?r.json():null).then(p=>{if(!p)return;const g=p.dravya_guna||p.dravyaguna||{},dos=p.dosha||{},cl=p.classical_reference||{};
  const sections=[...document.querySelectorAll('.plant-section')];
  const findSection=t=>sections.find(s=>s.querySelector('h2')?.textContent.trim()===t);
  const rasaSec=findSection('Rasa Panchaka & Dosha'); if(rasaSec){const body=rasaSec.querySelector('.identity-grid');if(body){const rows=body.querySelectorAll('.info-row');const map={};rows.forEach(r=>map[r.querySelector('.info-label')?.textContent.trim()]=r.querySelector('.info-value'));const out=document.createElement('div');out.className='rasa-badge-container';
    values(g.rasa).forEach(v=>out.innerHTML+=badge(v,'dg-rasa'));values(g.guna).forEach(v=>out.innerHTML+=badge(v,'dg-guna'));if(g.virya)out.innerHTML+=badge(`${g.virya} Veerya`,norm(g.virya).includes('ushna')?'dg-ushna':'dg-sheeta');if(g.vipaka)out.innerHTML+=badge(`${g.vipaka} Vipaka`,'dg-vipaka');values(g.karma).forEach(v=>out.innerHTML+=badge(v,'dg-dosha'));
    [['Vata',dos.vata],['Pitta',dos.pitta],['Kapha',dos.kapha]].forEach(([k,v])=>{if(v)out.innerHTML+=badge(`${k}: ${v}`,'dg-dosha')});
    body.replaceChildren(Object.assign(document.createElement('div'),{className:'info-row'}));const r=body.firstElementChild;r.innerHTML='<div class="info-label">Rasa Panchaka</div>';r.appendChild(out);}}
  }
  const classSec=findSection('Classical References');if(classSec){const body=classSec.querySelector('.identity-grid');if(body){const cards=[];values(cl.nighantu_references).forEach(v=>cards.push(`<article class="shloka-card"><div class="shloka-source">📚 Nighantu Reference</div><div class="shloka-text">${esc(v)}</div></article>`));values(cl.samhita_references).forEach(v=>cards.push(`<article class="shloka-card"><div class="shloka-source">📖 Samhita Reference</div><div class="shloka-text">${esc(v)}</div></article>`));values(cl.shlokas).forEach(v=>{if(typeof v==='object'){cards.push(`<article class="shloka-card"><div class="shloka-source">📜 ${esc(v.source||v.reference||'Classical Shloka')}</div><div class="shloka-text">${esc(v.text||'')}</div>${v.transliteration?`<div class="shloka-translit">${esc(v.transliteration)}</div>`:''}${v.meaning?`<div class="shloka-meaning"><strong>Meaning:</strong> ${esc(v.meaning)}</div>`:''}</article>`)}else cards.push(`<article class="shloka-card"><div class="shloka-source">📜 Classical Shloka</div><div class="shloka-text">${esc(v)}</div></article>`)});if(cards.length)body.innerHTML=`<div class="classical-reference-grid">${cards.join('')}</div>`;}}
 });
});
