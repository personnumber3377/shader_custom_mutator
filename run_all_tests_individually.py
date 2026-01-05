#!/usr/bin/env python3
import subprocess
import signal
import time
import sys
from pathlib import Path

ANGLE_BIN = "./angle_end2end_tests"
LIST_FILE = "tests.txt"

TIMEOUT_SECONDS = 10 * 60  # 10 minutes per group
LOG_DIR = Path("group_logs")
LOG_DIR.mkdir(exist_ok=True)

def parse_test_groups(list_file: Path):
    """
    Parses gtest_list_tests output and returns a sorted list of test suite names.
    """
    groups = []
    with list_file.open() as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            # Test suite lines end with '.'
            if line.endswith(".") and not line.startswith(" "):
                groups.append(line[:-1])
    return sorted(set(groups))


def run_group(group: str):
    log_path = LOG_DIR / f"{group}.log"
    filter_arg = f"{group}.*"

    print(f"\n=== Running group: {group} ===")
    print(f"    Filter: {filter_arg}")
    print(f"    Log: {log_path}")

    with log_path.open("w") as log:
        try:
            proc = subprocess.Popen(
                [ANGLE_BIN, f"--gtest_filter={filter_arg}"],
                stdout=log,
                stderr=subprocess.STDOUT,
                preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL),
            )

            start = time.time()
            while True:
                if proc.poll() is not None:
                    break
                if time.time() - start > TIMEOUT_SECONDS:
                    print(f"    ⏰ Timeout after {TIMEOUT_SECONDS}s, killing group {group}")
                    proc.kill()
                    log.write("\n[TIMEOUT]\n")
                    return "timeout"
                time.sleep(1)

            if proc.returncode == 0:
                print(f"    ✅ Finished OK")
                return "ok"
            else:
                print(f"    💥 Crashed / non-zero exit ({proc.returncode})")
                return "crash"

        except Exception as e:
            print(f"    ❌ Exception while running {group}: {e}")
            log.write(f"\n[EXCEPTION] {e}\n")
            return "exception"


def main():
    list_file = Path(LIST_FILE)
    if not list_file.exists():
        print(f"Missing {LIST_FILE}. Run:")
        print(f"  ./angle_end2end_tests --gtest_list_tests > {LIST_FILE}")
        sys.exit(1)

    groups = parse_test_groups(list_file)
    print(f"Found {len(groups)} test groups")

    results = {
        "ok": [],
        "crash": [],
        "timeout": [],
        "exception": [],
    }

    for group in groups:
        status = run_group(group)
        results[status].append(group)

    print("\n=== SUMMARY ===")
    for k, v in results.items():
        print(f"{k:10}: {len(v)}")

    # Save summary for resume/debug
    summary_path = LOG_DIR / "summary.txt"
    with summary_path.open("w") as f:
        for k, v in results.items():
            f.write(f"{k}:\n")
            for g in v:
                f.write(f"  {g}\n")
            f.write("\n")

    print(f"\nSummary written to {summary_path}")


if __name__ == "__main__":
    main()