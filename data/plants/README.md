# DravyaGuna 97 — Canonical Plant Database

This folder is the **single authoritative editable database** for the NCISM 97 syllabus.

## Permanent rule
- **One plant = one JSON file:** `data/plants/<plant-id>.json`
- Each NCISM record is identified by its `id` and `order` (1–97).
- Do **not** create batch files, correction files, aggregate databases, or duplicate plant records.
- `plant-index.json` is only a lightweight navigation/search index; the detailed JSON files are the source of truth.
- `plants.json` is intentionally absent and must not be recreated.

## Editing a plant
Edit only the relevant plant JSON file. Keep the common top-level structure:

`identity` · `classification` · `identification` · `images` · `dravya_guna` · `dosha` · `therapeutics` · `formulations` · `classical_reference` · `phytochemistry` · `modern_information` · `student` · `teacher` · `doctor` · `sources` · `metadata`

This makes missing fields easy to find, correct, review and independently verify without touching unrelated plants.

## Verification policy
Use explicit status rather than filling gaps with guesses:

- `verified_classical` — checked against the named classical source/edition.
- `needs_text_verification` — information is present but exact text/page/verse still needs checking.
- `working_draft` — structural or provisional content only.
- `modern_reference` — modern evidence/source kept separate from classical authority.

Blank fields are preferable to invented facts. For classical quotations, retain the source, edition/recension when known, chapter/section, verse/page when verified, and a verification flag.

## Practical identification
Keep separate identification notes where available for whole plant, root, stem, leaf, flower, fruit, seed and bark. Images must be species-specific and source/attribution information should be retained.

## Safe update workflow
1. Edit only the relevant plant JSON file.
2. Cross-check Sanskrit, botanical identity, rasa-panchaka, classical quotations and formulation references against authoritative texts.
3. Update `metadata.status`, `last_verified`, and source details.
4. Run the repository validation workflow before publication.

The deployment pipeline reads the modular files directly and validates that the canonical NCISM sequence contains exactly 97 records.
