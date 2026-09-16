from pathlib import Path
import re

p=Path('compare.html')
s=p.read_text(encoding='utf-8')

# Stronger mobile layout and 44px effective touch target.
s=s.replace('.multi-compare-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:14px}', '.multi-compare-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}')
s=s.replace('.btn-remove-card{position:absolute;top:9px;right:9px;background:#fee2e2;color:#dc2626;border:1px solid #fca5a5;border-radius:50%;width:27px;height:27px;font-size:.75rem;font-weight:800;cursor:pointer}', '.btn-remove-card{position:absolute;top:4px;right:4px;background:#fee2e2;color:#dc2626;border:1px solid #fca5a5;border-radius:50%;width:44px;height:44px;min-width:44px;min-height:44px;display:grid;place-items:center;font-size:.85rem;font-weight:800;cursor:pointer;line-height:1}')
s=s.replace('@media(max-width:700px){', '@media(max-width:640px){.multi-compare-grid{grid-template-columns:1fr}.compare-card{width:100%}.btn-remove-card{top:4px;right:4px}}@media(max-width:700px){')

# Remove secondary batch fallbacks: comparison should use the canonical index, with optional
# full-record enrichment only when available. The index remains the authoritative 97-record list.
old="""try{const full=await json('plants.json');if(Array.isArray(full))full.forEach(p=>{if(byId.has(String(p.id)))byId.set(String(p.id),merge(byId.get(String(p.id)),p))})}catch(e){console.warn('Detail database unavailable',e)}for(const file of ['plant-batch-24-28.json','plant-batch-29-33.json','plant-batch-34-38.json','plant-batch-39-43.json']){try{const batch=await json(file);if(Array.isArray(batch))batch.forEach(p=>{if(byId.has(String(p.id)))byId.set(String(p.id),merge(byId.get(String(p.id)),p))})}catch(e){console.warn('Batch unavailable',file,e)}}dataset=[...byId.values()].sort((a,b)=>Number(a.order)-Number(b.order));"""
new="""try{const full=await json('plants.json');if(Array.isArray(full))full.forEach(p=>{if(byId.has(String(p.id)))byId.set(String(p.id),merge(byId.get(String(p.id)),p))})}catch(e){console.warn('Optional detail database unavailable; using canonical plant index',e)}dataset=[...byId.values()].sort((a,b)=>Number(a.order)-Number(b.order));"""
if old in s:s=s.replace(old,new,1)

# Reconcile only changed cards instead of rebuilding the whole comparison grid on every add/remove.
pattern=r"function render\(\)\{.*?\}\n\$\('addPlantBtn'\)\.addEventListener"
replacement="""function bindRemoveButtons(root){root.querySelectorAll('[data-remove]').forEach(btn=>{if(btn.dataset.bound)return;btn.dataset.bound='1';btn.addEventListener('click',()=>removePlant(btn.dataset.remove))})}
function render(){const grid=$('multiCompareGrid');$('compareCounter').textContent=`${selectedPlantIds.length} / ${MAX} Selected`;$('addPlantBtn').disabled=selectedPlantIds.length>=MAX||!dataset.length;const wanted=new Set(selectedPlantIds.map(String));grid.querySelectorAll('.compare-card[data-plant-id]').forEach(node=>{if(!wanted.has(String(node.dataset.plantId)))node.remove()});grid.querySelectorAll('.empty,.compare-error').forEach(node=>node.remove());let slot=grid.querySelector('.slot-card');selectedPlantIds.forEach(id=>{if(!grid.querySelector(`.compare-card[data-plant-id=\"${CSS.escape(String(id))}\"]`)){const p=dataset.find(x=>String(x.id)===String(id));if(p){if(!slot)grid.insertAdjacentHTML('beforeend','<div class=\"slot-card\"></div>');slot=grid.querySelector('.slot-card');slot.insertAdjacentHTML('beforebegin',card(p));}}});if(!selectedPlantIds.length){if(slot)slot.remove();grid.insertAdjacentHTML('afterbegin',dataset.length?'<div class=\"empty\" style=\"grid-column:1/-1\"><strong>Select a plant above</strong><br>Click ➕ Add Plant to start your comparison.</div>':'');return}if(selectedPlantIds.length<MAX){if(!slot){grid.insertAdjacentHTML('beforeend','<div class=\"slot-card\"><div><strong>＋ Add Plant Slot</strong>Choose another plant above.<br><small>Up to 5 plants can be compared.</small></div></div>')}else{slot.innerHTML='<div><strong>＋ Add Plant Slot</strong>Choose another plant above.<br><small>Up to 5 plants can be compared.</small></div>'}}else if(slot)slot.remove();bindRemoveButtons(grid)}
$('addPlantBtn').addEventListener"""
s2,n=re.subn(pattern,replacement,s,flags=re.S)
if n==1:s=s2
else: print('render function pattern not found; retaining existing renderer')

# Mark generated cards with their stable plant key.
s=s.replace('<article class="compare-card"><button', '<article class="compare-card" data-plant-id="${esc(p.id)}"><button',1)

p.write_text(s,encoding='utf-8')
print('compare.html hardened')
