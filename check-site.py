#!/usr/bin/env python3
"""
DravyaGuna 97 - Website Doctor
Database and website integrity checker.

This checker enforces the final plant database architecture.
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
errors = []
warnings = []


# ============================================================
# HELPERS
# ============================================================

def add_error(message):
    errors.append(message)


def add_warning(message):
    warnings.append(message)


def is_string(value):
    return isinstance(value, str)


def is_list(value):
    return isinstance(value, list)


def is_dict(value):
    return isinstance(value, dict)


def require_dict(parent, key, path):
    value = parent.get(key)

    if not is_dict(value):
        add_error(f"{path}.{key} must be an object")
        return None

    return value


def require_string(parent, key, path, allow_empty=False):
    value = parent.get(key)

    if not is_string(value):
        add_error(f"{path}.{key} must be a string")
        return None

    if not allow_empty and not value.strip():
        add_error(f"{path}.{key} must not be empty")

    return value


def require_list(parent, key, path):
    value = parent.get(key)

    if not is_list(value):
        add_error(f"{path}.{key} must be an array")
        return None

    return value


def check_string_list(value, path):
    if not is_list(value):
        add_error(f"{path} must be an array")
        return

    for index, item in enumerate(value):
        if not is_string(item):
            add_error(
                f"{path}[{index}] must be a string"
            )


# ============================================================
# REQUIRED FILES
# ============================================================

required_files = [
    "index.html",
    "plant.html",
    "plants.json",
    "script.js",
    "style.css",
]

for filename in required_files:
    if not (ROOT / filename).is_file():
        add_error(f"Missing required file: {filename}")


# ============================================================
# LOAD DATABASE
# ============================================================

plants = []

plants_file = ROOT / "plants.json"

if plants_file.is_file():

    try:
        raw_data = json.loads(
            plants_file.read_text(encoding="utf-8")
        )

    except (OSError, json.JSONDecodeError) as exc:

        add_error(
            f"plants.json could not be parsed: {exc}"
        )
        raw_data = None

    # FINAL ARCHITECTURE:
    # plants.json MUST be an array.
    if raw_data is not None:

        if not isinstance(raw_data, list):

            add_error(
                "plants.json MUST contain an array of plant records. "
                "A single object is not allowed."
            )

        else:
            plants = raw_data

            if not plants:
                add_error(
                    "plants.json contains zero plant records"
                )


# ============================================================
# DUPLICATE ID CHECK
# ============================================================

plant_ids = set()


# ============================================================
# PLANT SCHEMA
# ============================================================

for index, plant in enumerate(plants):

    record_number = index + 1
    path = f"plants.json record {record_number}"

    if not isinstance(plant, dict):

        add_error(
            f"{path} must be an object"
        )
        continue

    # --------------------------------------------------------
    # ID
    # --------------------------------------------------------

    plant_id = require_string(
        plant,
        "id",
        path
    )

    if plant_id:

        if plant_id in plant_ids:
            add_error(
                f"Duplicate plant id: {plant_id}"
            )

        plant_ids.add(plant_id)

    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------

    identity = require_dict(
        plant,
        "identity",
        path
    )

    if identity is not None:

        for field in [
            "name",
            "sanskrit_name",
            "transliteration",
            "botanical_name",
            "family",
            "english_name",
            "hindi_name",
        ]:
            require_string(
                identity,
                field,
                f"{path}.identity"
            )

        for field in [
            "common_names",
            "regional_names",
            "synonyms",
        ]:
            value = identity.get(field)

            if value is not None:
                check_string_list(
                    value,
                    f"{path}.identity.{field}"
                )

    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    classification = require_dict(
        plant,
        "classification",
        path
    )

    if classification is not None:

        for field in [
            "kingdom",
            "habit",
            "habitat",
            "distribution",
        ]:
            require_string(
                classification,
                field,
                f"{path}.classification",
                allow_empty=True
            )

    # --------------------------------------------------------
    # IDENTIFICATION
    # --------------------------------------------------------

    identification = require_dict(
        plant,
        "identification",
        path
    )

    if identification is not None:

        for field in [
            "description",
            "whole_plant",
            "root",
            "stem",
            "leaf",
            "flower",
            "fruit",
            "seed",
            "bark",
        ]:
            require_string(
                identification,
                field,
                f"{path}.identification",
                allow_empty=True
            )

        points = identification.get(
            "identification_points"
        )

        if points is not None:
            check_string_list(
                points,
                f"{path}.identification.identification_points"
            )

    # --------------------------------------------------------
    # IMAGES
    # --------------------------------------------------------

    images = require_dict(
        plant,
        "images",
        path
    )

    if images is not None:

        for field in [
            "whole_plant",
            "habit",
            "root",
            "stem",
            "leaf",
            "flower",
            "fruit",
            "seed",
            "bark",
        ]:

            value = images.get(field)

            if value is None:
                add_error(
                    f"{path}.images.{field} is missing"
                )
                continue

            if not isinstance(value, str):
                add_error(
                    f"{path}.images.{field} must be a string"
                )
                continue

            if value.strip():

                image_path = ROOT / value

                if not image_path.is_file():

                    add_error(
                        f"{plant_id or path} image "
                        f"{field} is missing: {value}"
                    )

    # --------------------------------------------------------
    # DRAVYA GUNA
    # --------------------------------------------------------

    dravya_guna = require_dict(
        plant,
        "dravya_guna",
        path
    )

    if dravya_guna is not None:

        for field in [
            "rasa",
            "guna",
            "karma",
        ]:

            value = dravya_guna.get(field)

            if value is None:
                add_error(
                    f"{path}.dravya_guna.{field} is missing"
                )
            else:
                check_string_list(
                    value,
                    f"{path}.dravya_guna.{field}"
                )

        for field in [
            "virya",
            "vipaka",
            "prabhava",
        ]:

            require_string(
                dravya_guna,
                field,
                f"{path}.dravya_guna",
                allow_empty=True
            )

    # --------------------------------------------------------
    # DOSHA
    # --------------------------------------------------------

    dosha = require_dict(
        plant,
        "dosha",
        path
    )

    if dosha is not None:

        for field in [
            "vata",
            "pitta",
            "kapha",
        ]:

            require_string(
                dosha,
                field,
                f"{path}.dosha",
                allow_empty=True
            )

    # --------------------------------------------------------
    # THERAPEUTICS
    # --------------------------------------------------------

    therapeutics = require_dict(
        plant,
        "therapeutics",
        path
    )

    if therapeutics is not None:

        for field in [
            "useful_part",
            "indications",
            "therapeutic_actions",
        ]:

            value = therapeutics.get(field)

            if value is None:
                add_error(
                    f"{path}.therapeutics.{field} is missing"
                )
            else:
                check_string_list(
                    value,
                    f"{path}.therapeutics.{field}"
                )

        for field in [
            "dose",
            "anupana",
            "duration",
            "precautions",
            "contraindications",
        ]:

            value = therapeutics.get(field)

            if value is None:
                add_error(
                    f"{path}.therapeutics.{field} is missing"
                )
            elif not isinstance(value, (str, list)):
                add_error(
                    f"{path}.therapeutics.{field} "
                    "must be a string or array"
                )

    # --------------------------------------------------------
    # FORMULATIONS
    # --------------------------------------------------------

    formulations = require_list(
        plant,
        "formulations",
        path
    )

    if formulations is not None:

        for formulation_index, formulation in enumerate(
            formulations
        ):

            formulation_path = (
                f"{path}.formulations[{formulation_index}]"
            )

            if not isinstance(formulation, dict):

                add_error(
                    f"{formulation_path} must be an object"
                )
                continue

            for field in [
                "name",
                "dosage_form",
                "indication",
                "reference",
            ]:

                require_string(
                    formulation,
                    field,
                    formulation_path,
                    allow_empty=True
                )

    # --------------------------------------------------------
    # CLASSICAL REFERENCES
    # --------------------------------------------------------

    classical_reference = require_dict(
        plant,
        "classical_reference",
        path
    )

    if classical_reference is not None:

        shlokas = classical_reference.get(
            "shlokas"
        )

        if shlokas is None:
            add_error(
                f"{path}.classical_reference.shlokas is missing"
            )

        elif not isinstance(shlokas, list):

            add_error(
                f"{path}.classical_reference.shlokas "
                "must be an array"
            )

        else:

            for shloka_index, shloka in enumerate(
                shlokas
            ):

                shloka_path = (
                    f"{path}.classical_reference."
                    f"shlokas[{shloka_index}]"
                )

                if not isinstance(shloka, dict):

                    add_error(
                        f"{shloka_path} must be an object"
                    )
                    continue

                for field in [
                    "text",
                    "transliteration",
                    "meaning",
                    "source",
                    "chapter",
                    "reference",
                ]:

                    require_string(
                        shloka,
                        field,
                        shloka_path,
                        allow_empty=True
                    )

                verified = shloka.get("verified")

                if verified is not None and not isinstance(
                    verified,
                    bool
                ):

                    add_error(
                        f"{shloka_path}.verified "
                        "must be true or false"
                    )

        for field in [
            "nighantu_references",
            "samhita_references",
        ]:

            value = classical_reference.get(field)

            if value is not None and not isinstance(
                value,
                list
            ):

                add_error(
                    f"{path}.classical_reference."
                    f"{field} must be an array"
                )

    # --------------------------------------------------------
    # PHYTOCHEMISTRY
    # --------------------------------------------------------

    phytochemistry = require_dict(
        plant,
        "phytochemistry",
        path
    )

    if phytochemistry is not None:

        constituents = phytochemistry.get(
            "major_constituents"
        )

        if constituents is not None:

            check_string_list(
                constituents,
                f"{path}.phytochemistry.major_constituents"
            )

        require_string(
            phytochemistry,
            "chemical_notes",
            f"{path}.phytochemistry",
            allow_empty=True
        )

    # --------------------------------------------------------
    # MODERN INFORMATION
    # --------------------------------------------------------

    modern_information = require_dict(
        plant,
        "modern_information",
        path
    )

    if modern_information is not None:

        for field in [
            "evidence_summary",
            "safety_notes",
        ]:

            require_string(
                modern_information,
                field,
                f"{path}.modern_information",
                allow_empty=True
            )

        for field in [
            "recognized_uses",
            "sources",
        ]:

            value = modern_information.get(field)

            if value is not None:

                check_string_list(
                    value,
                    f"{path}.modern_information.{field}"
                )

    # --------------------------------------------------------
    # STUDENT
    # --------------------------------------------------------

    student = require_dict(
        plant,
        "student",
        path
    )

    if student is not None:

        for field in [
            "exam_points",
            "viva_questions",
            "identification_points",
            "mnemonics",
        ]:

            value = student.get(field)

            if value is None:
                add_error(
                    f"{path}.student.{field} is missing"
                )
            else:
                check_string_list(
                    value,
                    f"{path}.student.{field}"
                )

        require_string(
            student,
            "quick_revision",
            f"{path}.student",
            allow_empty=True
        )

    # --------------------------------------------------------
    # TEACHER
    # --------------------------------------------------------

    teacher = require_dict(
        plant,
        "teacher",
        path
    )

    if teacher is not None:

        for field in [
            "teaching_points",
            "discussion_points",
            "practical_points",
        ]:

            value = teacher.get(field)

            if value is None:
                add_error(
                    f"{path}.teacher.{field} is missing"
                )
            else:
                check_string_list(
                    value,
                    f"{path}.teacher.{field}"
                )

    # --------------------------------------------------------
    # DOCTOR
    # --------------------------------------------------------

    doctor = require_dict(
        plant,
        "doctor",
        path
    )

    if doctor is not None:

        for field in [
            "quick_reference",
            "useful_part",
            "dose",
            "anupana",
            "key_precautions",
        ]:

            value = doctor.get(field)

            if value is None:
                add_error(
                    f"{path}.doctor.{field} is missing"
                )

            elif field == "key_precautions":

                check_string_list(
                    value,
                    f"{path}.doctor.{field}"
                )

            else:

                require_string(
                    doctor,
                    field,
                    f"{path}.doctor",
                    allow_empty=True
                )

        important_indications = doctor.get(
            "important_indications"
        )

        if important_indications is None:

            add_error(
                f"{path}.doctor.important_indications "
                "is missing"
            )

        else:

            check_string_list(
                important_indications,
                f"{path}.doctor.important_indications"
            )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    sources = require_list(
        plant,
        "sources",
        path
    )

    if sources is not None:

        for source_index, source in enumerate(
            sources
        ):

            source_path = (
                f"{path}.sources[{source_index}]"
            )

            if not isinstance(source, dict):

                add_error(
                    f"{source_path} must be an object"
                )
                continue

            for field in [
                "type",
                "title",
                "author",
                "edition",
                "year",
                "page",
                "url",
            ]:

                require_string(
                    source,
                    field,
                    source_path,
                    allow_empty=True
                )

            verified = source.get("verified")

            if verified is not None and not isinstance(
                verified,
                bool
            ):

                add_error(
                    f"{source_path}.verified "
                    "must be true or false"
                )

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    metadata = require_dict(
        plant,
        "metadata",
        path
    )

    if metadata is not None:

        for field in [
            "status",
            "last_verified",
            "verified_by",
            "version",
        ]:

            require_string(
                metadata,
                field,
                f"{path}.metadata",
                allow_empty=True
            )


# ================================================
