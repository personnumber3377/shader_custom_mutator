from pathlib import Path

prefix = "precision mediump float;\nprecision mediump int;\n\n"

for p in Path(".").iterdir():
    if p.is_file() and p.suffix in {".frag", ".vert", ".glsl"}:
        txt = p.read_text()
        if not txt.lstrip().startswith("precision"):
            p.write_text(prefix + txt)
