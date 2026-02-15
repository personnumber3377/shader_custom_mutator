#!/bin/sh


# angle_no_assert

cp /home/oof/chromiumstuff/source/src/out/angle_no_assert/webgsl_translator_fuzzer ./angle_webgsl_translator

# ./dawn_angle_fuzzer

cp /home/oof/dawn/out/fuzzing/dawn_angle_fuzzer ./

zip -r dawn_angle_fuzzer.zip dawn_angle_fuzzer

rm dawn_angle_fuzzer
