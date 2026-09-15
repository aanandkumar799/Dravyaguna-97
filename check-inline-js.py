#!/usr/bin/env python3
"""Validate inline JavaScript blocks embedded in HTML files."""

from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parent
failed = False

for page in sorted(ROOT.rglob("*.html")):
    source = page.read_text(encoding="utf-8", errors="replace")
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", source, flags=re.IGNORECASE | re.DOTALL)

    for index, script in enumerate(scripts, start=1):
        if not script.strip():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(script)
            temporary_path = handle.name
        result = subprocess.run(["node", "--check", temporary_path], capture_output=True, text=True)
        if result.returncode:
            failed = True
            print(f"❌ {page} inline script {index}")
            print(result.stderr.strip())
        else:
            print(f"✅ {page} inline script {index}")

if failed:
    sys.exit(1)
