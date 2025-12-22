
import os
import sys
import random

TEST_DIR = "tests/"

import shader_parser # The parser...
import shader_mutator
import shader_unparser

def run_parse_tests(only_one=None): # Run the parse tests..
	if only_one == None:
		test_files = os.listdir(TEST_DIR)
	else:
		if only_one.startswith(TEST_DIR): # Cut off the thing...
			only_one = only_one[len(TEST_DIR):]
		test_files = [only_one]

	for fn in test_files:
		complete_fn = TEST_DIR + fn # Add the directory name too...
		print("Running "+str(complete_fn)+" ...")
		fh = open(complete_fn, "r")
		shader_src = fh.read()
		fh.close()
		# Now try to parse into tree and then unparse...
		tree = shader_parser.parse_to_tree(shader_src)
		rng = random.Random(random.randrange(100000000))
		tree = shader_mutator.mutate_translation_unit(tree, rng) # Actually mutate the tree
		unparsed_src = shader_unparser.unparse_tu(tree)
		print(unparsed_src)
	return

if __name__=="__main__":
	fn = None
	if len(sys.argv) >= 2:
		fn = sys.argv[1]
	run_parse_tests(only_one=fn)
	exit(0)