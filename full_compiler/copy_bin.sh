#!/bin/sh

rm angle_shader_fuzzer.zip

cp /home/oof/chromiumstuff/source/src/out/canvasfuzz/angle_shader_fuzzer .

zip -r angle_shader_fuzzer.zip angle_shader_fuzzer

rm angle_shader_fuzzer || true

# Now commit changes...
ca
