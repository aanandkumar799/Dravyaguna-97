(() => {
  'use strict';

  const DATA_URL = 'data/identification-gallery.json?v=1';
  const normalize = value => String(value || '').trim().toLowerCase().replace(/\s+/g, ' ');
  const esc = value => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;').replace(/'/g, '&#039;');

  async function loadGallery() {
    const response = await fetch(DATA_URL, { cache: 'no-store', headers: { Accept: 'application/json' } });
    if (!response.ok) return null;
    return response.json();
  }

  function render(record) {
    if (!record || document.getElementById('supplemental-identification-gallery')) return;
    const images = Array.isArray(record.gallery_images) ? record.gallery_images : [];
    if (!images.length) return;

    const section = document.createElement('section');
    section.className = 'plant-section supplemental-identification-section';
    section.id = 'supplemental-identification-gallery';
    section.innerHTML = `
      <h2>Identification Gallery — Drug ${esc(record.id)}</h2>
      <p class="gallery-disclaimer">Supplemental visual references supplied for identification practice. These external images are not treated as internally verified clinical or taxonomic evidence.</p>
      <div class="image-gallery identification-gallery">
        ${images.map(image => `
          <figure class="gallery-item supplemental-gallery-item">
            <img src="${esc(image.url)}" alt="${esc(record.sanskrit_name)} — ${esc(image.image_type)}" loading="lazy" data-full="${esc(image.url)}">
            <figcaption>${esc(image.image_type)}<small>${esc(image.caption)}</small></figcaption>
            <div class="identification-features"><strong>Identification features:</strong> ${esc((image.verified_features || []).join(' • '))}</div>
            <a class="gallery-source" href="${esc(image.url)}" target="_blank" rel="noopener noreferrer">External image source</a>
          </figure>
        `).join('')}
      </div>`;

    const sections = [...document.querySelectorAll('.plant-section')];
    const target = sections.find(sectionEl => normalize(sectionEl.querySelector('h2')?.textContent) === 'verified image registry');
    if (target) target.insertAdjacentElement('afterend', section);
    else document.getElementById('plant-content')?.appendChild(section);

    section.querySelectorAll('img').forEach(img => {
      img.addEventListener('error', () => {
        img.replaceWith(Object.assign(document.createElement('div'), {
          className: 'image-missing',
          textContent: 'Image could not be loaded'
        }));
      }, { once: true });
    });
  }

  async function findAndRender() {
    const title = document.querySelector('.plant-hero h1')?.textContent;
    const botanical = document.querySelector('.plant-hero .botanical')?.textContent;
    if (!title && !botanical) return;
    const data = await loadGallery().catch(() => null);
    const records = Array.isArray(data?.records) ? data.records : [];
    const match = records.find(record => normalize(record.sanskrit_name) === normalize(title) || normalize(record.botanical_name) === normalize(botanical));
    render(match);
  }

  const observer = new MutationObserver(() => {
    if (document.querySelector('.plant-hero h1')) {
      observer.disconnect();
      findAndRender();
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
  if (document.querySelector('.plant-hero h1')) findAndRender();
})();
