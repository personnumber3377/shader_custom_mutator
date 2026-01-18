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
import time
import copy
from typing import Tuple, List

# -----------------------------
# Imports from your project
# -----------------------------

import shader_parser
import shader_mutator
import shader_unparser
import mutator

import cProfile
import pstats

from test_helpers import (
    HEADER_SIZE,
    PRINT_LIMIT,
    strip_header_and_null,
    PRINT_COUNT,
)

# -----------------------------
# Checker (MANDATORY)
# -----------------------------

CHECKER_PATH = "./newest_angle"
TIMEOUT = 5.0

# These are for the actual fuzzing benchmark...

# ANGLE_BIN = "./angle_translator_fuzzer"
ANGLE_BIN = CHECKER_PATH
ASSERT_NEEDLE = b"stripStructSpecifierSamplers"
ASSERT_OUTDIR = "assert_hits"
ASSERT_TIMEOUT = 5.0 # 2.0
# PRINT_COUNT = 
INPUT_FILE = "./input.bin"

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

def save_file(fn: str, data: bytes):
    fh = open(fn, "wb")
    fh.write(data)
    fh.close()

def expected_out_path(fn: str) -> str:
    return fn + ".expected_out"

def load_expected_out(fn: str) -> str | None:
    p = expected_out_path(fn)
    if not os.path.isfile(p):
        return None
    return open(p, "r", encoding="utf-8").read()

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

def run_angle_and_check(path: str) -> bool:
    try:
        p = subprocess.run(
            [ANGLE_BIN, path],
            # input=buf,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=ASSERT_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return False

    combined = p.stdout + p.stderr
    # print("combined: "+str(combined))
    return ASSERT_NEEDLE in combined

def collect_files(path: str) -> List[str]:
    if os.path.isfile(path):
        return [path]
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f)) and not f.endswith(".expected_out") # Filter out the expected output files...
    ]

# -----------------------------
# Tests
# -----------------------------

def chase_assert_with_custom_mutator(
    seed_path: str,
    max_iters: int = 1_000_000,
):
    os.makedirs(ASSERT_OUTDIR, exist_ok=True)

    with open(seed_path, "rb") as f:
        seed = bytearray(f.read())
    
    # Make a copy of the original payload...
    original_buf = copy.deepcopy(seed)

    # IMPORTANT: never mutate header
    header = seed[:HEADER_SIZE]
    body   = seed[HEADER_SIZE:]

    for i in range(max_iters):
        # reconstruct full buffer each iteration
        buf = bytearray(header + body)

        # mutate ONCE using your custom mutator
        # print("Passing this here: "+str(buf))

        # Wrapped in a try since the mutator has some bugs in it still...
        try:
            buf = mutator.fuzz(buf, None, 1_000_000)
        except Exception as e:
            continue
        # buf = original_buf # Actually use the original shit...

        # Now try to write the file and run the checker...

        with open(INPUT_FILE, "wb") as f:
            f.write(buf)

        if run_angle_and_check(INPUT_FILE): # Originally was buf
            ts = int(time.time())
            out = os.path.join(
                ASSERT_OUTDIR,
                f"assert_hit_{ts}_{i}.bin"
            )

            with open(out, "wb") as f:
                f.write(buf)

            print("🔥 ASSERT FOUND")
            print(f"Saved crashing input: {out}")
            return out

        if i % PRINT_COUNT == 0: # Was originally 1000
            print(f"[assert-chase] iterations: {i}")

    print("❌ No assert found")
    return None

# Generate expected outputs from the files...
def generate_expected_outputs(path: str, force: bool = False):
    files = collect_files(path)

    if not force:
        print("⚠️  This will CREATE or OVERWRITE .expected_out files.")
        print("⚠️  This can invalidate your roundtrip test corpus.")
        resp = input("Type 'YES' to continue: ")
        if resp.strip() != "YES":
            print("Aborted.")
            return

    for fn in files:
        data = load_text_shader(fn) if fn.endswith(".glsl") else open(fn, "rb").read()
        ok, _ = check_file_bytes(data)
        if not ok:
            print(f"[skip] invalid shader: {fn}")
            continue

        src = strip_header_and_null(data).decode("utf-8", errors="ignore")

        try:
            tu = shader_parser.parse_to_tree(src)
            out = shader_unparser.unparse_tu(tu)
        except Exception as e:
            print(f"[skip] parse failed: {fn}")
            continue

        out_path = expected_out_path(fn)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)

        print(f"[expected] {out_path}")

VERBOSE = 0

def mutation_benchmark(path: str, iters: int, seed: int):
    files = collect_files(path)
    random.seed(seed)
    # mutator.init(seed)

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
            ok2, err = check_file_bytes(mutated)
        except Exception as e: # TODO: The mutator may fail for example with "ValueError: invalid literal for int() with base 10: 'c'" ... Please fix this!
            if VERBOSE:
                print("Encountered this exception here: "+str(e))
                print("Original source code: "+str(strip_header_and_null(data).decode("utf-8")))
                exit(1)
            total += 1
            continue
        total += 1
        success += int(ok2)
        if err and VERBOSE:
            print("Mutation resulted in this error: "+str(err))
            print("Mutated soource code: "+str(strip_header_and_null(mutated).decode("utf-8")))
            print("Original source code: "+str(strip_header_and_null(data).decode("utf-8")))
        if total and total % 10 == 0:
            print(f"[{total}] success rate = {success/total:.2%}")

    print("\n=== RESULT ===")
    print(f"Total mutations: {total}")
    print(f"Valid mutations: {success}")
    print(f"Success rate:    {success/total:.2%}")

