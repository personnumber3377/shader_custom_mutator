
set -e

python3 test.py --roundtrip ./tests_complex/function_returns_array.glsl

python3 test.py --mutation-bench ./mutation_tests/scalar_to_array_functions/
