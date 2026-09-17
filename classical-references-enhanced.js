(()=>{
const $=id=>document.getElementById(id),list=$('list'),info=$('info'),search=$('search');
if(!list||!info||!search)return;
const VERSION='100';
const clean=v=>String(v??'').trim();
const arr=v=>Array.isArray(v)?v.filter(x=>x!==null&&x!==undefined&&clean(x)!==''):[];
const name=p=>p.name||p.identity?.name||p.classical_sanskrit_name||p.id;
const sans=p=>p.sanskrit_name||p.identity?.sanskrit_name||'';
const bot=p=>p.botanical_name||p.identity?.botanical_name||'';
const esc=v=>clean(v).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\':'&#039;','"':'&quot;'}[c]||c));
let plants=[];
function refs(p){
 const c=p.classical_reference||{},out=[];
 arr(c.shlokas).forEach(x=>{
   if(typeof x==='object'){
     const value=x.text||x.shloka||'';
     if(value||x.reference||x.source)out.push({kind:'Shloka',value,source:x.source||x.reference||'Classical source',extra:[x.transliteration,x.meaning,x.chapter].filter(Boolean).join(' • '),verified:x.verified===true});
   }else out.push({kind:'Shloka',value:String(x),source:'Classical source',extra:'',verified:false});
 });
 arr(c.nighantu_references).forEach(x=>out.push({kind:'Nighantu',value:typeof x==='object'?(x.reference||x.text||JSON.stringify(x)):String(x),source:'Nighantu reference',extra:'',verified:false}));
 arr(c.samhita_references).forEach(x=>out.push({kind:'Samhita',value:typeof x==='object'?(x.reference||x.text||JSON.stringify(x)):String(x),source:'Samhita reference',extra:'',verified:false}));
 return out;
}
function render(){
 const q=clean(search.value).toLowerCase(),rows=[];
 plants.forEach(p=>refs(p).forEach(r=>{if(!q||[name(p),sans(p),bot(p),r.kind,r.value,r.source,r.extra].join(' ').toLowerCase().includes(q))rows.push({p,r})}));
 info.textContent=`${rows.length} reference item${rows.length===1?'':'s'} shown across ${plants.length} NCISM plants`;
 if(!rows.length){list.innerHTML='<div class="empty">No classical reference record found for this search.</div>';return}
 list.innerHTML=rows.map(({p,r})=>`<article class="card"><h2>#${esc(p.order||'')} — ${esc(name(p))}</h2><div class="meta">${esc(sans(p))}${bot(p)?' • '+esc(bot(p)):''}</div><div class="block"><div class="label">${esc(r.kind)} • ${esc(r.source)}${r.verified?' • ✓ verified':''}</div><div class="shloka">${esc(r.value||'Reference recorded without shloka text.')}</div>${r.extra?`<div class="meta">${esc(r.extra)}</div>`:''}</div><a class="link" href="plant.html?id=${encodeURIComponent(p.id)}">Open Plant Dossier →</a></article>`).join('');
}
async function loadIndex(){
 const r=await fetch(`plant-index.json?v=${VERSION}`,{cache:'no-store'});
 if(!r.ok)throw new Error('plant index unavailable');
 const data=await r.json();
 const rows=Array.isArray(data)?data:data.plants||[];
 if(!rows.length)throw new Error('empty plant index');
 return rows;
}
loadIndex().then(async index=>{
 index=index.filter(p=>p?.category==='NCISM-97'&&Number(p.order)>=1&&Number(p.order)<=97).sort((a,b)=>Number(a.order)-Number(b.order));
 plants=await Promise.all(index.map(async p=>{
   try{const r=await fetch(`data/plants/${encodeURIComponent(p.id)}.json?v=${VERSION}`,{cache:'no-store'});return r.ok?await r.json():p}catch(e){return p}
 }));
 render();search.oninput=render;
}).catch(()=>{info.textContent='Unable to load the classical reference database.';list.innerHTML='<div class="empty">Reference database unavailable. Please refresh once after the latest site deployment.</div>'});
})();
