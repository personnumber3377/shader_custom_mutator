#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from debug import * # Debugging...

import traceback
import os
import io
import sys
import pickle
import hashlib
import random

'''

import traceback
import generic_mutator_bytes
import copy
import datetime
import decimal
import compare

'''

# These are the actual heavy lifting libraries that we need...

import shader_parser # For actually parsing the thing...
import shader_mutator

sys.setrecursionlimit(20000)

# -----------------------------
# Config / Globals
# -----------------------------

HEADER_SIZE = 128 # This is the header of the fuzzed input bytes...

# -----------------------------
# Generic fallback mutator (kept but NOT used as fallback per request)
# -----------------------------

def remove_substring(b: bytes, rng: random.Random) -> bytes:
    if len(b) < 2:
        return b
    start = rng.randrange(len(b)-1)
    end = rng.randrange(start+1, len(b))
    return b[:start] + b[end:]


def multiply_substring(b: bytes, rng: random.Random) -> bytes:
    if len(b) < 2:
        return b
    start = rng.randrange(len(b)-1)
    end = rng.randrange(start+1, len(b))
    substr = b[start:end]
    where = rng.randrange(len(b))
    return b[:where] + substr * (1 + rng.randrange(4)) + b[where:]


def add_character(b: bytes, rng: random.Random) -> bytes:
    where = rng.randrange(len(b)) if b else 0
    return b[:where] + bytes([rng.randrange(256)]) + b[where:]


def mutate_generic(b: bytes, rng: random.Random) -> bytes:
    if not b:
        return bytes([rng.randrange(256)])
    choice = rng.randrange(3)
    if choice == 0:
        return remove_substring(b, rng)
    elif choice == 1:
        return multiply_substring(b, rng)
    else:
        return add_character(b, rng)

def mutate_shader_structural(shader_buffer, max_length, rng):
    """
    Main mutator entrypoint. Mutates the shader source code in a way which hopefully keeps it syntactically intact.
    """

    shader_source = shader_buffer.decode("utf-8", errors="ignore") # Decode as utf8 and ignore errors...
    tree = parse_to_tree(shader_source) # Make a treelike structure out of it...
    mutated_tree = mutate_tree(tree) # Mutate
    new_source = unparse_from_tree(mutated_tree)
    new_bytes = new_source.encode("utf-8") # Encode to utf-8
    new_bytes = new_bytes[:max_length] # Cut off just in case...
    return bytearray(new_bytes) # Return as bytearray just in case...

# -----------------------------
# AFL++ API: init / deinit / fuzz_count / fuzz
# -----------------------------

def init(seed: int):
    """
    Called once by AFL at startup with a seed.
    We load resources DB but do NOT use the provided seed for per-input mutation randomness.
    """
    global _initialized, _resources_db, _mutation_count

    if _initialized:
        return

    # Load resources DB from pickle or PDF dir
    try:
        #while True:
        #    dlog("Paskaaaaa!!!!!")
        _resources_db = load_resources_db(DEFAULT_PDF_DIR, DEFAULT_PKL_PATH)
        if len(_resources_db) == 0:
            exit(0)
    except Exception as e:
        print("Warning: load_resources_db failed: %s" % e, file=sys.stderr)
        dlog("Warning: load_resources_db failed: %s" % e)
        exit(0)
        _resources_db = []

    _initialized = True
    return


def deinit():
    global _initialized
    _initialized = False


def fuzz_count(buf: bytearray) -> int:
    """
    Return how many fuzz cycles to perform for this buffer.
    If the buffer cannot be parsed as a PDF (pikepdf), return 0 to skip mutating.
    """
    if not isinstance(buf, (bytes, bytearray)):
        return 0
    if len(buf) <= HEADER_SIZE:
        return 0
    # attempt to parse PDF (exclude header)
    try:
        core = bytes(buf[HEADER_SIZE:])
        with pikepdf.open(io.BytesIO(core)) as pdf:
            # open succeeded; schedule mutations
            return _mutation_count
    except Exception:
        # invalid PDFs we don't attempt to mutate structurally
        return 0


def fuzz(buf: bytearray, add_buf, max_size: int) -> bytearray:
    """
    Perform a single mutation. buf is bytes/bytearray input.
    Preserve HEADER_SIZE bytes and mutate the rest.
    Raises on structural failure (no silent fallback).
    """

    try:

        if not _initialized:
            raise RuntimeError("mutator not initialized; call init(seed) before fuzz()")

        if not isinstance(buf, (bytes, bytearray)):
            raise ValueError("buf must be bytes or bytearray")

        if len(buf) <= HEADER_SIZE:
            raise ValueError("buf too small (<= HEADER_SIZE)")

        header = bytes(buf[:HEADER_SIZE])
        core = bytes(buf[HEADER_SIZE:])

        # rng = random.Random() # rng_from_buf(bytes(buf))  # deterministic RNG from buffer

        rand_thing = random.randrange(1000000000)
        rng = random.Random(rand_thing)

        mutated_core = mutate_shader_structural(core, max_size - HEADER_SIZE, rng)
        out = bytearray()
        out.extend(header)
        out.extend(mutated_core)
        if len(out) > max_size:
            out = out[:max_size]
        return out
    except Exception as exception:
        return generic_mutator_bytes.mutate_generic(bytes(buf))



