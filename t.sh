#!/bin/sh

python3 mutator.py ./actual_shader.glsl crash_test_output.txt --iters 5 ; ./mutated_to_source.sh
