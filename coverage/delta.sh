#!/bin/sh

export PATH=/home/oof/llvminstall/LLVM-21.1.0-Linux-X64/bin:$PATH

llvm-profdata merge \
  -subtract \
  -o delta.profdata \
  angle_good_corpus.profdata \
  single_seed.profdata

# Then make html visualization

llvm-cov show \
  ./angle_translator_fuzzer \
  -instr-profile=delta.profdata \
  -format=html \
  -output-dir=coverage_delta_html \
  -Xdemangler=c++filt