# -----------------------------
# CLI helpers for maintenance (build pkl / test)
# -----------------------------
def cli_build_db(pdf_dir: str = None, pkl_path: str = None):
    pdf_dir = Path(pdf_dir or DEFAULT_PDF_DIR)
    pkl_path = Path(pkl_path or DEFAULT_PKL_PATH)
    db = build_resources_db_from_dir(pdf_dir, pkl_path)
    print(f"Built DB with {len(db)} samples; saved to {pkl_path}")


def cli_mutate_file(infile: str, outfile: str, times: int = 1):
    """
    Quick test: mutate a PDF file deterministically using its own bytes as seed.
    """
    with open(infile, "rb") as fh:
        data = fh.read()
    if len(data) <= HEADER_SIZE:
        data = (b"\x00" * HEADER_SIZE) + data
    else:
        data = b"\x00\x00\x00\x00" + data

    for i in range(times):
        mutated = fuzz(bytearray(data), None, 10_000_000)
        data = bytes(mutated)
        # with open(f"{outfile}.{i}", "wb") as fh:
        #     fh.write(data)
    with open(outfile, "wb") as fh:
        fh.write(data)
    # print(f"Wrote mutated output to {outfile}")

# Needed for libfuzzer
def custom_mutator(buf: bytearray, add_buf, max_size: int, callback=None) -> bytearray:
    """
    Python entrypoint for LLVMFuzzerCustomMutator.
    Mirrors the AFL++-style fuzz(buf, add_buf, max_size) signature.

    buf: current input as bytes/bytearray
    add_buf: optional secondary buffer (may be None)
    max_size: maximum allowed output size
    """

    # Make sure the mutator is initialized
    if not _initialized:
        init(0)

    # Just delegate to the main fuzz() implementation
    try:
        mutated = fuzz(buf, add_buf, max_size)
        fh = open("mutated.pdf", "wb")
        fh.write(mutated)
        fh.close()
        return mutated # fuzz(buf, add_buf, max_size)
    except Exception as e:
        # Log the error as well, so you know if something went wrong
        try:
            with open("custom_mutator.log", "a") as log:
                log.write(f"custom_mutator exception: {e}\n")
        except Exception:
            pass
        # On error, return the original buffer (safe fallback)
        return buf

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Mutator maintenance / testing")
    ap.add_argument("--build-db", action="store_true", help="Build resources.pkl from MUTATOR_PDF_DIR")
    ap.add_argument("--pdf-dir", default=str(DEFAULT_PDF_DIR))
    ap.add_argument("--pkl-path", default=str(DEFAULT_PKL_PATH))
    ap.add_argument("--mutate", nargs=2, metavar=("IN", "OUT"), help="Mutate IN -> OUT (single pass)")
    ap.add_argument("--mutate-iter", nargs=3, metavar=("IN", "OUT", "N"), help="Mutate IN repeatedly N times")
    # ap.add_argument("--run-until", nargs=2, metavar=("IN", "OUT"), help="Run until the specified point in the code...") # Do the stuff..
    ap.add_argument("--stress-test", nargs=1, metavar=("COUNT"), help="Stress test...")
    args = ap.parse_args()

    if args.build_db:
        cli_build_db(args.pdf_dir, args.pkl_path)
        sys.exit(0)

    if args.mutate:
        infile, outfile = args.mutate
        init(0)
        try:
            cli_mutate_file(infile, outfile, times=1)
        except Exception as e:
            print("Mutation error: " + str(e))
            traceback.print_exc()
        sys.exit(0)

    if args.mutate_iter:
        infile, outfile, n = args.mutate_iter
        n = int(n)
        init(0)
        try:
            # while not_reached:
            cli_mutate_file(infile, outfile, times=n)
        except Exception as e:
            print("Mutation error: " + str(e))
            traceback.print_exc()
        sys.exit(0)

    if args.stress_test:
        n = args.stress_test # Get count...
        n = int(n[0]) # Get the actual integer...
        init(0)
        cands = get_candidate_pdf("./testset/")
        for _ in range(n):
            infile = random.choice(cands)
            outfile = "output.pdf"
            cli_mutate_file(infile, outfile, times=10) # Just mutate some times...

    # print("No action specified. This script is the AFL++ custom mutator module.")
