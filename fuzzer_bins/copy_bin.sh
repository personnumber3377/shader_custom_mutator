#!/bin/sh

rm angle_translator_fuzzer.zip

cp /home/oof/chromiumstuff/source/src/out/canvasfuzz/angle_translator_fuzzer .

zip -r angle_translator_fuzzer.zip angle_translator_fuzzer

rm angle_translator_fuzzer || true

# Now commit changes...
ca
