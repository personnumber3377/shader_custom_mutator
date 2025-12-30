
import os
import sys
import random

from test_helpers import * # For the utilities...

TEST_DIR = "tests/"
DEBUG_ENV = True

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
		# Disabled for now...
		# tree = shader_mutator.mutate_translation_unit(tree, rng) # Actually mutate the tree.
		unparsed_src = shader_unparser.unparse_tu(tree)
		print(unparsed_src)
	return

def roundtrip_one(filename: str): # Run the thing...
	print("Running "+str(filename))
	fh = open(filename, "rb")
	source = fh.read() # Read the source code...
	source = strip_header_and_null(source, header_len=128) # Cut off the shit...
	fh.close()

	ok_orig, err = run_external_checker(source, 128) # Run the checker for this source code...
	if not ok_orig: # Ignore the files which we can not parse...
		print("filename "+str(filename)+" errored with: "+str(err))
		# return

	# Roundtrip...
	source = source.decode("ascii")
	tree = shader_parser.parse_to_tree(source)
	unparsed_src = shader_unparser.unparse_tu(tree)

	# Same?
	unparsed_src = unparsed_src.encode("ascii")
	ok_new, err_new = run_external_checker(unparsed_src, 128)

	if ok_orig != ok_new:
		print("Filename: "+str(filename)+" failed roundtrip test!!!")
		print("Original source code: "+str(source))
		print("\n\n\n")
		print("New source code: "+str(unparsed_src.decode("ascii")))
		print("Previous errors: "+str(err))
		print("New errors: "+str(err_new))
		assert False
	else:
		print("Filename: "+str(filename)+" passed with orig: "+str(ok_orig)+" and new: "+str(ok_new))
	return

def run_roundtrip_tests(directory: str) -> None: # Run the roundtrip tests...
	# Do the stuff...
	if directory[-1] != "/": # Append the slash here...
		directory += "/"
	test_files = os.listdir(directory) # List all of the things...
	print(test_files)
	for f in test_files:
		roundtrip_one(directory+f) # Run one roundtrip thing...
	return

def run_one(filename: str): # Run the thing...

	fh = open(filename, "rb")
	source = fh.read() # Read the source code...
	source = strip_header_and_null(source, header_len=128) # Cut off the shit...
	fh.close()

	ok, err = run_external_checker(source, 128) # Run the checker for this source code...
	if not ok: # Error? Try to parse as vertex shader...
		# print("filename "+str(filename)+" errored with: "+str(err))
		ok, err = run_external_checker(source, 128, as_vertex=True) # Try again with a vertex thing...
		if not ok:
			print("filename "+str(filename)+ " errored as vertex shader and fragment... Error: "+str(err))
			if DEBUG_ENV:
				# print("Removing this filename here: "+str(filename))
				os.system("rm "+str(filename))
				# print("Removing this filename here: "+str(filename))
				# Also delete the final fuzz input file thing...
				new_filename = filename.replace("webgl_cleaned", "webgl_fuzz_inputs").replace(".vert", ".bin").replace(".frag", ".bin").replace(".comp", ".bin")
				print("Removing this here: "+str(new_filename))
				os.system("rm "+str(new_filename))
		# assert False
	else:
		print("filename "+str(filename)+ " passed...")
	return

def run_parse_check(directory: str) -> None: # Errors out if there are any errors in any file inside the specified directory...
	# Do the stuff...
	if directory[-1] != "/": # Append the slash here...
		directory += "/"
	test_files = os.listdir(directory) # List all of the things...
	print(test_files)
	for f in test_files:
		run_one(directory+f) # Run one roundtrip thing...
	return
	# return

if __name__=="__main__":
	fn = None
	if len(sys.argv) == 2: # Check for special flags...
		if "--run-small" in sys.argv: # Run the small testset...
			run_parse_tests(only_one=None)
			exit(0)
	if len(sys.argv) == 3: # We need the directory and the thing...
		if "--run-roundtrip" == sys.argv[1]:
			run_roundtrip_tests(sys.argv[2]) # Pass the directory name as filename...
			exit(0)
		elif "--run-check" == sys.argv[1]:
			run_parse_check(sys.argv[2])
			exit(0)
	if len(sys.argv) >= 2:
		fn = sys.argv[1]
	run_parse_tests(only_one=fn)
	exit(0)
