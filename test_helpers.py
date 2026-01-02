
import subprocess
import tempfile
import os
import copy
import traceback
import random
import struct
import sys
from typing import List

HEADER_SIZE = 128
PRINT_COUNT = 10

# CHECKER_PATH = "./angle_shader_checker"  # <-- change if needed
CHECKER_PATH = "./newest_angle"
TIMEOUT = 5.0
GOOD_CORPUS_DIR = "good/"

def check_file_bytes(data: bytes) -> tuple[bool, str]:
    """
    Runs the checker on a single file.
    Returns (ok, stderr_output).
    ok == True  -> "SUCCESS" found in stderr
    ok == False -> otherwise
    """

    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=".bin",
        delete=False
    ) as f:
        fname = f.name
        f.write(data)

    try:
        proc = subprocess.run(
            [CHECKER_PATH, fname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"

    stderr = proc.stderr or ""
    ok = "SUCCESS" in stderr
    return ok, stderr.strip()

# Here check for the null byte and if found, then assume fuzz input...

def strip_header_and_null(buf: bytes) -> bytes:
    if not buf or buf[-1] != 0:
        return b""
    return buf[HEADER_SIZE:-1]

def run_external_checker(buf: bytes, header_len: int, as_vertex=False) -> tuple[bool, str]:
    """
    Returns (ok, output).
    ok == True  -> no ERROR found
    ok == False -> ERROR found or checker failed
    """

    # 1) 2) Strip header and null

    # if not isinstance(buf, bytes) and not isinstance(buf, bytes): # Maybe string type???
    #     buf = buf.decode("ascii") # Encode to ascii encoding...

    data = strip_header_and_null(buf, header_len=header_len)

    # 3) Write to temp file
    if as_vertex:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".vert",
            delete=False
        ) as f:
            fname = f.name
            f.write(data)
    else:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".glsl",
            delete=False
        ) as f:
            fname = f.name
            f.write(data)

    try:
        # 4) Run checker
        proc = subprocess.run(
            ["./angle_shader_translator", "-b=g330", fname], # ["./checker", fname],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5.0,
        )

        output = proc.stdout

        # 5) Check for ERROR
        if "ERROR" in output:
            return False, output

        return True, output

    except subprocess.TimeoutExpired:
        return False, "checker timeout"

    except Exception as e:
        return False, f"checker exception: {e}"

    finally:
        os.unlink(fname)

def run_as_frag_and_vertex(buf: bytes, header_len: int) -> tuple[bool, str]:
    '''
        ok, err = run_external_checker(source, 128) # Run the checker for this source code...
    if not ok: # Error? Try to parse as vertex shader...
        # print("filename "+str(filename)+" errored with: "+str(err))
        ok, err = run_external_checker(source, 128, as_vertex=True) # Try again with a vertex thing...
    '''
    source = strip_header_and_null(buf, header_len=header_len) # Cut off the shit...
    ok, err = run_external_checker(source, 128) # Run the checker for this source code...
    if not ok: # Error? Try to parse as vertex shader...
        print("Failed with these errors here when running as fragment: "+str(err))
        ok, err = run_external_checker(source, 128, as_vertex=True) # Try again with a vertex thing...
        if not ok: # Still errors? Return the error and failure...
            print("Failed with these errors here when running as vertex shader: "+str(err))
            return False, err

    return True, None



HEADER_SIZE = 128
PRINT_LIMIT = 100000000

# ---- ANGLE enums (subset we care about) ----

GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER   = 0x8B31

# ShShaderSpec
SPEC_FLAGS = {
    0: "-s=e2",   # SH_GLES2_SPEC
    1: "-s=w",    # SH_WEBGL_SPEC
    2: "-s=e3",   # SH_GLES3_SPEC
    3: "-s=w2",   # SH_WEBGL2_SPEC
    4: "-s=e31",  # SH_GLES3_1_SPEC
    5: "-s=w3",   # SH_WEBGL3_SPEC (rare)
    6: "-s=e32",  # SH_GLES3_2_SPEC
}

# ShShaderOutput
OUTPUT_FLAGS = {
    0:  None,         # SH_NULL_OUTPUT
    1:  "-b=e",       # SH_ESSL_OUTPUT
    2:  "-b=g",       # SH_GLSL_COMPATIBILITY_OUTPUT
    3:  "-b=g130",
    4:  "-b=g140",
    5:  "-b=g150",
    6:  "-b=g330",
    7:  "-b=g400",
    8:  "-b=g410",
    9:  "-b=g420",
    10: "-b=g430",
    11: "-b=g440",
    12: "-b=g450",
    13: "-b=h9",
    14: "-b=h11",
    15: "-b=v",       # SH_SPIRV_VULKAN_OUTPUT
    16: "-b=m",       # SH_MSL_METAL_OUTPUT
}

# ---- Helpers ----

'''
def strip_header_and_null(buf: bytes) -> bytes:
    if not buf or buf[-1] != 0:
        return b""
    return buf[HEADER_SIZE:-1]
'''

def parse_header(buf: bytes):
    if len(buf) < HEADER_SIZE:
        raise ValueError("buffer too small for header")

    shader_type, spec, output = struct.unpack_from("<III", buf, 0)
    return shader_type, spec, output

def run_checker(shader_bytes: bytes, shader_type: int, spec: int, output: int, original_filename: str = None):
    spec_flag = SPEC_FLAGS.get(spec)
    output_flag = OUTPUT_FLAGS.get(output)

    if spec_flag is None or output_flag is None:
        return False, f"unsupported spec/output: spec={spec}, output={output}"

    suffix = ".vert" if shader_type == GL_VERTEX_SHADER else ".frag"

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(shader_bytes)
        fname = f.name
    

    try:
        cmd = ["./angle_shader_translator", spec_flag, output_flag, fname]
        print("Running this command: "+str(" ".join(cmd)))
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5.0,
        )

        out = proc.stdout
        if "ERROR" in out:
            if original_filename != None:
                fh = open("/home/oof/failing/"+str(original_filename), "wb")
                fh.write(shader_bytes)
                fh.close()
            return False, out

        return True, out

    except subprocess.TimeoutExpired:
        return False, "timeout"

    finally:
        os.unlink(fname)
