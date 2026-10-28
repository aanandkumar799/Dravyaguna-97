#!/usr/bin/env python3
"""Validate inline JavaScript blocks embedded in HTML files."""

from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP_TYPES = {"application/ld+json", "application/json", "text/template", "text/html"}


class ScriptCollector(HTMLParser):
    """Collect inline <script> bodies using the standard HTML tokenizer."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.scripts = []  # (type, has_src, body)
        self._current = None

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            values = dict(attrs)
            self._current = [(values.get("type") or "").strip().lower(), "src" in values, []]

    def handle_endtag(self, tag):
        if tag == "script" and self._current is not None:
            kind, has_src, parts = self._current
            self.scripts.append((kind, has_src, "".join(parts)))
            self._current = None

    def handle_data(self, data):
        if self._current is not None:
            self._current[2].append(data)


failed = False
for page in sorted(ROOT.rglob("*.html")):
    if ".git" in page.parts or "node_modules" in page.parts:
        continue
    collector = ScriptCollector()
    collector.feed(page.read_text(encoding="utf-8", errors="replace"))
    collector.close()
    for index, (kind, has_src, script) in enumerate(collector.scripts, start=1):
        if has_src or not script.strip():
            continue
        if kind in SKIP_TYPES:
            print(f"⏭️ {page} script {index}: {kind} (not executable JavaScript)")
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

sys.exit(1 if failed else 0)
