
# Add the utils to path...

export PATH=/home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin:$PATH

# Now start generating the actual coverage...

rm /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/* || true # Delete the old stuff???

mkdir -p /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw

# Remember to add /home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin to path!!!

# /home/oof/minned

# was originally /home/oof/chromiumstuff/source/src/out/pdfium_cov/generated_files/

i=0
for f in /home/oof/minned/*; do
  echo "[*] Running $f"
  i=$((i+1))
  LLVM_PROFILE_FILE="/home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/run_$i.profraw" \
    /home/oof/chromiumstuff/source/src/out/pdfium_cov/angle_translator_fuzzer "$f" \
    -timeout=5 || true
done


# Now merge all of the stuff...

llvm-profdata merge -sparse /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/*.profraw -o /home/oof/chromiumstuff/source/src/out/pdfium_cov/angle.profdata

# Delete old output directory...

rm -r /home/oof/chromiumstuff/source/src/out/pdfium_cov/coverage_html/ || true


# We have to do this because the llvm-cov requires that we are in the same directory as the binary I think since it looks up ../../third_party/ ... and so on :D
cd /home/oof/chromiumstuff/source/src/out/pdfium_cov/

llvm-cov show  /home/oof/chromiumstuff/source/src/out/pdfium_cov/angle_translator_fuzzer \
  -instr-profile=/home/oof/chromiumstuff/source/src/out/pdfium_cov/angle.profdata \
  -format=html \
  -output-dir=/home/oof/chromiumstuff/source/src/out/pdfium_cov/coverage_html \
  -Xdemangler=c++filt

# Open the file...

/usr/bin/google-chrome /home/oof/chromiumstuff/source/src/out/pdfium_cov/coverage_html/index.html

# Change directory back...
cd /home/oof/shader_custom_mutator/coverage || true


