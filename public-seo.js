(() => {
  const base = new URL('https://aanandkumar799.github.io/Dravyaguna-97/');
  const setMeta = (name, content, attr = 'name') => {
    if (!content) return;
    let el = document.head.querySelector(`meta[${attr}="${CSS.escape(name)}"]`);
    if (!el) { el = document.createElement('meta'); el.setAttribute(attr, name); document.head.appendChild(el); }
    el.setAttribute('content', content);
  };
  const setCanonical = url => {
    let el = document.head.querySelector('link[rel="canonical"]');
    if (!el) { el = document.createElement('link'); el.rel = 'canonical'; document.head.appendChild(el); }
    el.href = url;
  };
  const addJsonLd = data => {
    const old = document.getElementById('dg-seo-jsonld');
    if (old) old.remove();
    const s = document.createElement('script'); s.type = 'application/ld+json'; s.id = 'dg-seo-jsonld'; s.textContent = JSON.stringify(data); document.head.appendChild(s);
  };
  const page = location.pathname.split('/').pop() || 'index.html';
  if (page !== 'plant.html') {
    const titles = { 'index.html':'DravyaGuna 97 | BAMS Dravyaguna Learning Portal', 'plants.html':'NCISM 97 Plant Library | DravyaGuna 97', 'compare.html':'Compare Ayurvedic Dravyas | DravyaGuna 97', 'quiz.html':'BAMS Dravyaguna Practice Quiz | DravyaGuna 97' };
    if (titles[page]) document.title = titles[page];
    setCanonical(new URL(page === 'index.html' ? '' : page, base).href);
    addJsonLd({ '@context':'https://schema.org', '@type':'WebSite', name:'DravyaGuna 97', url:base.href, description:'BAMS Dravyaguna learning and reference portal for medicinal plants, practical identification, revision, comparison and quizzes.' });
    return;
  }
  const id = new URLSearchParams(location.search).get('id');
  if (!id) return;
  fetch(new URL('data/plants/' + encodeURIComponent(id) + '.json', location.href), {cache:'force-cache'})
    .then(r => r.ok ? r.json() : Promise.reject(new Error('not found')))
    .then(p => {
      const i = p.identity || {}, m = p.metadata || {};
      const name = i.name || p.name || id, botanical = i.botanical_name || '', family = i.family || '';
      const description = `BAMS Dravyaguna reference for ${name}${botanical ? ` (${botanical})` : ''}. Includes identity, practical identification, Rasa Panchaka, classical references, formulations, student revision and safety notes.`;
      document.title = `${name} | DravyaGuna 97`;
      setMeta('description', description);
      setMeta('og:title', `${name} | DravyaGuna 97`, 'property');
      setMeta('og:description', description, 'property');
      setMeta('og:type', 'article', 'property');
      setMeta('og:image', new URL('images/icon-512.png', base).href, 'property');
      setMeta('twitter:card', 'summary_large_image');
      setMeta('twitter:image', new URL('images/icon-512.png', base).href);
      setCanonical(new URL(`plants/${encodeURIComponent(id)}/`, base).href);
      addJsonLd({ '@context':'https://schema.org', '@type':'Article', headline:`${name} | DravyaGuna 97`, description, url:new URL(`plants/${encodeURIComponent(id)}/`, base).href, isPartOf:{'@type':'WebSite',name:'DravyaGuna 97',url:base.href}, about:{'@type':'Thing',name, ...(botanical ? {alternateName:botanical}:{})}, ...(family ? {keywords:[family,'Dravyaguna','BAMS','Ayurveda']} : {}), educationalUse:['study','revision','practical identification'], citation:m.sources || p.sources || [] });
    }).catch(() => {});
})();
