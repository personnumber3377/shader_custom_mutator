# shader_parser.py

import re
from typing import List
from shader_ast import *


STRUCT_RE = re.compile(r"\bstruct\s+(\w+)\s*\{", re.MULTILINE)
FUNC_RE = re.compile(r"(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{", re.MULTILINE)
UNIFORM_STRUCT_RE = re.compile(r"uniform\s+struct\s+(\w+)\s*\{", re.MULTILINE)


def _find_matching_brace(src: str, start: int) -> int:
    depth = 0
    for i in range(start, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unmatched brace")


def parse_struct(src: str, start: int) -> tuple[StructDefinition, int]:
    m = STRUCT_RE.match(src, start)
    name = m.group(1)
    body_start = m.end()
    body_end = _find_matching_brace(src, body_start - 1)
    body = src[body_start:body_end]

    fields = []
    for line in body.splitlines():
        line = line.strip().rstrip(";")
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            fields.append(StructField(parts[0], parts[1]))

    return StructDefinition(name, fields), body_end + 2


def parse_function(src: str, start: int) -> tuple[FunctionDefinition, int]:
    m = FUNC_RE.match(src, start)
    ret, name, params = m.groups()
    body_start = m.end()
    body_end = _find_matching_brace(src, body_start - 1)
    body = src[body_start:body_end].strip()

    param_objs = []
    for p in params.split(","):
        p = p.strip()
        if not p:
            continue
        t, n = p.split()
        param_objs.append(FunctionParameter(t, n))

    return FunctionDefinition(ret, name, param_objs, body), body_end + 1


def parse_to_tree(src: str) -> List[Expression]:
    pos = 0
    nodes: List[Expression] = []

    while pos < len(src):
        for parser in (parse_struct, parse_function):
            try:
                node, new_pos = parser(src, pos)
                nodes.append(node)
                pos = new_pos
                break
            except Exception:
                continue
        else:
            # fallback: raw text until next newline
            next_nl = src.find("\n", pos)
            if next_nl == -1:
                nodes.append(RawText(src[pos:]))
                break
            nodes.append(RawText(src[pos:next_nl + 1]))
            pos = next_nl + 1

    return nodes


def unparse_from_tree(tree: List[Expression]) -> str:
    return "".join(node.unparse() for node in tree)