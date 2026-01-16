
# Add the utils to path...

export PATH=/home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin:$PATH

# Copy the newest custom mutator stuff to the fuzzing directory...

cp /home/oof/shader_custom_mutator/*.py /home/oof/chromiumstuff/source/src/out/canvasfuzz/


# First run the fuzzer with the newest custom mutator stuff...

# Delete old input file directory

rm -r /home/oof/chromiumstuff/source/src/out/canvasfuzz/generated_files/ || true

mkdir -p /home/oof/chromiumstuff/source/src/out/canvasfuzz/generated_files/ || true

# Copy the initial corpus to the thing...

cp testing_corpus/* /home/oof/chromiumstuff/source/src/out/canvasfuzz/generated_files/

# Now run the fuzzer

#  -dict=angle_translator_fuzzer.dict
# -seed=1 is so that the output is deterministic...
# -runs=10000 so that it always runs 10k times...

ASAN_OPTIONS=external_symbolizer_path=/usr/bin/llvm-symbolizer:alloc_dealloc_mismatch=0:allocator_may_return_null=1:halt_on_error=1:abort_on_error=1 SLOT_INDEX=1 FUZZ_ONLY_CUSTOM=1 LIBFUZZER_PYTHON_MODULE=mutator PYTHONPATH=/home/oof/chromiumstuff/source/src/out/canvasfuzz/ /home/oof/chromiumstuff/source/src/out/canvasfuzz/angle_translator_fuzzer -seed=1 -fork=1 -runs=10000 -ignore_crashes=1 -max_len=10000 -only_ascii=0 -timeout=1 -cross_over=0 -rss_limit_mb=2048 /home/oof/chromiumstuff/source/src/out/canvasfuzz/generated_files/

# Now make the coverage directory...

# Delete old...
rm -r /home/oof/chromiumstuff/source/src/out/pdfium_cov/generated_files/ || true
# Make new...
mkdir -p /home/oof/chromiumstuff/source/src/out/pdfium_cov/generated_files/ || true

# Now copy the corpus files...

cp /home/oof/chromiumstuff/source/src/out/canvasfuzz/generated_files/* /home/oof/chromiumstuff/source/src/out/pdfium_cov/generated_files/





# Now start generating the actual coverage...

rm /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/* || true # Delete the old stuff???

mkdir -p /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw

# Remember to add /home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin to path!!!

i=0
for f in /home/oof/chromiumstuff/source/src/out/pdfium_cov/generated_files/*; do
  echo "[*] Running $f"
  i=$((i+1))
  LLVM_PROFILE_FILE="/home/oof/chromiumstuff/source/src/out/pdfium_cov/run_$i.profraw" \
    /home/oof/chromiumstuff/source/src/out/pdfium_cov/angle_translator_fuzzer "$f" \
    -timeout=5 || true
done


# Now merge all of the stuff...

llvm-profdata merge -sparse /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/*.profraw -o /home/oof/chromiumstuff/source/src/out/pdfium_cov/angle.profdata

# Delete old output directory...

rm -r /home/oof/chromiumstuff/source/src/out/pdfium_cov/coverage_html/ || true

llvm-cov show ./angle_translator_fuzzer \
  -instr-profile=/home/oof/chromiumstuff/source/src/out/pdfium_cov/angle.profdata \
  -format=html \
  -output-dir=/home/oof/chromiumstuff/source/src/out/pdfium_cov/coverage_html \
  -Xdemangler=c++filt


