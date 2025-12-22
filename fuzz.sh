#!/bin/sh

ASAN_OPTIONS=alloc_dealloc_mismatch=0:allocator_may_return_null=1:halt_on_error=1:abort_on_error=1 SLOT_INDEX=1 LIBFUZZER_PYTHON_MODULE=daemon PYTHONPATH=. ./pdfium_fuzzer -fork=1 -ignore_crashes=1 -dict=angle_translator_fuzzer.dict -timeout=1 -rss_limit_mb=2048 ./translator_corpus/

