
import os
import sys
import random

from test_helpers import * # For the utilities...

TEST_DIR = "tests/"
DEBUG_ENV = True

import shader_parser # The parser...
import shader_mutator
import shader_unparser
import mutator



def normalize_input(data: bytes) -> bytes:
    """
    Ensure buffer has header and no embedded nulls in shader body.
    """
    # If header is missing, prepend it
    if b"\x00" not in data[:HEADER_SIZE]:
        # return data
        data = b"\x00" * HEADER_SIZE + data

    # Strip accidental nulls in shader body
    body = data[HEADER_SIZE:]
    body = body.replace(b"\x00", b"")

    return data[:HEADER_SIZE] + body + b"\x00"


def is_valid_shader(buf: bytes) -> bool:
    """
    Check fragment first, then vertex.
    """
    ok, err1 = run_external_checker(buf, HEADER_SIZE)
    if ok:
        return True, err1
    ok, err2 = run_external_checker(buf, HEADER_SIZE, as_vertex=True)
    # Count errors and return the one with the least errors...
    if err1.count("ERROR") < err2.count("ERROR"):
        return ok, err1 # Return the one that has less errors...
    else:
        return ok, err2


def benchmark_mutation_success(
    input_dir: str,
    trials: int = 100,
    seed: int | None = None,
    dump_failures: bool = False,
    dump_dir: str = "mutation_failures",
):
    """
    Randomly samples shaders, mutates once, checks validity.
    Returns success ratio.
    """

    if seed is not None:
        random.seed(seed)
        mutator.init(seed)
    files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f))
    ]

    if not files:
        raise RuntimeError("No input files found")

    if dump_failures:
        os.makedirs(dump_dir, exist_ok=True)

    total = 0
    success = 0

    for i in range(1000): # range(trials):
        rate = (success / total * 100.0) if total else 0.0
        if rate != 0.0: # Is not zero?
            print(rate)
            # break
        if i % PRINT_COUNT == 0:
            print(f"Mutations attempted: {total}")
            print(f"Valid mutations:     {success}")
            print(f"Success rate:        {rate:.2f}%")
        fn = random.choice(files)
        if ".vert" in fn:
            as_vertex = True
        else:
            as_vertex = False

        try:
            print("Processing this: "+str(fn))

            with open(fn, "rb") as f:
                dataorig = f.read()

            # dataorig = b"\x00" * 128 + dataorig + b"\x00" # Convert to fuzz format...

            data = normalize_input(dataorig)

            # Check original validity
            # print("is valid???")
            # print("data: "+str(data))
            v, err = is_valid_shader(data) # run_external_checker(data, HEADER_SIZE, as_vertex=as_vertex) # is_valid_shader(data)
            if not v:
                print(err)
                continue  # skip invalid seeds
            buf = bytearray(data)
            print("Original source code: \n"+str(dataorig.decode("ascii")))

            # Mutate exactly once
            print("Passing this here: "+str(buf))
            buf = mutator.fuzz(buf, None, 1_000_000)
            print("Mutated source code: \n"+str(buf[128:-1].decode("ascii")))
            print("As vertex? : "+str(as_vertex))
            total += 1

            v, err = is_valid_shader(buf) # run_external_checker(buf, HEADER_SIZE, as_vertex=as_vertex)

            if v:
                print("SUCCESS!")
                success += 1
            else:
                print("Errored with this here: "+str(err))
                print("="*30)
                print(buf[128:-1].decode("ascii"))
                print("="*30)
                if dump_failures:
                    out = strip_header_and_null(buf, HEADER_SIZE)
                    with open(
                        os.path.join(dump_dir, f"fail_{i}.glsl"),
                        "w",
                        encoding="utf-8",
                        errors="ignore",
                    ) as fh:
                        fh.write(out.decode("utf-8", errors="ignore"))

        except Exception:
            traceback.print_exc()
            continue

    rate = (success / total * 100.0) if total else 0.0

    print(f"Mutations attempted: {total}")
    print(f"Valid mutations:     {success}")
    print(f"Success rate:        {rate:.2f}%")

    return rate

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

PRINT_SOURCE = True

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
	try:
		tree = shader_parser.parse_to_tree(source)
		unparsed_src = shader_unparser.unparse_tu(tree)
	except Exception as e:
		# raise e # Raise exception
		print(str(e))
		# Error while parsing? Log the file and continue...
		print("Filename: "+str(filename)+ "errored... continuing anyway...")
		# raise e
		return
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
		if PRINT_SOURCE:
			print("Original source code: "+str(source))
			print("\n\n\n")
			print("New source code: "+str(unparsed_src.decode("ascii")))

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
		elif "--benchmark-mutations" == sys.argv[1]:
			'''
				def benchmark_mutation_success(
			    input_dir: str,
			    trials: int = 100,
			    seed: int | None = None,
			    dump_failures: bool = False,
			    dump_dir: str = "mutation_failures",
			):
			'''

			s = random.randrange(100000)

			print("Using this seed: "+str(s))

			benchmark_mutation_success(input_dir=sys.argv[2], trials=1000, seed=s, dump_failures=False)
			exit(0)

	if len(sys.argv) >= 2:
		fn = sys.argv[1]
	run_parse_tests(only_one=fn)
	exit(0)
