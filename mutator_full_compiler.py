#!/usr/bin/env python3
from __future__ import annotations

import sys
import random
import traceback
from typing import Optional

# -----------------------------
# Shader toolchain
# -----------------------------

import shader_parser
import shader_mutator
import shader_unparser

from shader_ast import *

sys.setrecursionlimit(50000)

# -----------------------------
# Debug
# -----------------------------

DEBUG = False

def save_crashing(buffer: bytes):
    return
    # with open("/home/oof/crashing_input.bin", "wb") as f:
    #     f.write(buffer)

# -----------------------------
# Config
# -----------------------------

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
        a = rng.randrange(len(b) - 1)
        c = rng.randrange(a + 1, len(b))
        return b[:a] + b[c:]

    if op == 1:
        pos = rng.randrange(len(b))
        return b[:pos] + bytes([rng.randrange(256)]) + b[pos:]

    pos = rng.randrange(len(b))
    return b[:pos] + bytes([b[pos] ^ (1 << rng.randrange(8))]) + b[pos + 1:]

# -----------------------------
# Structural shader mutation
# -----------------------------

def mutate_shader_structural(shader_bytes: bytes, max_size: int, rng: random.Random) -> bytearray:
    src = shader_bytes.decode("utf-8", errors="ignore")

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
    if not _initialized:
        init(0)

    if not isinstance(buf, (bytes, bytearray)):
        return buf

    rng = random.Random(random.randrange(1 << 30))

    try:
        if not buf:
            return bytearray(mutate_bytes_generic(bytes(buf), rng))

        mutated_body = mutate_shader_structural(bytes(buf), max_size, rng)
        return mutated_body

    except Exception:
        if not ENABLE_FALLBACK:
            save_crashing(bytes(buf))
            raise

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
    except Exception:
        return buf

# -----------------------------
# libFuzzer custom crossover
# -----------------------------

def custom_crossover(data1: bytes, data2: bytes, max_size: int, seed: int):
    random.seed(seed)

    try:
        s1 = data1.decode("utf-8", errors="ignore")
        s2 = data2.decode("utf-8", errors="ignore")

        try:
            tu1 = shader_parser.parse_to_tree(s1)
            tu2 = shader_parser.parse_to_tree(s2)
        except Exception:
            cut = random.randrange(min(len(data1), len(data2)))
            return (data1[:cut] + data2[cut:])[:max_size]

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

        stmts = list(m1.body.stmts)
        splice = random.sample(
            m2.body.stmts,
            k=min(len(m2.body.stmts), random.randint(1, 5))
        )

        insert_at = random.randrange(len(stmts) + 1)
        stmts[insert_at:insert_at] = splice
        m1.body.stmts = stmts

        def uniq(items):
            seen = set()
            out = []
            for it in items:
                k = repr(it)
                if k not in seen:
                    seen.add(k)
                    out.append(it)
            return out

        tu1.items = uniq(g1 + g2 + f1 + f2 + [m1])

        out_src = shader_unparser.unparse_tu(tu1)
        out = out_src.encode("utf-8", errors="ignore")

        return out[:max_size]

    except Exception:
        return data1[:max_size]

# -----------------------------
# CLI testing helper
# -----------------------------

def run_mutator(data: bytes):
    init(random.randrange(1 << 30))

    buf = bytearray(data)

    while True:
        try:
            buf = fuzz(buf, None, 1_000_000)
            print(buf.decode("utf-8", errors="ignore"))
        except Exception:
            continue

if __name__ == "__main__":
    import argparse, os

    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--iters", type=int, default=1)
    ap.add_argument("--mutate-only", type=int, default=0)
    args = ap.parse_args()

    seed = random.randrange(10_000_000)
    print("SEED:", seed)
    random.seed(seed)
    init(seed)

    if os.path.isdir(args.input):
        fn = random.choice(os.listdir(args.input))
        with open(os.path.join(args.input, fn), "rb") as f:
            data = f.read()
    else:
        with open(args.input, "rb") as f:
            data = f.read()

    if args.mutate_only:
        run_mutator(data)
        sys.exit(0)

    buf = bytearray(data)

    for _ in range(args.iters):
        buf = fuzz(buf, None, 1_000_000)

    with open(args.output, "wb") as f:
        f.write(buf)