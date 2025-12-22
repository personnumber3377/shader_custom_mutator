#!/bin/sh

python3 mutator.py crash_test/crashing_input.bin crash_test_output.txt --iters 1 ; ./mutated_to_source.sh
