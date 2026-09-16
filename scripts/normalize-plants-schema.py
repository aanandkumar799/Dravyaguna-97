#!/usr/bin/env python3
"""Normalize legacy plant records into the Website Doctor schema.

This changes data shape only; it does not invent Ayurvedic content.
Unknown/non-string scalar metadata is converted to safe strings, legacy
string shlokas become structured shloka objects, and formulation fields are
normalized to strings.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "plants.json"

STRING_FIELDS = ("author", "edition", "year", "page")
FORMULATION_FIELDS = ("name", "dosage_form", "indication", "reference")
SHLOKA_FIELDS = ("text", "transliteration", "meaning", "source", "chapter", "reference")


def to_string(value):
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        # Empty/legacy list values represent an unfilled text field.
        if not value:
            return ""
        return "; ".join(to_string(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def normalize(data):
    changed = False
    for plant in data:
        if not isinstance(plant, dict):
            continue

        guna = plant.get("dravya_guna")
        if isinstance(guna, dict):
            value = guna.get("prabhava")
            normalized = to_string(value)
            if value != normalized:
                guna["prabhava"] = normalized
                changed = True

        formulations = plant.get("formulations")
        if isinstance(formulations, list):
            for formulation in formulations:
                if not isinstance(formulation, dict):
                    continue
                for field in FORMULATION_FIELDS:
                    value = formulation.get(field, "")
                    normalized = to_string(value)
                    if field not in formulation or value != normalized:
                        formulation[field] = normalized
                        changed = True

        classical = plant.get("classical_reference")
        if isinstance(classical, dict):
            shlokas = classical.get("shlokas")
            if isinstance(shlokas, list):
                normalized_shlokas = []
                for shloka in shlokas:
                    if isinstance(shloka, dict):
                        item = dict(shloka)
                        for field in SHLOKA_FIELDS:
                            value = item.get(field, "")
                            normalized = to_string(value)
                            if field not in item or value != normalized:
                                changed = True
                            item[field] = normalized
                        if "verified" in item and not isinstance(item["verified"], bool):
                            item["verified"] = bool(item["verified"])
                            changed = True
                        normalized_shlokas.append(item)
                    elif isinstance(shloka, str):
                        normalized_shlokas.append({
                            "text": shloka,
                            "transliteration": "",
                            "meaning": "",
                            "source": "",
                            "chapter": "",
                            "reference": "",
                            "verified": False,
                        })
                        changed = True
                    else:
                        normalized_shlokas.append({
                            "text": to_string(shloka),
                            "transliteration": "",
                            "meaning": "",
                            "source": "",
                            "chapter": "",
                            "reference": "",
                            "verified": False,
                        })
                        changed = True
                if shlokas != normalized_shlokas:
                    classical["shlokas"] = normalized_shlokas
                    changed = True

        sources = plant.get("sources")
        if isinstance(sources, list):
            for source in sources:
                if not isinstance(source, dict):
                    continue
                for field in STRING_FIELDS:
                    value = source.get(field, "")
                    normalized = to_string(value)
                    if field not in source or value != normalized:
                        source[field] = normalized
                        changed = True
                if "verified" in source and not isinstance(source["verified"], bool):
                    source["verified"] = bool(source["verified"])
                    changed = True

    return changed


data = json.loads(PATH.read_text(encoding="utf-8"))
if not isinstance(data, list):
    raise SystemExit("plants.json must contain an array")

if normalize(data):
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Normalized plants.json schema fields")
else:
    print("plants.json already normalized")
