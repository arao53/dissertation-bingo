#!/usr/bin/env python3
"""Convert HEIC files in surprise/ to square-cropped WebPs with random 2-word names."""

import os
import random
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SURPRISE_DIR = os.path.join(ROOT, "surprise")
WORDS_FILE = "/usr/share/dict/words"
MAX_SIDE = 1200
WEBP_QUALITY = 80


def load_words():
    with open(WORDS_FILE) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha() and 4 <= len(w.strip()) <= 8]


def random_name(words, used):
    while True:
        name = f"{random.choice(words)}_{random.choice(words)}"
        if name not in used:
            used.add(name)
            return name


def convert(src, out):
    # -auto-orient applies EXIF rotation, then square center-crop, resize, convert to WebP
    subprocess.run([
        "magick", src,
        "-auto-orient",
        "-gravity", "Center",
        "-resize", f"{MAX_SIDE}x{MAX_SIDE}^",
        "-extent", f"{MAX_SIDE}x{MAX_SIDE}",
        "-quality", str(WEBP_QUALITY),
        out,
    ], capture_output=True, check=True)


def main():
    heic_files = sorted(f for f in os.listdir(SURPRISE_DIR) if f.upper().endswith(".HEIC"))
    if not heic_files:
        print("No HEIC files found.")
        return

    words = load_words()
    used_names = {os.path.splitext(f)[0] for f in os.listdir(SURPRISE_DIR)}

    for heic in heic_files:
        src = os.path.join(SURPRISE_DIR, heic)
        name = random_name(words, used_names)
        out = os.path.join(SURPRISE_DIR, f"{name}.webp")
        convert(src, out)
        os.remove(src)
        print(f"{heic} -> {name}.webp")

    print(f"\nConverted {len(heic_files)} file(s).")


if __name__ == "__main__":
    main()
