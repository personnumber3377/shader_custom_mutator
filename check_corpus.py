#!/usr/bin/env python3
import os
import struct
import subprocess
import tempfile
import sys
import traceback

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

def strip_header_and_null(buf: bytes) -> bytes:
    if not buf or buf[-1] != 0:
        return b""
    return buf[HEADER_SIZE:-1]

def parse_header(buf: bytes):
    if len(buf) < HEADER_SIZE:
        raise ValueError("buffer too small for header")

    shader_type, spec, output = struct.unpack_from("<III", buf, 0)
    return shader_type, spec, output

def run_checker(shader_bytes: bytes, shader_type: int, spec: int, output: int, original_filename: str):
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
            fh = open("/home/oof/failing/"+str(original_filename), "wb")
            fh.write(shader_bytes)
            fh.close()
            return False, out

        return True, out

    except subprocess.TimeoutExpired:
        return False, "timeout"

    finally:
        os.unlink(fname)

# ---- Main driver ----

def check_directory(dirpath: str):
    total = 0
    failures = 0
    printed = 0

    for name in sorted(os.listdir(dirpath)):
        path = os.path.join(dirpath, name)
        if not os.path.isfile(path):
            continue

        try:
            data = open(path, "rb").read()
            shader_type, spec, output = parse_header(data)
            shader_src = strip_header_and_null(data)

            if not shader_src:
                continue

            ok, msg = run_checker(shader_src, shader_type, spec, output, name)
            total += 1

            if not ok:
                failures += 1
                if printed < PRINT_LIMIT:
                    printed += 1
                    print("=" * 60)
                    print(f"FAIL: {name}")
                    print(f"  type={hex(shader_type)} spec={spec} output={output}")
                    print(msg)
                    # os.system("cp ")

        except Exception as e:
            failures += 1
            if printed < PRINT_LIMIT:
                printed += 1
                print("=" * 60)
                print(f"EXCEPTION: {name}")
                traceback.print_exc()

    print("\n==== SUMMARY ====")
    print(f"Total checked : {total}")
    print(f"Failures      : {failures}")
    print(f"Success       : {total - failures}")

# ---- Entry point ----

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <angle-corpus-dir>")
        sys.exit(1)

    check_directory(sys.argv[1])