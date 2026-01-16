
rm /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/* || true # Delete the old stuff???

mkdir -p /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw

# Remember to add /home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin to path!!!

i=0
for f in min/*; do
  echo "[*] Running $f"
  i=$((i+1))
  LLVM_PROFILE_FILE="/home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/run_$i.profraw" \
    /home/oof/chromiumstuff/source/src/out/pdfium_cov/profraw/angle_translator_fuzzer "$f" \
    -timeout=5 || true
done
