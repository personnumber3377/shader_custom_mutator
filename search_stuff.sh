#/bin/sh

# "applyLogicOp" signifies the thing...
grep -rl "applyLogicOp" /home/oof/current_corpus/corpus/angle_fuzzing_custom/preprocced/ | xargs cp -t after_preproc_tests/

