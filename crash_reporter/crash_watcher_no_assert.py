#!/usr/bin/env python3
import os
import re
import time
import hashlib
import subprocess

# -----------------------
# CONFIG
# -----------------------

FUZZER = "./angle_translator_fuzzer_no_assert"
SYMBOLIZER = "/usr/bin/llvm-symbolizer"

SCAN_INTERVAL = 10

SEEN_DB = "seen_noassert_crashes.txt"
BANLIST = "ban_signatures.txt"

# -----------------------
# REGEX / CLASSIFICATION
# -----------------------

ADDR_RE = re.compile(r"0x[0-9a-fA-F]+")
NEAR_NULL_RE = re.compile(r"0x0+$|0x[0-9a-fA-F]{1,3}$")

INTERESTING_PATTERNS = [
    "heap-buffer-overflow",
    "heap-use-after-free",
    "stack-buffer-overflow",
    "global-buffer-overflow",
    "AddressSanitizer",
    "SEGV",
    "SIGABRT",
    "wild pointer",
]

# -----------------------
# UTILS
# -----------------------

def load_set(path):
    if not os.path.exists(path):
        return set()
    return set(open(path).read().splitlines())

def save_set(path, s):
    with open(path, "w") as f:
        for x in sorted(s):
            f.write(x + "\n")

def normalize_stack(stderr: str) -> str:
    frames = []
    for line in stderr.splitlines():
        if line.strip().startswith("#"):
            line = ADDR_RE.sub("ADDR", line)
            frames.append(line)
        if len(frames) >= 6:
            break
    return "\n".join(frames)

def fingerprint(stderr: str) -> str:
    return hashlib.sha1(normalize_stack(stderr).encode()).hexdigest()

def is_near_null(stderr: str) -> bool:
    for line in stderr.splitlines():
        if "address" in line.lower():
            m = re.search(r"0x[0-9a-fA-F]+", line)
            if m and NEAR_NULL_RE.match(m.group(0)):
                return True
    return False

def is_interesting(stderr: str) -> bool:
    if "Assertion" in stderr:
        return False
    if is_near_null(stderr):
        return False
    return any(p in stderr for p in INTERESTING_PATTERNS)

def banned(stderr: str, banlist) -> bool:
    return any(b in stderr for b in banlist)

# -----------------------
# RUNNER
# -----------------------

def run_fuzzer(path: str) -> str:
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = f"external_symbolizer_path={SYMBOLIZER}"

    p = subprocess.run(
        [FUZZER, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=10,
    )
    return p.stderr.decode(errors="ignore")

# -----------------------
# MAIN LOOP
# -----------------------

def main():
    print("[*] Starting NO-ASSERT crash watcher")

    seen = load_set(SEEN_DB)
    banlist = load_set(BANLIST)

    while True:
        time.sleep(SCAN_INTERVAL)

        for fn in sorted(os.listdir(".")):
            if not fn.startswith("crash-"):
                continue

            print(f"[+] Testing {fn}")

            try:
                stderr = run_fuzzer(fn)
            except Exception as e:
                print(f"[!] Failed {fn}: {e}")
                continue

            if not is_interesting(stderr):
                print("[-] Not interesting")
                continue

            if banned(stderr, banlist):
                print("[-] Banned")
                continue

            sig = fingerprint(stderr)

            if sig in seen:
                print("[-] Duplicate")
                continue

            seen.add(sig)
            save_set(SEEN_DB, seen)

            print("[🔥] NEW REAL CRASH FOUND")
            print(normalize_stack(stderr))
            print("--------------------------------")

if __name__ == "__main__":
    main()