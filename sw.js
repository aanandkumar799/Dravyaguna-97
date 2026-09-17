const CACHE_NAME = 'dravya-guna-97-v5';
const APP_SHELL = ['./','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html','./style.css','./responsive-fix.css','./plant-dossier-layout.css','./academic-enhancements.css','./academic-enhancements.js','./image-gallery-fix.js','./manifest.json','./404.html','./robots.txt','./sitemap.xml','./favicon.svg','./images/favicon.png'];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.endsWith('.json')) {
    event.respondWith(fetch(request, {cache:'no-store'}).then(response => {
      if (response && response.ok) { const copy=response.clone(); caches.open(CACHE_NAME).then(cache=>cache.put(request,copy)); }
      return response;
    }).catch(()=>caches.match(request)));
    return;
  }

  if (request.mode === 'navigate' || url.pathname.endsWith('.html')) {
    event.respondWith(fetch(request).then(async response => {
      if (!response || !response.ok) return response;
      let finalResponse=response;
      if (url.pathname.endsWith('/plant.html') || url.pathname.endsWith('/plant.html')) {
        try {
          const html=await response.clone().text();
          if (!html.includes('image-gallery-fix.js')) {
            const injected=html.replace('</body>','<script src="./image-gallery-fix.js" defer></script></body>');
            finalResponse=new Response(injected,{status:response.status,statusText:response.statusText,headers:{'Content-Type':'text/html; charset=UTF-8','Cache-Control':'no-cache'}});
          }
        } catch(e) { console.warn('Plant image fix injection failed',e); }
      }
      const copy=finalResponse.clone(); caches.open(CACHE_NAME).then(cache=>cache.put(request,copy));
      return finalResponse;
    }).catch(()=>caches.match(request).then(cached=>cached||caches.match('./index.html'))));
    return;
  }

  event.respondWith(caches.match(request).then(cached=>cached||fetch(request).then(response=>{
    if(response&&response.status===200&&response.type==='basic'){const copy=response.clone();caches.open(CACHE_NAME).then(cache=>cache.put(request,copy));}
    return response;
  }).catch(()=>caches.match('./index.html'))));
});
