import re
import json
from pathlib import Path

FUNC_RE = re.compile(
    r"""
    (?P<ret>[A-Za-z0-9_]+)
    \s+
    (?P<name>[A-Za-z0-9_]+)
    \s*
    \(
        (?P<params>[^)]*)
    \)
    \s*;
    """,
    re.VERBOSE,
)

DEFAULT_META_RE = re.compile(r"DEFAULT METADATA\s+(\{.*\})")


def parse_builtin_file(path: Path):
    builtins = {}
    current_meta = {}

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("//"):
            continue

        # DEFAULT METADATA {...}
        m = DEFAULT_META_RE.match(line)
        if m:
            current_meta = json.loads(m.group(1))
            continue

        # function declaration
        m = FUNC_RE.match(line)
        if not m:
            continue

        name = m.group("name")
        ret = m.group("ret")

        params_raw = m.group("params").strip()
        params = []

        if params_raw:
            for p in params_raw.split(","):
                p = p.strip()
                # remove qualifiers
                p = re.sub(r"\b(in|out|inout|readonly|writeonly)\b", "", p)
                params.append(p.strip())

        entry = {
            "return": ret,
            "params": params,
            "extensions": [],
        }

        if "essl_extension" in current_meta:
            entry["extensions"] = [
                e.strip() for e in current_meta["essl_extension"].split(",")
            ]

        builtins[name] = entry

    return builtins


def emit_python(builtins: dict, out: Path):
    with out.open("w") as f:
        f.write("# Auto-generated — do not edit\n\n")
        f.write("BUILTIN_FUNCTIONS = {\n")
        for name, info in sorted(builtins.items()):
            f.write(f"    {name!r}: {info!r},\n")
        f.write("}\n")


def main():
    import sys

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    builtins = parse_builtin_file(src)
    emit_python(builtins, dst)


if __name__ == "__main__":
    main()