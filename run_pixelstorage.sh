#!/bin/sh

python3 test.py --text-to-bin tests_complex/local_pixel_storage.glsl ; mv tests_complex/local_pixel_storage.glsl.bin tests_complex_binary/local_pixel_storage.glsl.bin ; gdb --args /home/oof/chromiumstuff/source/src/out/canvasfuzz/angle_translator_fuzzer ./tests_complex_binary/local_pixel_storage.glsl.bin
