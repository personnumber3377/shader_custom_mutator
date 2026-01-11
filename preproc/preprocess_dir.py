#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile

HEADER_SIZE = 128
NULL_BYTE = b"\x00"

import re

UINT_SUFFIX_RE = re.compile(rb'\b(\d+)u\b')

# :D
def sanitize_preprocessor_uints(src: bytes) -> bytes:
    out = []
    for line in src.splitlines(keepends=True):
        if line.lstrip().startswith(b"#"):
            line = UINT_SUFFIX_RE.sub(rb'\1', line)
        out.append(line)
    return b"".join(out)

def preprocess_shader_blob(blob: bytes) -> bytes:
    assert len(blob) > HEADER_SIZE
    assert blob.endswith(NULL_BYTE)

    header = blob[:HEADER_SIZE]
    source = blob[HEADER_SIZE:-1]  # strip final \x00
    
    # Patch out problematic preproc macro shit...
    source = sanitize_preprocessor_uints(source)
    
    # Write source to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".glsl") as f:
        f.write(source)
        src_path = f.name

    try:
        # Run glslang preprocessor
        result = subprocess.run(
            [
                "glslangValidator",
                "-E",
                "-S", "vert",
                src_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Preprocessing failed:\n{result.stderr.decode(errors='ignore')}"
            )

        preprocessed = result.stdout

        # glslang sometimes adds #line directives — keep them
        return header + preprocessed + NULL_BYTE

    finally:
        os.unlink(src_path)

def preprocess_directory(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for name in os.listdir(input_dir):
        in_path = os.path.join(input_dir, name)
        out_path = os.path.join(output_dir, name)

        if not os.path.isfile(in_path):
            continue

        with open(in_path, "rb") as f:
            blob = f.read()

        try:
            new_blob = preprocess_shader_blob(blob)
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            continue

        with open(out_path, "wb") as f:
            f.write(new_blob)

        print(f"[OK] {name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_dir> <output_dir>")
        sys.exit(1)

    preprocess_directory(sys.argv[1], sys.argv[2])