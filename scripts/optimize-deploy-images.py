#!/usr/bin/env python3
"""Create lightweight WebP plant images in a prepared deployment directory.

Original repository assets remain untouched. This script is run after the site
has been copied to _site, so only the deployed artifact is rewritten.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

MAX_WIDTH = 1200
QUALITY = 78
LOCAL_ROOT = "images/plants/"
TEXT_EXTENSIONS = {".html", ".js", ".css", ".json", ".xml", ".txt", ".webmanifest"}
LOCAL_REF_RE = re.compile(r"images/plants/[^\"'<>\s)]+?\.(?:jpe?g|png)", re.IGNORECASE)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    image_root = root / LOCAL_ROOT
    if not image_root.is_dir():
        raise SystemExit(f"Plant image directory not found: {image_root}")

    replacements: dict[str, str] = {}
    converted = 0
    original_bytes = 0
    optimized_bytes = 0

    for source in sorted(image_root.rglob("*")):
        if not source.is_file() or source.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        rel = source.relative_to(root).as_posix()
        target = source.with_suffix(".webp")
        with Image.open(source) as image:
            image = image.convert("RGB")
            if image.width > MAX_WIDTH:
                height = round(image.height * MAX_WIDTH / image.width)
                image.thumbnail((MAX_WIDTH, height), Image.Resampling.LANCZOS)
            target.parent.mkdir(parents=True, exist_ok=True)
            image.save(target, "WEBP", quality=QUALITY, method=6)
        original_bytes += source.stat().st_size
        optimized_bytes += target.stat().st_size
        replacements[rel] = target.relative_to(root).as_posix()
        source.unlink()
        converted += 1

    if not replacements:
        print("No JPEG/PNG plant images found to optimize.")
        return 0

    # Update generated HTML, JSON, JS, CSS, XML and manifest references.
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        # Also cover dynamic fallback strings such as image.jpg in script.js.
        updated = LOCAL_REF_RE.sub(
            lambda match: str(Path(match.group(0)).with_suffix(".webp")).replace("\\", "/"),
            updated,
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8")

    print(
        f"Optimized {converted} plant images: "
        f"{original_bytes / 1024 / 1024:.1f} MiB -> "
        f"{optimized_bytes / 1024 / 1024:.1f} MiB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
