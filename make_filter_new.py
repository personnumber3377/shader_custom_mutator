import sys
import re

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <gtest_list_tests_output>")
    sys.exit(1)

suites = []

with open(sys.argv[1], "r", errors="ignore") as f:
    for line in f:
        line = line.rstrip()

        # Match lines like:
        #   UniformTest.
        #   BasicUniformUsageTest.
        #   AdvancedBlendTestES32.
        #
        # Exclude indented lines and noise.
        if (
            line
            and not line.startswith(" ")
            and line.endswith(".")
            and "/" not in line
            and not line.startswith("Skipping ")
            and not line.startswith("Active ")
            and not line.startswith("Optimus")
            and not line.startswith("AMD ")
            and not line.startswith("Mac ")
        ):
            suite = line[:-1]  # strip trailing dot
            suites.append(suite)

# Deduplicate + stable sort
suites = sorted(set(suites))

# Build gtest filter
patterns = [f"{s}.*" for s in suites]
filter_arg = "--gtest_filter=" + ":".join(patterns)

print(filter_arg)
print()
print(f"# {len(suites)} test suites included")