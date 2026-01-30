#!/usr/bin/env python3
import os
import subprocess
import shutil

# -----------------------
# CONFIG
# -----------------------

FUZZER_ASSERT = "./angle_translator_fuzzer_assert"
FUZZER_NOASSERT = "./angle_translator_fuzzer_noassert"

INPUT_DIR = "./initial_crashes"
OUTPUT_DIR = "./clean_noassert_seeds"

TIMEOUT = 10

# -----------------------
# RUNNER
# -----------------------

def run(binary: str, path: str) -> bool:
    """
    Returns True if the binary crashes on input.
    """
    try:
        p = subprocess.run(
            [binary, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT,
        )
        return p.returncode != 0
    except subprocess.TimeoutExpired:
        # Treat timeouts as crashes (conservative)
        return True

# -----------------------
# MAIN
# -----------------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = 0
    kept = 0

    for fn in sorted(os.listdir(INPUT_DIR)):
        if not fn.startswith("crash-"):
            continue

        total += 1
        path = os.path.join(INPUT_DIR, fn)

        print(f"[+] Testing {fn}")

        crashes_assert = run(FUZZER_ASSERT, path)
        crashes_noassert = run(FUZZER_NOASSERT, path)

        if crashes_assert:
            print("    [-] Crashes assert build → discard")
            continue

        if crashes_noassert:
            print("    [-] Crashes no-assert → discard")
            continue

        shutil.copy(path, os.path.join(OUTPUT_DIR, fn))
        kept += 1
        print("    [✓] Kept (kept only crashes that crash assert build but not the no assert build)")

    print(f"\nDone. Kept {kept}/{total} inputs.")

if __name__ == "__main__":
    main()