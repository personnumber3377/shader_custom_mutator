#!/usr/bin/env python3

import os
import subprocess
import sys
from typing import List

CHECKER_PATH = "./angle_shader_checker"  # <-- change if needed
TIMEOUT = 5.0
GOOD_CORPUS_DIR = "good/"

def check_file(path: str) -> tuple[bool, str]:
    """
    Runs the checker on a single file.
    Returns (ok, stderr_output).
    ok == True  -> "SUCCESS" found in stderr
    ok == False -> otherwise
    """
    try:
        proc = subprocess.run(
            [CHECKER_PATH, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"

    stderr = proc.stderr or ""
    ok = "SUCCESS" in stderr
    return ok, stderr.strip()


def scan_directory(directory: str) -> None:
    if not os.path.isdir(directory):
        print(f"[!] Not a directory: {directory}")
        sys.exit(1)

    files: List[str] = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    total = len(files)
    ok_count = 0
    fail_count = 0

    print(f"[*] Checking {total} files in {directory}\n")

    for i, path in enumerate(files, 1):
        ok, stderr = check_file(path)

        if ok:
            # Copy good files to the good corpus directory.
            os.system("cp "+str(path)+" ./"+str(GOOD_CORPUS_DIR))
            ok_count += 1
        else:
            fail_count += 1
            print(f"[FAIL] {path}")
            print("------- stderr -------")
            print(stderr)
            print("----------------------\n")

        if i % 100 == 0:
            print(f"[*] Progress: {i}/{total}")

    print("\n========== SUMMARY ==========")
    print(f"Total files : {total}")
    print(f"SUCCESS     : {ok_count}")
    print(f"FAILURE     : {fail_count}")
    print("=============================\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)

    scan_directory(sys.argv[1])