#!/bin/sh

# python3 preproc.py corpus_input/ corpus_cleaned/ corpus_fuzz_inputs/

rm ~/shader_sources_cleaned/*
rm ~/shader_sources_fuzz_inputs/*

python3 preproc.py ~/shader_sources/ ~/shader_sources_cleaned/ ~/shader_sources_fuzz_inputs/
