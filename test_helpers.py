
import subprocess
import tempfile
import os

# Here check for the null byte and if found, then assume fuzz input...

def strip_header_and_null(data, header_len=0):
    
    if data and data[-1] == 0:
        # 1) Strip header
        data = data[header_len:]
        # 2) Strip final null byte if present
        data = data[:-1]

    return data

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