
import os

TEST_DIR = "./tests/"

import shader_parser # The parser...
import shader_unparser

def run_parse_tests(): # Run the parse tests..
	test_files = os.listdir(TEST_DIR)
	for fn in test_files:
		complete_fn = TEST_DIR + fn # Add the directory name too...
		fh = open(complete_fn, "r")
		shader_src = fh.read()
		fh.close()
		# Now try to parse into tree and then unparse...
		tree = shader_parser.parse_to_tree(shader_src)
		unparsed_src = shader_unparser.unparse_tu(tree)
		print(unparsed_src)
	return

if __name__=="__main__":
	run_parse_tests()
	exit(0)