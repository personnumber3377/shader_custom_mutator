#!/bin/sh

rm angle_translator_fuzzer.zip

cp /home/oof/chromiumstuff/source/src/out/canvasfuzz/angle_translator_fuzzer .

zip -r angle_translator_fuzzer.zip angle_translator_fuzzer

rm angle_translator_fuzzer || true



rm angle_translator_fuzzer_no_assert.zip

cp /home/oof/chromiumstuff/source/src/out/angle_no_assert/angle_translator_fuzzer ./angle_translator_fuzzer_no_assert

zip -r angle_translator_fuzzer_no_assert.zip angle_translator_fuzzer_no_assert

rm angle_translator_fuzzer_no_assert || true


# Now commit changes...
ca








