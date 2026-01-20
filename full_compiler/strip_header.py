#!/usr/bin/env python3

import os
import shutil
import sys

SKIP_PREFIX = 128
SKIP_SUFFIX = 1


def copy_and_trim_file(src_path: str, dst_path: str):
    with open(src_path, "rb") as f:
        data = f.read()

    # If file is too small, write empty file
    if len(data) <= SKIP_PREFIX + SKIP_SUFFIX:
        trimmed = b""
    else:
        trimmed = data[SKIP_PREFIX:-SKIP_SUFFIX]

    with open(dst_path, "wb") as f:
        f.write(trimmed)


def copy_directory(src_dir: str, dst_dir: str):
    for root, dirs, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)
        dst_root = dst_dir if rel_root == "." else os.path.join(dst_dir, rel_root)

        os.makedirs(dst_root, exist_ok=True)

        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_root, file)

            copy_and_trim_file(src_path, dst_path)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <destination_dir>")
        sys.exit(1)

    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]

    if not os.path.isdir(src_dir):
        print(f"Error: source directory '{src_dir}' does not exist")
        sys.exit(1)

    if os.path.exists(dst_dir):
        print(f"Error: destination directory '{dst_dir}' already exists")
        sys.exit(1)

    copy_directory(src_dir, dst_dir)
    print("Done.")


if __name__ == "__main__":
    main()

