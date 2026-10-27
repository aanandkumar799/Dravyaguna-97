# Dravyaguna 97

BAMS Dravyaguna reference portal for the 97 NCISM plants, with searchable plant records, practical identification tools, classical references, quizzes, and a verified image registry.

## Repository layout

- **Public site files at the root** — HTML, CSS, JavaScript, `plant-index.json`, `manifest.json`, `sw.js`, `robots.txt`, and `sitemap.xml`. These remain at the root because GitHub Pages and Firebase Hosting serve them at their public URLs.
- **`plants/`** — crawlable static pages for each NCISM plant, generated from the modular records.
- **`data/plants/`** — canonical modular plant records and data documentation.
- **`data/curated-image-manifest.json`** — image registry with verification status and source metadata.
- **`images/`** — repository image assets and image documentation.
- **`scripts/`** — generators, validators, audits, deployment preparation, and maintenance utilities.
- **`docs/`** — security, Firebase, image-enrichment, and source documentation.
- **`.github/workflows/`** — GitHub Pages, Firebase Hosting, Website Doctor, CodeQL, and image-audit workflows.

## Local validation

From the repository root:

```bash
python3 scripts/generate-site-artifacts.py
python3 scripts/audit-data-quality.py
python3 scripts/predeploy-validation.py
python3 scripts/check-site.py
python3 scripts/check-inline-js.py
python3 scripts/validate-curated-images.py
```

The deploy workflows also optimize plant photos into resized WebP files in the deployment artifact; the original source assets remain available in Git for traceability.

## Deployments

GitHub Pages is the primary public deployment. Firebase Hosting is used for the Firebase-backed copy and authenticated feedback integration. Firebase CI requires the environment secret `FIREBASE_SERVICE_ACCOUNT_DRAVYA_GUNA_97` and the service account roles documented in [`docs/FIREBASE_SETUP.md`](docs/FIREBASE_SETUP.md).
