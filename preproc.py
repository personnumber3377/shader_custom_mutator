#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import struct
import sys
from pathlib import Path

# -----------------------------
# ANGLE fuzz header constants
# -----------------------------

SHADER_TYPE_FRAGMENT = 0x8B30        # GL_FRAGMENT_SHADER
SHADER_SPEC_GLES3 = 2                # SH_GLES3_SPEC
OUTPUT_SPIRV_VULKAN = 15             # SH_SPIRV_VULKAN_OUTPUT

HEADER_SIZE = 128


# -----------------------------
# Regexes
# -----------------------------

RE_LINE_COMMENT = re.compile(r"//.*?$", re.MULTILINE)
RE_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

RE_DIRECTIVE = re.compile(r"^\s*#.*?$", re.MULTILINE)

# Matches:
#   layout (...) in;
#   layout (...) out;
#   layout (...) buffer foo { ... };
#   layout (...) uniform foo { ... };
RE_LAYOUT_STATEMENT = re.compile(
    r"""
    layout\s*\([^)]*\)          # layout(...)
    \s*
    (
        (in|out)\s*;            # layout(...) in;
      |                         # OR
        (uniform|buffer)\s+\w+  # layout(...) buffer Name
        \s*\{.*?\}\s*;          # { ... };
    )
    """,
    re.DOTALL | re.VERBOSE,
)


# -----------------------------
# Cleaning logic
# -----------------------------

def clean_shader_source(src: str) -> str:
    """
    Remove comments, directives, and layout declarations.
    """

    # Remove comments
    src = RE_BLOCK_COMMENT.sub("", src)
    src = RE_LINE_COMMENT.sub("", src)

    # Remove preprocessor directives
    src = RE_DIRECTIVE.sub("", src)

    # Remove layout(...) declarations
    src = RE_LAYOUT_STATEMENT.sub("", src)

    # Normalize whitespace
    lines = [ln.rstrip() for ln in src.splitlines()]
    lines = [ln for ln in lines if ln.strip()]

    return "\n".join(lines) + "\n"


# -----------------------------
# Header construction
# -----------------------------

def build_angle_header() -> bytes:
    compile_flags = (1 << 0)  # objectCode enabled
    compile_opts = compile_flags.to_bytes(32, byteorder="little")

    header = struct.pack(
        "<III",
        SHADER_TYPE_FRAGMENT,
        SHADER_SPEC_GLES3,
        OUTPUT_SPIRV_VULKAN,
    )
    header += compile_opts
    header += b"\x00" * (HEADER_SIZE - len(header))
    return header


# -----------------------------
# Main processing
# -----------------------------

def process_shader(in_path: Path, out_clean: Path, out_fuzz: Path):
    src = in_path.read_text(errors="ignore")

    cleaned = clean_shader_source(src)

    # Save cleaned GLSL
    clean_path = out_clean / in_path.name
    clean_path.write_text(cleaned)

    # Build fuzzer input
    header = build_angle_header()
    fuzz_bytes = header + cleaned.encode("utf-8") + b"\x00"

    fuzz_path = out_fuzz / (in_path.stem + ".bin")
    fuzz_path.write_bytes(fuzz_bytes)


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input_dir> <out_clean_dir> <out_fuzz_dir>")
        sys.exit(1)

    in_dir = Path(sys.argv[1])
    out_clean = Path(sys.argv[2])
    out_fuzz = Path(sys.argv[3])

    out_clean.mkdir(parents=True, exist_ok=True)
    out_fuzz.mkdir(parents=True, exist_ok=True)

    for p in sorted(in_dir.iterdir()):
        if p.suffix not in {".glsl", ".vert", ".frag", ".comp"}:
            continue

        try:
            process_shader(p, out_clean, out_fuzz)
            print(f"[+] {p.name}")
        except Exception as e:
            print(f"[!] Failed {p.name}: {e}")


if __name__ == "__main__":
    main()