# DravyaGuna 97 — Modular Plant Database

This folder is the **canonical editable database**.

## Rule
- **One plant = one JSON file**: `data/plants/<plant-id>.json`
- Do not create a second aggregate database.
- `plants.json` is no longer a source file. The build pipeline may assemble it temporarily for legacy enrichment/validation scripts and deletes it before committing.
- `plant-index.json` remains the lightweight navigation/search index.

## Editing a plant
Each JSON record should keep the same top-level structure so the website can render every section consistently:

`identity` · `classification` · `identification` · `images` · `dravya_guna` · `dosha` · `therapeutics` · `formulations` · `classical_reference` · `phytochemistry` · `modern_information` · `student` · `teacher` · `doctor` · `sources` · `metadata`

## Verification policy
Use explicit status rather than filling gaps with guesses:

- `verified_classical` — checked against the named classical source/edition.
- `needs_text_verification` — information is present but the exact text/page/verse still needs checking.
- `working_draft` — structural or provisional content only.
- `modern_reference` — modern evidence/source, kept separate from classical authority.

Blank fields are preferable to invented facts. For classical quotations, retain the source, edition/recension when known, chapter/section, verse/page when verified, and a verification flag.

## Practical identification
Where available, keep separate identification notes for whole plant, root, stem, leaf, flower, fruit, seed and bark. Images must be species-specific and source/attribution information should be retained.

## Safe update workflow
1. Edit only the relevant plant JSON file.
2. Cross-check Sanskrit, botanical identity, rasa-panchaka, classical quotations and formulation references against authoritative texts.
3. Update `metadata.status`, `last_verified`, and source details.
4. Run the database validation pipeline before publication.

## Migration status
The legacy aggregate database has been migrated into individual plant JSON records. The aggregate `plants.json` file is intentionally absent from the repository.
