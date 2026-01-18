#!/bin/sh

set -e

python3 test.py --roundtrip ./tests_complex/layout_case.glsl
# python3 test.py --mutation-bench ./mutation_tests/scalar_to_array_functions/


