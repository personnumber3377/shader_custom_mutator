#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import random
import struct
import argparse
import tempfile
import subprocess
import traceback
from typing import Tuple, List

# -----------------------------
# Imports from your project
# -----------------------------

import shader_parser
import shader_mutator
import shader_unparser
import mutator

from test_helpers import (
    HEADER_SIZE,
    PRINT_LIMIT,
    strip_header_and_null,
)

# -----------------------------
# Checker (MANDATORY)
# -----------------------------

CHECKER_PATH = "./newest_angle"
TIMEOUT = 5.0

def check_file_bytes(data: bytes) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".bin", delete=False) as f:
        fname = f.name
        f.write(data)

    try:
        proc = subprocess.run(
            [CHECKER_PATH, fname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    finally:
        try:
            os.unlink(fname)
        except Exception:
            pass

    stderr = proc.stderr or ""
    ok = "SUCCESS" in stderr
    return ok, stderr.strip()

# -----------------------------
# HEADER parsing (text shaders)
# -----------------------------

GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER   = 0x8B31

SPEC_FLAGS = {
    0: "-s=e2",
    1: "-s=w",
    2: "-s=e3",
    3: "-s=w2",
    4: "-s=e31",
    5: "-s=w3",
    6: "-s=e32",
}

OUTPUT_FLAGS = {
    0: None,
    1: "-b=e",
    2: "-b=g",
    3: "-b=g130",
    4: "-b=g140",
    5: "-b=g150",
    6: "-b=g330",
    7: "-b=g400",
    8: "-b=g410",
    9: "-b=g420",
    10: "-b=g430",
    11: "-b=g440",
    12: "-b=g450",
    13: "-b=h9",
    14: "-b=h11",
    15: "-b=v",
    16: "-b=m",
}

def build_header_from_directive(src: str) -> bytes:
    """
    HEADER: <shader_type> <spec> <output>
    Example:
      HEADER: frag 3 6
    """
    lines = src.splitlines()
    if not lines or not lines[0].startswith("HEADER:"):
        raise ValueError("Missing HEADER directive")

    _, rest = lines[0].split("HEADER:", 1)
    parts = rest.strip().split()
    if len(parts) != 3:
        raise ValueError("Invalid HEADER format")

    stype_s, spec_s, out_s = parts

    shader_type = {
        "frag": GL_FRAGMENT_SHADER,
        "vert": GL_VERTEX_SHADER,
    }.get(stype_s)

    if shader_type is None:
        raise ValueError("Unknown shader type")

    spec = int(spec_s)
    output = int(out_s)

    header = bytearray(HEADER_SIZE)
    struct.pack_into("<III", header, 0, shader_type, spec, output)
    return bytes(header)

def load_text_shader(path: str) -> bytes:
    src = open(path, "r", encoding="utf-8").read()
    header = build_header_from_directive(src)
    body = "\n".join(src.splitlines()[1:]).encode("utf-8")
    return header + body + b"\x00"

def text_to_binary(src_path: str, out_path: str):
    src = open(src_path, "r", encoding="utf-8").read()
    header = build_header_from_directive(src)
    body = "\n".join(src.splitlines()[1:]).encode("utf-8")
    blob = header + body + b"\x00"

    with open(out_path, "wb") as f:
        f.write(blob)

    print(f"[text→bin] {src_path} -> {out_path}")

def binary_to_text(bin_path: str, out_path: str):
    data = open(bin_path, "rb").read()
    shader_type, spec, output = struct.unpack_from("<III", data, 0)

    shader_type_str = "vert" if shader_type == GL_VERTEX_SHADER else "frag"
    header_line = f"HEADER: {shader_type_str} {spec} {output}"

    body = strip_header_and_null(data).decode("utf-8", errors="ignore")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header_line + "\n" + body)

    print(f"[bin→text] {bin_path} -> {out_path}")

# -----------------------------
# Utilities
# -----------------------------

def collect_files(path: str) -> List[str]:
    if os.path.isfile(path):
        return [path]
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]

# -----------------------------
# Tests
# -----------------------------

