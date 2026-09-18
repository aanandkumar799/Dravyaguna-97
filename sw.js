const CACHE_NAME = 'dravya-guna-97-v30-supplementary-loader';
const APP_SHELL = [
  './','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html','./viva.html','./progress.html','./rasa.html','./reference-library.html','./data-quality.html',
  './practical-lab.html','./references.html','./404.html','./style.css','./responsive-fix.css','./site-theme.css','./plant-dossier-layout.css','./cover-image-fix.js','./dossier-fallback.js','./image-gallery-delay.js',
  './image-gallery-fix.js','./academic-verification.js','./public-seo.js','./flashcard-entry.js','./classical-references-enhanced.js','./practical-lab-enhanced.js','./script.js',
  './data/curated-image-manifest.json','./plant-index.json','./plants.json','./manifest.json','./robots.txt','./sitemap.xml','./manifest.json','./feedback-config.js','./feedback.js','./feedback.css','./site-theme.js','./supplementary.html','./supplementary-plant.html','./data/supplementary-index.json','./favicon-exact.jpg'
];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL).catch(()=>Promise.all(APP_SHELL.map(url=>cache.add(url).catch(()=>{}))))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{
  const request=event.request;if(request.method!=='GET')return;
  const url=new URL(request.url);if(url.origin!==self.location.origin)return;
  if(url.pathname.endsWith('.json')){event.respondWith(fetch(request,{cache:'no-store'}).then(response=>{if(response.ok)caches.open(CACHE_NAME).then(c=>c.put(request,response.clone())).catch(()=>{});return response}).catch(()=>caches.match(request)));return}
  if(request.mode==='navigate'||url.pathname.endsWith('.html')){event.respondWith(fetch(request).then(response=>{if(response.ok)caches.open(CACHE_NAME).then(c=>c.put(request,response.clone())).catch(()=>{});return response}).catch(()=>caches.match(request).then(c=>c||caches.match('./index.html'))));return}
  event.respondWith(caches.match(request).then(cached=>cached||fetch(request).then(response=>{if(response.ok&&response.type==='basic')caches.open(CACHE_NAME).then(c=>c.put(request,response.clone())).catch(()=>{});return response})));
});
