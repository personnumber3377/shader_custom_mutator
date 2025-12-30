
import subprocess
import tempfile
import os
import copy

# Here check for the null byte and if found, then assume fuzz input...

def strip_header_and_null(data, header_len=0):
    datanew = copy.deepcopy(data)
    if datanew and datanew[-1] == 0:
        print("Cutting the header...")
        # 1) Strip header
        datanew = datanew[header_len:]
        # 2) Strip final null byte if present
        datanew = datanew[:-1]

    return datanew

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
    print("buffer before: "+str(buf))
    source = strip_header_and_null(buf, header_len=header_len) # Cut off the shit...
    print("source: "+str(source))
    ok, err = run_external_checker(source, 128) # Run the checker for this source code...
    print("After the thing...")
    if not ok: # Error? Try to parse as vertex shader...
        print("Failed with these errors here when running as fragment: "+str(err))
        ok, err = run_external_checker(source, 128, as_vertex=True) # Try again with a vertex thing...
        if not ok: # Still errors? Return the error and failure...
            print("Failed with these errors here when running as vertex shader: "+str(err))
            return False, err

    return True, None
