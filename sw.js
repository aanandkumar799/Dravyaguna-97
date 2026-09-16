const CACHE_NAME = 'dravya-guna-97-v4';
const APP_SHELL = ['./','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html','./style.css','./responsive-fix.css','./plant-dossier-layout.css','./academic-enhancements.css','./academic-enhancements.js','./manifest.json','./404.html','./robots.txt','./sitemap.xml','./favicon.svg','./images/favicon.png'];

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

  // Always prefer fresh JSON so database corrections are visible immediately.
  if (url.pathname.endsWith('.json')) {
    event.respondWith(fetch(request, {cache:'no-store'}).then(response => {
      if (response && response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
      }
      return response;
    }).catch(() => caches.match(request)));
    return;
  }

  // Network-first for HTML prevents stale GitHub Pages documents after deployment.
  if (request.mode === 'navigate' || url.pathname.endsWith('.html')) {
    event.respondWith(fetch(request).then(response => {
      if (response && response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
      }
      return response;
    }).catch(() => caches.match(request).then(cached => cached || caches.match('./index.html'))));
    return;
  }

  event.respondWith(caches.match(request).then(cached => cached || fetch(request).then(response => {
    if (response && response.status === 200 && response.type === 'basic') {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
    }
    return response;
  }).catch(() => caches.match('./index.html'))));
});
