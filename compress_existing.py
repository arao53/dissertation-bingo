#!/usr/bin/env python3
"""Compress existing PNGs/JPGs in surprise/ to WebP, then delete the originals."""

import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SURPRISE_DIR = os.path.join(ROOT, "surprise")
MAX_SIDE = 1200
WEBP_QUALITY = 80


def compress(src):
    base = os.path.splitext(src)[0]
    out = base + ".webp"
    before = os.path.getsize(src)

    # -auto-orient applies EXIF rotation before any other operation
    subprocess.run([
        "magick", src,
        "-auto-orient",
        "-resize", f"{MAX_SIDE}x{MAX_SIDE}>",
        "-quality", str(WEBP_QUALITY),
        out,
    ], capture_output=True, check=True)

    return out, before, os.path.getsize(out)


def main():
    exts = {".png", ".jpg", ".jpeg"}
    files = sorted(
        f for f in os.listdir(SURPRISE_DIR)
        if os.path.splitext(f)[1].lower() in exts
    )
    if not files:
        print("No image files found.")
        return

    total_before = total_after = 0

    for fname in files:
        src = os.path.join(SURPRISE_DIR, fname)
        out, before, after = compress(src)
        total_before += before
        total_after += after
        os.remove(src)
        print(f"{fname}  {before/1e6:.1f}MB -> {os.path.basename(out)}  {after/1e6:.1f}MB  ({100*after/before:.0f}%)")

    print(f"\nTotal: {total_before/1e6:.1f} MB -> {total_after/1e6:.1f} MB  (saved {(total_before-total_after)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
