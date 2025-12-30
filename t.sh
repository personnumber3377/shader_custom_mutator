#!/bin/sh

python3 mutator.py /home/oof/webgl_fuzz_inputs/ crash_test_output.txt --iters 5 ; ./mutated_to_source.sh
