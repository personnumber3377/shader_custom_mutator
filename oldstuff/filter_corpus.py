#!/usr/bin/env python3
import re
from pathlib import Path

SVG_DIR = Path("svg")
OUTPUT_FILE = Path("output.txt")

# Extract allowed filenames
allowed = set()
pattern = re.compile(r"Running on\s+svg/([^\s]+)")

for line in OUTPUT_FILE.read_text().splitlines():
    m = pattern.search(line)
    if m:
        allowed.add(m.group(1))

print(f"[+] Keeping {len(allowed)} SVG files")

# Delete everything else
for svg in SVG_DIR.glob("*.svg"):
    if svg.name not in allowed:
        print(f"[-] Deleting {svg}")
        svg.unlink()