def mutation_benchmark(path: str, iters: int, seed: int):
    files = collect_files(path)
    random.seed(seed)
    mutator.init(seed)

    total = 0
    success = 0

    for i in range(iters):
        fn = random.choice(files)
        data = load_text_shader(fn) if fn.endswith(".glsl") else open(fn, "rb").read()

        ok, _ = check_file_bytes(data)
        if not ok:
            continue
        try:
            mutated = mutator.fuzz(bytearray(data), None, 1_000_000)
            ok2, _ = check_file_bytes(mutated)
        except Exception as e: # TODO: The mutator may fail for example with "ValueError: invalid literal for int() with base 10: 'c'" ... Please fix this!
            total += 1
            continue
        total += 1
        success += int(ok2)

        if total and total % 10 == 0:
            print(f"[{total}] success rate = {success/total:.2%}")

    print("\n=== RESULT ===")
    print(f"Total mutations: {total}")
    print(f"Valid mutations: {success}")
    print(f"Success rate:    {success/total:.2%}")

def roundtrip_test(path: str):
    files = collect_files(path)

    for i, fn in enumerate(files):
        print(f"[roundtrip] {fn} ({i}/{len(files)})")
        data = load_text_shader(fn) if fn.endswith(".glsl") else open(fn, "rb").read()
        # print("passing this here: "+str(data))
        ok, msg = check_file_bytes(data)
        if not ok:
            raise RuntimeError(f"Initial shader invalid:\n{msg}")

        src = strip_header_and_null(data).decode("utf-8")
        print("Passing this source code: "+str(src))
        tu = shader_parser.parse_to_tree(src)
        out = shader_unparser.unparse_tu(tu)
        print("Got this source code back: "+str(out))

        rebuilt = data[:HEADER_SIZE] + out.encode("utf-8") + b"\x00"
        ok2, msg2 = check_file_bytes(rebuilt)

        if not ok2:
            raise RuntimeError(f"Roundtrip failed:\n{msg2}")

    print("✔ Roundtrip tests passed")

def add_default_header_to_directory(
    directory: str,
    default_header: str = "HEADER: frag 3 6"
):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue

        # Skip binaries
        try:
            data = open(path, "rb").read()
            data.decode("utf-8")
        except Exception:
            continue

        with open(path, "r", encoding="utf-8") as f:
            src = f.read()

        if src.startswith("HEADER:"):
            continue  # already has header

        print(f"[add-header] {path}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(default_header + "\n" + src)

def corpus_check(path: str):
    total = 0
    failures = 0

    for fn in sorted(collect_files(path)):
        data = open(fn, "rb").read()
        ok, msg = check_file_bytes(data)
        total += 1

        if not ok:
            failures += 1
            if failures <= PRINT_LIMIT:
                print("=" * 60)
                print(f"FAIL: {fn}")
                print(msg)

    print("\n=== SUMMARY ===")
    print(f"Total checked: {total}")
    print(f"Failures:     {failures}")
    print(f"Success:      {total - failures}")

# -----------------------------
# CLI
# -----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="file or directory")
    ap.add_argument("--mutation-bench", action="store_true")
    ap.add_argument("--roundtrip", action="store_true")
    ap.add_argument("--check-corpus", action="store_true")
    ap.add_argument("--iters", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--add-default-header", action="store_true",
                help="Add default HEADER to all text shaders in directory")
    ap.add_argument("--text-to-bin", action="store_true",
                help="Convert text shader to binary format")
    ap.add_argument("--bin-to-text", action="store_true",
                help="Convert binary shader to text format")
    args = ap.parse_args()

    seed = args.seed or random.randrange(1 << 30)
    print(f"[seed] {seed}")

    try:
        if args.mutation_bench:
            mutation_benchmark(args.path, args.iters, seed)
        elif args.roundtrip:
            roundtrip_test(args.path)
        elif args.check_corpus:
            corpus_check(args.path)
        elif args.add_default_header:
            if not os.path.isdir(args.path):
                ap.error("--add-default-header requires a directory")
            add_default_header_to_directory(args.path)
        elif args.text_to_bin:
            if not os.path.isfile(args.path):
                ap.error("--text-to-bin requires a file")
            out = args.path + ".bin"
            text_to_binary(args.path, out)
        elif args.bin_to_text:
            if not os.path.isfile(args.path):
                ap.error("--bin-to-text requires a file")
            out = args.path + ".glsl"
            binary_to_text(args.path, out)
        else:
            ap.error("no test selected")
    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()