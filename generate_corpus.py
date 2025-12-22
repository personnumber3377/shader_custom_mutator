
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import random
import hashlib
from pathlib import Path

import shader_parser
import shader_mutator
import shader_unparser

HEADER_SIZE = 128
MAX_SHADER_SIZE = 64 * 1024  # keep sane


def mutate_once(buf: bytes, rng: random.Random) -> bytes | None:
    """
    Perform ONE structural mutation.
    Returns mutated buffer or None on failure.
    """
    if len(buf) <= HEADER_SIZE:
        return None

    header = buf[:HEADER_SIZE]
    body = buf[HEADER_SIZE:]

    try:
        src = body.rstrip(b"\x00").decode("utf-8", errors="ignore")
        tree = shader_parser.parse_to_tree(src)
        mutated = shader_mutator.mutate_translation_unit(tree, rng)
        new_src = shader_unparser.unparse_tu(mutated)

        out = header + new_src.encode("utf-8") + b"\x00"
        return out[:MAX_SHADER_SIZE]
    except Exception:
        return None


def expand_one_input(
    path: Path,
    out_dir: Path,
    min_mut: int,
    max_mut: int,
    seed: int,
):
    data = path.read_bytes()
    rng = random.Random(seed)

    count = rng.randint(min_mut, max_mut)
    for i in range(count):
        mutated = mutate_once(data, rng)
        if not mutated:
            continue

        h = hashlib.sha1(mutated).hexdigest()
        out_path = out_dir / f"{path.stem}_{h}.bin"
        out_path.write_bytes(mutated)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <in_corpus> <out_corpus>")
        sys.exit(1)

    in_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])

    out_dir.mkdir(parents=True, exist_ok=True)

    seeds = list(in_dir.iterdir())
    print(f"[+] Loaded {len(seeds)} seed inputs")

    for idx, p in enumerate(seeds):
        if not p.is_file():
            continue

        seed = hash(p.name) ^ idx
        expand_one_input(
            path=p,
            out_dir=out_dir,
            min_mut=5,
            max_mut=50,
            seed=seed,
        )

        if idx % 10 == 0:
            print(f"[+] Processed {idx}/{len(seeds)}")

    print("[+] Corpus expansion complete")


if __name__ == "__main__":
    main()
