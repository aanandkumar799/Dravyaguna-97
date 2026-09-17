(function(){
function load(){if(document.getElementById('image-gallery-fix-script'))return;const s=document.createElement('script');s.id='image-gallery-fix-script';s.src='./image-gallery-fix.js';document.body.appendChild(s)}
function watch(){const h=document.getElementById('plant-gallery-host');if(!h){setTimeout(watch,250);return}const done=()=>h.querySelectorAll('.gallery-item').length>=9;if(done()){setTimeout(load,800);return}const mo=new MutationObserver(()=>{if(done()){mo.disconnect();setTimeout(load,800)}});mo.observe(h,{childList:true,subtree:true});setTimeout(()=>{mo.disconnect();load()},8000)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch);else watch();
})();
