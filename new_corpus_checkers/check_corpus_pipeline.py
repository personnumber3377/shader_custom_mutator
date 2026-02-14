#!/usr/bin/env python3
import subprocess
import sys
import os
from collections import defaultdict

BINARY = "./dawn_angle_fuzzer"

def run_file(path):
    try:
        result = subprocess.run(
            [BINARY, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

    if result.returncode < 0:
        return "CRASH"

    output = result.stderr.decode()
    # output = result.stdout.decode()

    print(output)

    for line in reversed(output.strip().splitlines()):
        if line.startswith("ERROR:") or line == "VALID":
            return line.replace("ERROR: ", "")

    return "UNKNOWN"

def main():
    if len(sys.argv) != 2:
        print("Usage: check_pipeline_corpus.py <file_or_dir>")
        return

    path = sys.argv[1]
    files = []

    if os.path.isdir(path):
        for root, _, names in os.walk(path):
            for n in names:
                files.append(os.path.join(root, n))
    else:
        files = [path]

    stats = defaultdict(int)

    for f in files:
        result = run_file(f)
        stats[result] += 1
        print(f"{f}: {result}")

    print("\n==== Statistics ====")
    total = sum(stats.values())
    print(f"Total files: {total}")
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()