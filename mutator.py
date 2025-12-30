#!/usr/bin/env python3
from __future__ import annotations

import sys
import random
import traceback
import os
from typing import Optional

# -----------------------------
# Shader toolchain
# -----------------------------

import shader_parser
import shader_mutator
import shader_unparser

sys.setrecursionlimit(50000)

# -----------------------------
# Debug
# -----------------------------

DEBUG = False

def save_crashing(buffer): # Saves the crashing file for debugging...
    fh = open("/home/oof/crashing_input.bin", "wb")
    fh.write(buffer)
    fh.close()
    return

# -----------------------------
# Config
# -----------------------------

HEADER_SIZE = 128          # bytes reserved for directives / comments
MAX_HEADER_MUT = 16        # max bytes to mutate in header
# ENABLE_FALLBACK = True    # generic byte fallback if AST path fails

ENABLE_FALLBACK = False

_initialized = False


# -----------------------------
# Generic byte fallback
# -----------------------------

def mutate_bytes_generic(b: bytes, rng: random.Random) -> bytes:
    if not b:
        return bytes([rng.randrange(256)])

    op = rng.randrange(3)

    if op == 0 and len(b) > 1:
        # delete slice
        a = rng.randrange(len(b) - 1)
        c = rng.randrange(a + 1, len(b))
        return b[:a] + b[c:]

    if op == 1:
        # insert random byte(s)
        pos = rng.randrange(len(b))
        return b[:pos] + bytes([rng.randrange(256)]) + b[pos:]

    # flip byte
    pos = rng.randrange(len(b))
    return b[:pos] + bytes([b[pos] ^ (1 << rng.randrange(8))]) + b[pos + 1:]


# -----------------------------
# Header mutation
# -----------------------------

def mutate_header(header: bytes, rng: random.Random) -> bytes:
    h = bytearray(header)

    n = rng.randrange(1, MAX_HEADER_MUT + 1)
    for _ in range(n):
        if not h:
            break
        i = rng.randrange(len(h))
        h[i] ^= (1 << rng.randrange(8))

    return bytes(h)


# -----------------------------
# Structural shader mutation
# -----------------------------

def mutate_shader_structural(shader_bytes: bytes, max_size: int, rng: random.Random) -> bytearray:
    """
    Core shader AST mutation.
    """
    src = shader_bytes.decode("utf-8", errors="ignore")

    # Parse → mutate → unparse
    tu = shader_parser.parse_to_tree(src)
    mutated = shader_mutator.mutate_translation_unit(tu, rng)
    out_src = shader_unparser.unparse_tu(mutated)

    out = out_src.encode("utf-8", errors="ignore")
    return bytearray(out[:max_size])


# -----------------------------
# AFL++ API
# -----------------------------

def init(seed: int):
    global _initialized
    if _initialized:
        return
    random.seed(seed)
    _initialized = True


def deinit():
    global _initialized
    _initialized = False


def fuzz(buf: bytearray, add_buf, max_size: int) -> bytearray:
    """
    AFL++ custom mutator entrypoint.
    """
    if not _initialized:
        init(0)

    if not isinstance(buf, (bytes, bytearray)):
        return buf

    rng = random.Random(random.randrange(1 << 30))

    try:
        if len(buf) <= HEADER_SIZE:
            return bytearray(mutate_bytes_generic(bytes(buf), rng)) # buf
            # raise ValueError("buffer too small")

        header = bytes(buf[:HEADER_SIZE])
        body = bytes(buf[HEADER_SIZE:])

        # Check for the last null byte here...

        if body[-1] == 0x00: # Strip null byte
            body = body[:-1]

        # mutate header lightly
        header = mutate_header(header, rng)

        # structural mutation
        mutated_body = mutate_shader_structural(body, max_size - HEADER_SIZE, rng)

        out = bytearray()
        out.extend(header)
        out.extend(mutated_body)
        out.extend(bytes([0x00])) # Add the null byte

        assert out[-1] == 0x00 # Check for the last null byte...

        return out[:max_size]

    except Exception:
        if not ENABLE_FALLBACK:
            save_crashing(buf)
            raise

        # Fallback: byte-level mutation of entire buffer
        try:
            mutated = mutate_bytes_generic(bytes(buf), rng)
            return bytearray(mutated[:max_size])
        except Exception:
            return buf


# -----------------------------
# libFuzzer entrypoint
# -----------------------------

def custom_mutator(buf: bytearray, add_buf, max_size: int, callback=None) -> bytearray:
    try:
        return fuzz(buf, add_buf, max_size)
    except Exception as e:
        try:
            with open("custom_mutator.log", "a") as f:
                f.write(f"mutator exception: {e}\n")
                traceback.print_exc(file=f)
        except Exception:
            pass
        return buf


# -----------------------------
# CLI testing helper
# -----------------------------

from test_helpers import *

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="input shader")
    ap.add_argument("output", help="output shader")
    ap.add_argument("--iters", type=int, default=1)
    args = ap.parse_args()

    seed = 5660207
    print("SEED: "+str(seed))

    random.seed(seed)

    inp = args.input

    if os.path.isdir(inp): # Select a random file as input from the thing...
        fn = random.choice(os.listdir(inp))
        if inp[-1] != "/":
            inp = inp + "/"
        # Now construct the full filename...
        fn = inp + fn
        with open(fn, "rb") as f:
            data = f.read()
    else:
        with open(inp, "rb") as f:
            data = f.read()

    # if len(data) < HEADER_SIZE:
    # Always prepend the header...
    data = b"\x00" * HEADER_SIZE + data

    # seed = random.randrange(10000000) # 5 # Modify this to appropriate values when debugging...
    
    # init(random.randrange(100000)) # Random shit here...
    
    init(seed)

    buf = bytearray(data)

    try:

        for _ in range(args.iters):
            buf = fuzz(buf, None, 1_000_000)

            source = strip_header_and_null(buf, header_len=HEADER_SIZE).decode("utf-8")
            print(source)

            ok, out = run_external_checker(buf, header_len=HEADER_SIZE)

            if not ok: # Produced invalid syntax???
                print("External syntax checker failed with: "+str(out))
                fh = open("failed.glsl", "w")
                fh.write(source)
                fh.close()
                exit(1)

            # Save mutated output...
            fh = open("mutated.bin", "wb")
            fh.write(buf)
            fh.close()
        with open(args.output, "wb") as f:
            f.write(buf)
    except Exception as e:
        traceback.print_exc()
        print("FAIL: "+str(e))


