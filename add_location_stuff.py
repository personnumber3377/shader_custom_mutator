import os
import re
import sys
import subprocess

HEADER_SIZE = 128


def run_shader(path):
    result = subprocess.run(
        ["./dawn_angle_fuzzer", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=5
    )
    return result.stdout.decode("utf-8", errors="ignore")


def needs_fix(output):
    return (
        "expected expression for location" in output or
        "expected expression for binding" in output
    )


def patch_glsl(glsl_text):
    location_counter = 0
    binding_counter = 0

    lines = glsl_text.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("//"):
            new_lines.append(line)
            continue

        # Skip if already has layout
        if "layout(" in stripped:
            new_lines.append(line)
            continue

        # ---- Handle in/out ----
        if re.match(r'^(in|out)\s+[A-Za-z_]', stripped):
            indent = line[:len(line) - len(line.lstrip())]
            new_line = indent + f"layout(location = {location_counter}) " + stripped
            location_counter += 1
            new_lines.append(new_line)
            continue

        # ---- Handle varying (legacy) ----
        if re.match(r'^varying\s+', stripped):
            indent = line[:len(line) - len(line.lstrip())]
            new_line = indent + f"layout(location = {location_counter}) " + stripped
            location_counter += 1
            new_lines.append(new_line)
            continue

        # ---- Handle sampler uniforms ----
        if re.match(r'^uniform\s+sampler', stripped):
            indent = line[:len(line) - len(line.lstrip())]
            new_line = indent + f"layout(binding = {binding_counter}) " + stripped
            binding_counter += 1
            new_lines.append(new_line)
            continue

        new_lines.append(line)

    return "\n".join(new_lines)


def process_file(path):
    with open(path, "rb") as f:
        data = f.read()

    if len(data) <= HEADER_SIZE:
        return False

    header = data[:HEADER_SIZE]
    glsl_bytes = data[HEADER_SIZE:]

    try:
        glsl_text = glsl_bytes.decode("utf-8", errors="ignore")
    except:
        return False

    output = run_shader(path)

    if not needs_fix(output):
        return False

    fixed_glsl = patch_glsl(glsl_text)

    if fixed_glsl == glsl_text:
        return False

    new_data = header + fixed_glsl.encode("utf-8")

    with open(path, "wb") as f:
        f.write(new_data)

    print(f"Patched: {path}")
    return True


def process_directory(directory):
    modified = 0
    tot = 0
    for root, _, files in os.walk(directory):
        if tot % 100 == 0:
            print("Total files: "+str(tot))
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                tot += 1
                if process_file(full_path):
                    modified += 1

    print(f"\nModified {modified} files.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_glsl_feedback.py <corpus_dir>")
        sys.exit(1)

    process_directory(sys.argv[1])