def profile_mutator(path: str, iters: int, seed: int):
    """
    Profile the Python custom mutator by running it repeatedly.
    - If `path` is a directory: pick random files
    - If `path` is a file: always mutate that file
    """

    print("[*] Profiling mutator")
    print("[*] Iterations:", iters)

    random.seed(seed)
    mutator.init(seed)

    # -----------------------------
    # Load corpus
    # -----------------------------
    if os.path.isfile(path):
        files = [path]
        print("[*] Using single file:", path)
    else:
        files = collect_files(path)
        print("[*] Corpus size:", len(files))

    if not files:
        print("❌ No input files found")
        return

    # Preload buffers to avoid disk I/O during profiling
    buffers = []
    for fn in files:
        try:
            data = load_text_shader(fn) if fn.endswith(".glsl") else open(fn, "rb").read()
            buffers.append(bytearray(data))
        except Exception:
            continue

    if not buffers:
        print("❌ No valid buffers loaded")
        return

    print("[*] Buffers loaded:", len(buffers))

    # -----------------------------
    # Hot loop (what we profile)
    # -----------------------------
    def run():
        for _ in range(iters):
            buf = random.choice(buffers)
            mutator.custom_mutator(buf, None, 10000) # Run the thing...
            '''
            try:
                # mutator.fuzz(buf, None, 10000)
                # Actually use the custom_mutator here...
                # custom_mutator(buf: bytearray, add_buf, max_size: int, callback=None)
                mutator.custom_mutator(buf, None, 10000) # Run the thing...
            except Exception:
                pass
            '''
            
    # -----------------------------
    # Run profiler
    # -----------------------------
    prof = cProfile.Profile()
    prof.enable()
    run()
    prof.disable()

    out_file = "mutator.prof"
    prof.dump_stats(out_file)

    print(f"✔ Profile written to {out_file}")
    print("👉 Inspect with:")
    print("   python3 -m pstats mutator.prof")
    print("   snakeviz mutator.prof")

def roundtrip_test(path: str, ignore_invalid: int = 0):
    files = collect_files(path)

    fail = 0
    tot = 0
    ignored = 0
    mismatch = 0

    for i, fn in enumerate(files):
        print(f"[roundtrip] {fn} ({i}/{len(files)})")

        if i and i % PRINT_COUNT == 0:
            print("Roundtrip stats:")
            print("Total:   ", tot)
            print("Failed:  ", fail)
            print("Ignored: ", ignored)
            print("Mismatch:", mismatch)

        data = load_text_shader(fn) if fn.endswith(".glsl") else open(fn, "rb").read()

        ok, msg = check_file_bytes(data)
        if not ok:
            ignored += 1
            print("Invalid shader (original)")
            print("msg:", msg)
            continue

        tot += 1

        src = strip_header_and_null(data).decode("utf-8", errors="ignore")

        try:
            tu = shader_parser.parse_to_tree(src)
            out = shader_unparser.unparse_tu(tu)
        except Exception as e:
            if ignore_invalid:
                ignored += 1
                continue
            raise

        # -----------------------------
        # Expected output comparison
        # -----------------------------
        expected = load_expected_out(fn)
        if expected is not None:
            if out != expected:
                mismatch += 1
                fail += 1
                print("❌ EXPECTED OUTPUT MISMATCH")
                print("--- expected ---")
                print(expected[:500])
                print("--- got ---")
                print(out[:500])
                continue

        rebuilt = data[:HEADER_SIZE] + out.encode("utf-8") + b"\x00"

        ok2, msg2 = check_file_bytes(rebuilt)
        if not ok2:
            fail += 1
            print("❌ Roundtrip ANGLE failure:")
            print(msg2)
            print("--- original ---")
            print(src[:500])
            print("--- got ---")
            print(out[:500])
            assert False

    print("\n=== ROUNDTRIP SUMMARY ===")
    print("Total tested: ", tot)
    print("Failures:     ", fail)
    print("Ignored:      ", ignored)
    print("Mismatches:   ", mismatch)

    if fail == 0:
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
            # Delete the files...
            os.system("rm "+str(fn))
        else:
            print("SUCCESS!")

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
    ap.add_argument("--chase-assert", action="store_true")
    ap.add_argument("--gen-expected-out", action="store_true", help="Generate .expected_out files (DANGEROUS)")
    ap.add_argument("--profile-mutator", action="store_true", help="Profile Python mutator performance (cProfile)")
    ap.add_argument("--iters", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--ignore-invalid", type=int, default=0)
    ap.add_argument("--add-default-header", action="store_true",
                help="Add default HEADER to all text shaders in directory")
    ap.add_argument("--text-to-bin", action="store_true",
                help="Convert text shader to binary format")
    ap.add_argument("--bin-to-text", action="store_true",
                help="Convert binary shader to text format")
    args = ap.parse_args()

    seed = args.seed or random.randrange(1 << 30)
    print(f"[seed] {seed}")

    # Initialize the seed to the actual mutator...
    mutator.init(seed)

    try:
        if args.mutation_bench:
            mutation_benchmark(args.path, args.iters, seed)
        elif args.chase_assert:
            chase_assert_with_custom_mutator(args.path)
            # exit(0)
        elif args.profile_mutator:
            profile_mutator(args.path, args.iters, seed)
        elif args.roundtrip:
            roundtrip_test(args.path, ignore_invalid=args.ignore_invalid)
        elif args.gen_expected_out:
            generate_expected_outputs(args.path)
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