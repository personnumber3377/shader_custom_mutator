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

# This is required for the crossover stuff...

from shader_ast import * # The stuff...

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
        print("poopooo")
        init(0)

    if not isinstance(buf, (bytes, bytearray)):
        return buf

    rng = random.Random(random.randrange(1 << 30))

    try:
        if len(buf) <= HEADER_SIZE:
            exit(1)
            return bytearray(mutate_bytes_generic(bytes(buf), rng)) # buf
            # raise ValueError("buffer too small")

        header = bytes(buf[:HEADER_SIZE])
        body = bytes(buf[HEADER_SIZE:])

        # Check for the last null byte here...

        if body[-1] == 0x00: # Strip null byte
            body = body[:-1]

        # mutate header lightly
        # header = mutate_header(header, rng) # TODO: This almost always produces invalid headers. Disabled for now.

        # structural mutation
        mutated_body = mutate_shader_structural(body, max_size - HEADER_SIZE, rng)

        out = bytearray()
        out.extend(header)
        out.extend(mutated_body)
        out.extend(bytes([0x00])) # Add the null byte

        assert out[-1] == 0x00 # Check for the last null byte...

        return out[:max_size]

    except Exception:
        # print("FUCK!")
        if not ENABLE_FALLBACK:
            save_crashing(buf)
            raise
        # assert False
        exit(1)
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
# libFuzzer entrypoint for custom crossover
# -----------------------------


def custom_crossover(data1, data2, max_size, seed):
    # import random
    random.seed(seed)

    # fh = open("/home/oof/thestuff.txt", "wb")
    # fh.write(b"Called custom mut...")
    # fh.close()

    try:

        # --- 1. Split header / body ---
        def split(buf):
            header = buf[:128]
            body = buf[128:].rstrip(b"\x00").decode("ascii", errors="ignore")
            return header, body

        h1, s1 = split(data1)
        h2, s2 = split(data2)

        # --- 2. Parse both ---
        try:
            tu1 = shader_parser.parse_to_tree(s1)
            tu2 = shader_parser.parse_to_tree(s2)
        except Exception:
            # fallback to simple byte crossover
            cut = random.randrange(min(len(data1), len(data2)))
            return (data1[:cut] + data2[cut:])[:max_size]

        # --- 3. Classify items ---
        def split_items(tu):
            globals_, funcs, main = [], [], None
            for it in tu.items:
                if isinstance(it, FunctionDef) and it.name == "main":
                    main = it
                elif isinstance(it, FunctionDef):
                    funcs.append(it)
                else:
                    globals_.append(it)
            return globals_, funcs, main

        g1, f1, m1 = split_items(tu1)
        g2, f2, m2 = split_items(tu2)

        if not m1 or not m2:
            return data1[:max_size]

        # --- 4. Merge main bodies ---
        stmts = list(m1.body.stmts)
        splice = random.sample(
            m2.body.stmts,
            k=min(len(m2.body.stmts), random.randint(1, 5))
        )
        insert_at = random.randrange(len(stmts) + 1)
        stmts[insert_at:insert_at] = splice
        m1.body.stmts = stmts

        # --- 5. Merge globals / funcs ---
        def uniq(items):
            seen = set()
            out = []
            for it in items:
                k = repr(it)
                if k not in seen:
                    seen.add(k)
                    out.append(it)
            return out

        new_items = uniq(g1 + g2 + f1 + f2 + [m1])
        tu1.items = new_items

        # --- 6. Unparse ---
        out_src = shader_unparser.unparse_tu(tu1)
        out = h1 + out_src.encode("ascii") + b"\x00"

        return out[:max_size]
    except Exception as e:
        fh = open("/home/oof/thestuff.txt", "wb")
        fh.write(str(e).encode("utf-8"))
        fh.close()
        return data1[:max_size]



'''
def custom_crossover(data1: bytearray, data2: bytearray, max_size: int, seed: int) -> bytearray:
    fh = open("/home/oof/thestuff.txt", "wb")
    fh.write(b"someshit here")
    fh.close()
    return data1 # Just return the original data shit...
'''

# -----------------------------
# CLI testing helper
# -----------------------------

from test_helpers import *

def run_mutator(data: bytes): # Run only...
    # Now assume that data is only the source code of the shader, so add the header thing and then the final null byte...
    data = b"\x00"*128 + data + b"\x00" # Add the header and the final null byte...
    while True:
        try:
            buf = fuzz(data, None, 1_000_000)

            source = strip_header_and_null(buf).decode("utf-8")
            print("Mutated source:")
            print(source)
        except Exception as e:
            continue
    return


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="input shader")
    ap.add_argument("output", help="output shader")
    ap.add_argument("--iters", type=int, default=1)
    ap.add_argument("--mutate-only", type=int, default=0)
    args = ap.parse_args()

    # seed = 5660207
    seed = random.randrange(10000000)
    print("SEED: "+str(seed))

    random.seed(seed)

    inp = args.input

    if os.path.isdir(inp): # Select a random file as input from the thing...
        fn = random.choice(os.listdir(inp))
        if inp[-1] != "/":
            inp = inp + "/"
        # Now construct the full filename...
        fn = inp + fn
        print("Using "+str(fn)+" as input filename...")
    else:
        with open(inp, "rb") as f:
            data = f.read()

    if args.mutate_only:
        # Do the stuff...
        init(seed)
        run_mutator(data)
        exit(0)

    # if len(data) < HEADER_SIZE:
    # Always prepend the header...
    # Check for a null byte close to the start, if found, then assume header already appended...
    if b"\x00" not in data[:HEADER_SIZE]:
        data = b"\x00" * HEADER_SIZE + data
    # global _initialized
    # _initialized = True
    init(seed)

    buf = bytearray(data)

    # Run initial thing...

    ok, out = run_as_frag_and_vertex(buf, HEADER_SIZE)
    if not ok:
        print("Initial parse is: "+str(out))
        assert False
    # assert ok

    try:

        for _ in range(args.iters):
            buf = fuzz(buf, None, 1_000_000)

            source = strip_header_and_null(buf).decode("utf-8")
            print(source)

            ok, out = run_as_frag_and_vertex(buf, HEADER_SIZE)

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


