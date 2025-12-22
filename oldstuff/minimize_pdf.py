import sys
import subprocess
import shutil
import pikepdf
import os

CHECK_SCRIPT = "./check_crash.sh"
TIMEOUT = 3

def crashes(path):
    """Return True if the crash script reports a crash."""
    try:
        r = subprocess.run([CHECK_SCRIPT, path],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           timeout=TIMEOUT)
        return r.returncode == 1
    except subprocess.TimeoutExpired:
        # Timeout is treated as still-crashing
        return True

def try_write(pdf, path):
    """Write PDF safely."""
    tmp = path + ".tmp"
    pdf.save(tmp)
    shutil.move(tmp, path)

def minimize_stream_data(pdf_path, out_path):
    """
    Try removing chunks of the content stream (obj 4 normally).
    This is where the bug is, so we aggressively shrink that.
    """
    pdf = pikepdf.open(pdf_path)

    # Find all stream objects → target the longest one first.
    stream_objs = [(obj, len(obj.read_bytes())) for obj in pdf.objects if isinstance(obj, pikepdf.Stream)]

    if not stream_objs:
        print("No stream objects found")
        return

    # Sort largest first
    stream_objs.sort(key=lambda x: -x[1])
    target_stream = stream_objs[0][0]

    orig_data = target_stream.read_bytes()
    data = bytearray(orig_data)

    print(f"Original stream size: {len(data)} bytes")

    # Basic binary chopping reducer
    chunk = 1024
    changed = True

    while chunk > 1:
        print(f"\nTrying chunk size {chunk}")
        i = 0
        while i < len(data):
            test_data = data[:i] + data[i+chunk:]
            target_stream.set_stream(test_data)

            try_write(pdf, out_path)

            if crashes(out_path):
                print(f"Crash persists after deleting bytes {i}:{i+chunk}")
                data = test_data
            else:
                # revert
                target_stream.set_stream(data)

            i += chunk

        chunk //= 2

    # Final cleanup: rewrite minimal version
    target_stream.set_stream(data)
    try_write(pdf, out_path)

    print(f"Final minimized stream size: {len(data)} bytes")


def minimize_structure(pdf_path, out_path):
    """Remove objects, dictionary keys, and emptify arrays when possible."""
    pdf = pikepdf.open(pdf_path)

    # List all indirect objects
    objnums = list(pdf.objects)

    changed = True
    while changed:
        changed = False
        for obj in list(pdf.objects):
            # Try removing object entirely
            backup = pdf.copy()
            objnum = obj.objgen

            try:
                del pdf[objnum]
            except Exception:
                continue

            try_write(pdf, out_path)
            if crashes(out_path):
                print(f"Removed object {objnum} successfully")
                changed = True
            else:
                pdf = backup

    try_write(pdf, out_path)
    print("Structural minimization pass done.")


def main():
    if len(sys.argv) != 3:
        print("Usage: minimize_pdf.py input.pdf output.pdf")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]

    # Start with a copy
    shutil.copy(inp, out)

    print("[1] Minimizing structure")
    # minimize_structure(inp, out)

    print("[2] Minimizing streams")
    minimize_stream_data(out, out)

    print("Done. Output saved to", out)


if __name__ == "__main__":
    main()