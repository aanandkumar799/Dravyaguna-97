const CACHE_NAME = 'dravya-guna-97-v54-app-icon';
const APP_SHELL = [
  './','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html','./viva.html','./progress.html','./rasa.html','./reference-library.html','./data-quality.html','./sources-review.html',
  './practical-lab.html','./references.html','./formulations.html','./404.html','./style.css','./site-theme.css','./plant-dossier-layout.css',
  './academic-verification.js','./public-seo.js','./flashcard-entry.js','./classical-references-enhanced.js','./practical-lab-enhanced.js','./script.js',
  './data/curated-image-manifest.json','./plant-index.json','./manifest.json','./robots.txt','./sitemap.xml',
  './feedback-config.js','./feedback.js','./feedback.css','./feedback.html','./site-theme.js','./supplementary.html','./supplementary-plant.html',
  './data/supplementary-index.json','./images/favicon.png','./images/icon-192.png','./images/icon-512.png','./images/icon-maskable-512.png','./apple-touch-icon.png','./favicon.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.all(APP_SHELL.map(url => cache.add(url).catch(() => undefined))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.endsWith('.json')) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request, { cache: 'no-store' });
        if (response.ok) {
          const cache = await caches.open(CACHE_NAME);
          await cache.put(request, response.clone()).catch(() => {});
          return response;
        }
        // A cached last-known-good JSON response is preferable to a transient
        // server error for offline study, but preserve the server response if
        // no cached copy exists.
        return (await caches.match(request)) || response;
      } catch (error) {
        const cached = await caches.match(request);
        if (cached) return cached;
        throw error;
      }
    })());
    return;
  }

  if (request.mode === 'navigate' || url.pathname.endsWith('.html')) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok) {
          const cache = await caches.open(CACHE_NAME);
          await cache.put(request, response.clone()).catch(() => {});
        }
        return response;
      } catch (error) {
        const cached = await caches.match(request);
        if (cached) return cached;
        const shell = await caches.match('./index.html');
        if (shell) return shell;
        throw error;
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cached = await caches.match(request);
    if (cached) return cached;
    const response = await fetch(request);
    if (response.ok && response.type === 'basic') {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, response.clone()).catch(() => {});
    }
    return response;
  })());
});
