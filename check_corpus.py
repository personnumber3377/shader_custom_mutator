#!/usr/bin/env python3
import os
import struct
import subprocess
import tempfile
import sys
import traceback
from test_helpers import *

# ---- Main driver ----

def check_directory(dirpath: str):
    total = 0
    failures = 0
    printed = 0

    for name in sorted(os.listdir(dirpath)):
        path = os.path.join(dirpath, name)
        if not os.path.isfile(path):
            continue

        try:
            data = open(path, "rb").read()
            shader_type, spec, output = parse_header(data)
            shader_src = strip_header_and_null(data)

            if not shader_src:
                continue

            ok, msg = run_checker(shader_src, shader_type, spec, output, original_filename=name)
            total += 1

            if not ok:
                failures += 1
                if printed < PRINT_LIMIT:
                    printed += 1
                    print("=" * 60)
                    print(f"FAIL: {name}")
                    print(f"  type={hex(shader_type)} spec={spec} output={output}")
                    print(msg)
                    # os.system("cp ")

        except Exception as e:
            failures += 1
            if printed < PRINT_LIMIT:
                printed += 1
                print("=" * 60)
                print(f"EXCEPTION: {name}")
                traceback.print_exc()

    print("\n==== SUMMARY ====")
    print(f"Total checked : {total}")
    print(f"Failures      : {failures}")
    print(f"Success       : {total - failures}")

# ---- Entry point ----

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <angle-corpus-dir>")
        sys.exit(1)

    check_directory(sys.argv[1])