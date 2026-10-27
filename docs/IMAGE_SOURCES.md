# DravyaGuna-97 — Botanical Image Sources

The website now uses a reliability-first image-source hierarchy for plant cover images:

1. **Wikimedia Commons** — preferred when an exact botanical-name match is available. Part-specific searches are used for leaf, flower, fruit, seed, root, stem and bark images. The site links back to the Commons file page.
2. **iNaturalist** — fallback for exact scientific-name observations. The resolver accepts only photographs explicitly marked CC0, CC BY or CC BY-SA and links to the observation for attribution.
3. **GBIF** — fallback for occurrence records with still images. Media licensing is checked before use and the image links back to the GBIF occurrence record.
4. **Kew Plants of the World Online (POWO)** — authoritative taxonomic/image reference for identity checking. Individual image rights are respected; POWO is primarily used as a verification/reference source rather than blindly hotlinking every image.
5. **eFlora of India** — important Indian-flora photographic reference for species and identification checking. Image rights/attribution are respected on a per-image basis.
6. **India Biodiversity Portal** — Indian biodiversity reference and image/observation source. Reusable content is attributed according to the applicable Creative Commons terms.

## Selection rules

- Exact botanical identity is preferred over common-name matching.
- Obvious leaf/flower/fruit/root/bark/stem/diagram/illustration results are excluded from the homepage cover-image search.
- A missing image is never filled with an unrelated species merely to make the card look complete.
- Plant-part galleries should prefer an image of the requested part; otherwise the UI should show that a verified image is unavailable.
- Whole-plant and habit/growth-form images should not reuse the same URL.
- Image attribution/source links should remain available wherever an external image is used.
- For iNaturalist, the website only accepts CC0, CC BY and CC BY-SA photographs in the automatic fallback because the project should remain reusable beyond a strictly non-commercial context.
- GBIF media may carry terms that are more restrictive than the occurrence dataset, so the individual media license must be respected.

## Why these sources?

Kew POWO provides authoritative plant names, taxonomy and images; Wikimedia Commons provides a large species- and plant-part-oriented media collection; eFlora of India and India Biodiversity Portal are particularly useful for Indian medicinal plants; iNaturalist and GBIF provide additional biodiversity observations and media with machine-readable licensing metadata.
