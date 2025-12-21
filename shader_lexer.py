# shader_lexer.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import re


KEYWORDS = {
    "struct", "uniform", "const", "in", "out", "inout",
    "if", "else", "for", "while", "do",
    "break", "continue", "return", "discard",
    "true", "false",
    "precision", "lowp", "mediump", "highp",
    # basic types / constructors are treated as identifiers but you'll often want them here too:
    "void", "bool", "int", "uint", "float", "double",
    "vec2", "vec3", "vec4", "ivec2", "ivec3", "ivec4",
    "uvec2", "uvec3", "uvec4", "bvec2", "bvec3", "bvec4",
    "mat2", "mat3", "mat4",
    "sampler2D", "sampler3D", "samplerCube", "sampler2DArray",
}

# Ordered (longest-first) so ">>=" matches before ">>" etc.
OPERATORS = [
    ">>=", "<<=",
    "++", "--",
    "+=", "-=", "*=", "/=", "%=",
    "==", "!=", "<=", ">=",
    "&&", "||",
    "<<", ">>",
    "->",  # not GLSL, but harmless if appears
    "=", "+", "-", "*", "/", "%", "<", ">", "!", "~",
    "&", "|", "^",
    "?", ":",
    ".",  # member access
]

PUNCT = {"{", "}", "(", ")", "[", "]", ";", ",", "#"}

# Regex building
_OP_RE = "|".join(re.escape(op) for op in OPERATORS)
_PUNCT_RE = "|".join(re.escape(p) for p in sorted(PUNCT, key=len, reverse=True))

TOKEN_RE = re.compile(
    rf"""
    (?P<WS>\s+) |
    (?P<LINECOMMENT>//[^\n]*\n?) |
    (?P<BLOCKCOMMENT>/\*.*?\*/) |
    (?P<FLOAT>(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?[fF]?) |
    (?P<INT>\d+[uU]?) |
    (?P<ID>[A-Za-z_][A-Za-z0-9_]*) |
    (?P<OP>{_OP_RE}) |
    (?P<PUNCT>{_PUNCT_RE})
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


@dataclass
class Token:
    kind: str
    value: str
    pos: int


def lex(src: str) -> List[Token]:
    out: List[Token] = []
    i = 0
    for m in TOKEN_RE.finditer(src):
        kind = m.lastgroup
        value = m.group(kind)
        pos = m.start()

        if kind in ("WS", "LINECOMMENT", "BLOCKCOMMENT"):
            continue

        if kind == "ID" and value in KEYWORDS:
            out.append(Token("KW", value, pos))
        elif kind == "PUNCT":
            out.append(Token(value, value, pos))  # punctuation as its own kind
        elif kind == "OP":
            out.append(Token("OP", value, pos))
        elif kind == "INT":
            out.append(Token("INT", value, pos))
        elif kind == "FLOAT":
            out.append(Token("FLOAT", value, pos))
        else:
            out.append(Token(kind, value, pos))

        i = m.end()

    out.append(Token("EOF", "", len(src)))
    return out