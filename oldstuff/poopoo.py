import sys, subprocess, shutil, re, tempfile

CHECK_SCRIPT = "./check_crash.sh"
TIMEOUT = 3

def crashes(path):
    """Returns True if PDFium/Chrome crashes on this file."""
    try:
        r = subprocess.run([CHECK_SCRIPT, path],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           timeout=TIMEOUT)
        return r.returncode == 1
    except subprocess.TimeoutExpired:
        # Timeout = treat as crash
        return True

def extract_stream(pdf_text):
    """Extracts the content stream for object 4 0 obj."""
    # Regex for object 4:
    #   4 0 obj
    #   << ... >>
    #   stream
    #   ...DATA...
    #   endstream
    m = re.search(
        r"4 0 obj\s*<<[^>]*?>>\s*stream\s*(.*?)\s*endstream",
        pdf_text,
        re.DOTALL,
    )
    if not m:
        print("Could not find stream for 4 0 obj")
        sys.exit(1)
    return m.start(1), m.end(1), m.group(1)

def rebuild_pdf(original_text, start, end, new_stream):
    """Stitches a new PDF string together with the replaced stream."""
    return original_text[:start] + new_stream + original_text[end:]

def delta_reduce_stream(orig_pdf, out_pdf):
    """Perform binary chopping on the content stream."""
    with open(orig_pdf, "r", errors="replace") as f:
        pdf_text = f.read()

    start, end, stream = extract_stream(pdf_text)

    data = stream
    print(f"Original stream length: {len(data)} bytes")

    chunk = 32
    while chunk > 4:
        print(f"\nTrying chunk size: {chunk}")
        i = 0
        while i < len(data):
            test_data = data[:i] + data[i+chunk:]
            new_pdf_text = rebuild_pdf(pdf_text, start, end, test_data)

            tmp = "tmp.pdf"
            with open(tmp, "w") as f:
                f.write(new_pdf_text)

            if crashes(tmp):
                print(f"Keeping deletion {i}:{i+chunk}")
                data = test_data
                pdf_text = new_pdf_text
                # Update end offset since length changed
                end = start + len(data)
            else:
                # crash disappeared → revert
                pass

            i += chunk

        chunk //= 2

    print(f"\nFinal minimized stream length: {len(data)} bytes")
    with open(out_pdf, "w") as f:
        f.write(pdf_text)

    print(f"Saved minimized PDF as {out_pdf}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 minimize_stream.py crash.pdf minimized.pdf")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]

    shutil.copy(inp, out)  # initial snapshot
    delta_reduce_stream(inp, out)

if __name__ == "__main__":
    main()