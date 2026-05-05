#!/usr/bin/env python3
"""Update the SURPRISE_IMAGES list in index.html from the surprise/ folder."""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SURPRISE_DIR = os.path.join(ROOT, "surprise")
INDEX_HTML = os.path.join(ROOT, "index.html")

images = sorted(
    f for f in os.listdir(SURPRISE_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
)

if not images:
    raise SystemExit("No images found in surprise/")

entries = ",".join(f"'{img}'" for img in images)
replacement = f"    const SURPRISE_IMAGES = [{entries}];"

with open(INDEX_HTML, "r", encoding="utf-8") as fh:
    html = fh.read()

updated, count = re.subn(
    r"    const SURPRISE_IMAGES = \[.*?\];",
    replacement,
    html,
    flags=re.DOTALL,
)

if count == 0:
    raise SystemExit("Could not find SURPRISE_IMAGES in index.html")

with open(INDEX_HTML, "w", encoding="utf-8") as fh:
    fh.write(updated)

print(f"Updated SURPRISE_IMAGES with {len(images)} image(s): {images}")
