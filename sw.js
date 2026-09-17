const CACHE_NAME = 'dravya-guna-97-v8';
const APP_SHELL = ['./','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html','./style.css','./responsive-fix.css','./plant-dossier-layout.css','./academic-enhancements.css','./academic-enhancements.js','./cover-image-fix.js','./image-gallery-delay.js','./image-gallery-fix.js','./data/curated-image-manifest.json','./manifest.json','./404.html','./robots.txt','./sitemap.xml','./favicon.svg','./images/favicon.png'];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const request=event.request;if(request.method!=='GET')return;const url=new URL(request.url);if(url.origin!==self.location.origin)return;
  if(url.pathname.endsWith('.json')){event.respondWith(fetch(request,{cache:'no-store'}).then(r=>{if(r&&r.ok){const c=r.clone();caches.open(CACHE_NAME).then(x=>x.put(request,c))}return r}).catch(()=>caches.match(request)));return}
  if(request.mode==='navigate'||url.pathname.endsWith('.html')){event.respondWith(fetch(request).then(async response=>{if(!response||!response.ok)return response;let out=response;try{const html=await response.clone().text();let injected=html;if(!injected.includes('cover-image-fix.js'))injected=injected.replace('</body>','<script src="./cover-image-fix.js" defer></script></body>');if(url.pathname.endsWith('/plant.html')&&!injected.includes('image-gallery-delay.js'))injected=injected.replace('</body>','<script src="./image-gallery-delay.js" defer></script></body>');if(injected!==html)out=new Response(injected,{status:response.status,statusText:response.statusText,headers:{'Content-Type':'text/html; charset=UTF-8','Cache-Control':'no-cache'}})}catch(e){console.warn('Image script injection failed',e)}const c=out.clone();caches.open(CACHE_NAME).then(x=>x.put(request,c));return out}).catch(()=>caches.match(request).then(c=>c||caches.match('./index.html'))));return}
  event.respondWith(caches.match(request).then(c=>c||fetch(request).then(r=>{if(r&&r.status===200&&r.type==='basic'){const x=r.clone();caches.open(CACHE_NAME).then(k=>k.put(request,x))}return r}).catch(()=>caches.match('./index.html'))));
});
