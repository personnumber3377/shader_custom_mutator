#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

# -----------------------------
# ANGLE fuzz header constants
# -----------------------------

SHADER_TYPE_FRAGMENT = 0x8B30
SHADER_SPEC_GLES3 = 2
OUTPUT_SPIRV_VULKAN = 15
HEADER_SIZE = 128

# -----------------------------
# Regexes
# -----------------------------

RE_LINE_COMMENT = re.compile(r"//.*?$", re.MULTILINE)
RE_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
RE_DIRECTIVE = re.compile(r"^\s*#(?!include).*?$", re.MULTILINE)

RE_INCLUDE = re.compile(
    r'^\s*#include\s+"([^"]+)"\s*$',
    re.MULTILINE
)

RE_LAYOUT_STATEMENT = re.compile(
    r"""
    layout\s*\([^)]*\)
    \s*
    (
        (in|out)\s*;
      |
        (uniform|buffer)\s+\w+\s*\{.*?\}\s*;
    )
    """,
    re.DOTALL | re.VERBOSE,
)

# -----------------------------
# Include expansion
# -----------------------------

def expand_includes(path: Path, seen: set[Path]) -> str:
    if path in seen:
        return ""
    seen.add(path)

    src = path.read_text(errors="ignore")
    out = []

    for line in src.splitlines():
        m = RE_INCLUDE.match(line)
        if m:
            inc = (path.parent / m.group(1)).resolve()
            if inc.exists():
                out.append(expand_includes(inc, seen))
            continue
        out.append(line)

    return "\n".join(out)

# -----------------------------
# Cleaning logic
# -----------------------------

def clean_shader_source(src: str) -> str:
    # ERROR: 0:4: 'highp' : precision is not supported in fragment shader
    src = RE_BLOCK_COMMENT.sub("", src)
    src = RE_LINE_COMMENT.sub("", src)
    src = RE_DIRECTIVE.sub("", src)
    src = RE_LAYOUT_STATEMENT.sub("", src)

    # Remove float suffixes: 1.0f → 1.0
    src = re.sub(r'(\d+\.\d+)f\b', r'\1', src)

    # Remove empty arguments as void to just empty paranthesis...

    src = src.replace("(void)", "()") # Do the stuff...
    src = src.replace("highp", "mediump") # Replace the highp things with mediump because the shader may not support that...
    lines = [ln.rstrip() for ln in src.splitlines() if ln.strip()]
    return "\n".join(lines)

# -----------------------------
# Header construction
# -----------------------------

def build_angle_header() -> bytes:
    flags = (1 << 0)
    opts = flags.to_bytes(32, "little")
    hdr = struct.pack("<III", SHADER_TYPE_FRAGMENT, SHADER_SPEC_GLES3, OUTPUT_SPIRV_VULKAN)
    hdr += opts
    hdr += b"\x00" * (HEADER_SIZE - len(hdr))
    return hdr

# -----------------------------
# Main processing
# -----------------------------

def process_shader(path: Path, out_clean: Path, out_fuzz: Path):
    expanded = expand_includes(path.resolve(), set())
    cleaned = clean_shader_source(expanded)

    final_src = (
        # "#version 310 es\n"
        "#define ERROR_EPSILON 0.1\n"
        "precision mediump float;\n"
        "precision mediump int;\n\n"
        + cleaned
        + "\n"
    )

    clean_path = out_clean / path.name
    clean_path.write_text(final_src)

    fuzz_bytes = build_angle_header() + final_src.encode() + b"\x00"
    fuzz_path = out_fuzz / (path.stem + ".bin")
    fuzz_path.write_bytes(fuzz_bytes)

# -----------------------------
# Entry point
# -----------------------------

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input_dir> <out_clean> <out_fuzz>")
        sys.exit(1)

    in_dir = Path(sys.argv[1])
    out_clean = Path(sys.argv[2])
    out_fuzz = Path(sys.argv[3])

    out_clean.mkdir(parents=True, exist_ok=True)
    out_fuzz.mkdir(parents=True, exist_ok=True)

    for p in in_dir.rglob("*"):
        if p.suffix in {".glsl", ".frag", ".vert", ".comp"}:
            try:
                process_shader(p, out_clean, out_fuzz)
                print(f"[+] {p}")
            except Exception as e:
                print(f"[!] {p}: {e}")

if __name__ == "__main__":
    main()