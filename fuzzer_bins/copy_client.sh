#!/bin/sh

cp ../shader_custom_mutator/fuzzer_bins/angle_translator_fuzzer.zip .
cp ../shader_custom_mutator/fuzzer_bins/angle_translator_fuzzer_no_assert.zip .

unzip -o angle_translator_fuzzer.zip
unzip -o angle_translator_fuzzer_no_assert.zip
