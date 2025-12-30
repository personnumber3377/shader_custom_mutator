#!/bin/sh

./preproc_webgl.sh
python3 test_mutator.py --run-check ~/webgl_cleaned/ > out2.txt
