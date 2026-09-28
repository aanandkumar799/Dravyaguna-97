# Image enrichment workflow

The image registry contains 9 required plant-part slots for each of the 97 NCISM plants.

## Safe enrichment process

1. Run `python scripts/build-image-enrichment-queue.py`.
2. Work only from the generated botanical-name + plant-part queries.
3. Prefer Wikimedia Commons and iNaturalist records with documented licensing.
4. Confirm the exact botanical species and the requested plant part from the source itself.
5. Check for duplicates against the existing registry.
6. Download the approved image to the canonical local path:
   `images/plants/<plant_id>/<part>/image.jpg`
7. Update the manifest with source URL, media URL, license, author and verification status.
8. Regenerate `data/image-audit-report.json`.
9. Run:
   - `python scripts/audit-data-quality.py`
   - `python scripts/predeploy-validation.py`

## Important

A missing image stays missing. A remote URL alone is not treated as a local asset, and no placeholder or AI-generated image should be marked as verified. The goal is accurate botanical identification, correct plant-part matching, documented licensing and a reproducible local asset.

The queue is deterministic and can be regenerated whenever the manifest changes.
