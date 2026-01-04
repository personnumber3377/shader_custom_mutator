#!/usr/bin/env python3
import sys
import struct
from pathlib import Path
from collections import Counter

GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER   = 0x8B31
GL_COMPUTE_SHADER  = 0x91B9

def classify_shader(path: Path):
    try:
        with path.open("rb") as f:
            hdr = f.read(4)
            if len(hdr) < 4:
                return "too_short"
            shader_type, = struct.unpack("<I", hdr)
    except Exception:
        return "read_error"

    if shader_type == GL_VERTEX_SHADER:
        return "vertex"
    elif shader_type == GL_FRAGMENT_SHADER:
        return "fragment"
    elif shader_type == GL_COMPUTE_SHADER:
        return "compute"
    else:
        return f"other_0x{shader_type:04x}"

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)

    root = Path(sys.argv[1])
    if not root.is_dir():
        print("Error: not a directory")
        sys.exit(1)

    counts = Counter()
    total = 0

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        total += 1
        kind = classify_shader(p)
        counts[kind] += 1

    print("Shader type distribution:\n")

    for k, v in counts.most_common():
        pct = (v / total) * 100 if total else 0
        print(f"{k:12s} : {v:6d}  ({pct:6.2f}%)")

    print(f"\nTotal files: {total}")

if __name__ == "__main__":
    main()