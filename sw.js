const CACHE_NAME = 'dravya-guna-97-v14';
const APP_SHELL = [
  './','./index.html','./plants.html','./plant.html','./compare.html','./quiz.html',
  './practical-lab.html','./references.html','./404.html','./style.css','./responsive-fix.css',
  './plant-dossier-layout.css','./cover-image-fix.js','./dossier-fallback.js','./image-gallery-delay.js',
  './image-gallery-fix.js','./academic-verification.js','./public-seo.js','./flashcard-entry.js',
  './classical-references-enhanced.js','./practical-lab-enhanced.js','./script.js',
  './data/curated-image-manifest.json','./plant-index.json','./manifest.json','./robots.txt','./sitemap.xml','./favicon.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function plantPageResponse(request, response) {
  if (!response?.ok) return response;
  try {
    const html = await response.text();
    if (!/<script[^>]+src=["'](?:\.\/)?image-gallery-fix\.js/i.test(html)) {
      const injected = html.replace(/<\/head>/i, '<script src="./image-gallery-fix.js" defer></script></head>');
      return new Response(injected, {status: response.status, statusText: response.statusText, headers: response.headers});
    }
  } catch (_) {}
  return response;
}

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.endsWith('.json')) {
    event.respondWith(
      fetch(request, {cache:'no-store'})
        .then(response => {
          if (response?.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, copy)).catch(() => {});
          }
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  if (request.mode === 'navigate' || url.pathname.endsWith('.html')) {
    event.respondWith(
      fetch(request)
        .then(async response => {
          const finalResponse = url.pathname.endsWith('/plant.html') || url.pathname.endsWith('/plant')
            ? await plantPageResponse(request, response)
            : response;
          if (finalResponse?.ok) {
            const copy = finalResponse.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, copy)).catch(() => {});
          }
          return finalResponse;
        })
        .catch(() => caches.match(request).then(cached => cached || caches.match('./index.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then(cached => cached || fetch(request).then(response => {
      if (response?.ok && response.type === 'basic') {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, copy)).catch(() => {});
      }
      return response;
    }))
  );
});
