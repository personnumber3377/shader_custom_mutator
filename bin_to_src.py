#!/usr/bin/env python3

# This script is supposed to take a directory of corpus files and then extract the source code out of them.

import os
import sys

FUZZ_HEADER_SIZE = 128

def extract_shader(path: str) -> str | None:
    with open(path, "rb") as f:
        data = f.read()

    if len(data) <= FUZZ_HEADER_SIZE:
        return None

    payload = data[FUZZ_HEADER_SIZE:]

    # Strip trailing NULLs
    payload = payload.rstrip(b"\x00")

    # Heuristic: GLSL should be ASCII / UTF-8 text
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None

    # Optional sanity check
    if "void main" not in text:
        # Still allow it, but you can uncomment this if you want strict filtering
        pass

    return text


def main(inp_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)

    count = 0
    skipped = 0

    for name in sorted(os.listdir(inp_dir)):
        in_path = os.path.join(inp_dir, name)
        if not os.path.isfile(in_path):
            continue

        src = extract_shader(in_path)
        if src is None:
            skipped += 1
            continue

        out_name = name + ".glsl"
        out_path = os.path.join(out_dir, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(src)

        count += 1

    print(f"[+] Extracted {count} shaders")
    print(f"[!] Skipped {skipped} non-text / invalid files")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_dir> <output_dir>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])