

# shader_parser.py

# Precedence table (higher = binds tighter)
# This is "good enough" for GLSL fuzzing purposes.
PRECEDENCE = {
    ",": 1,  # sequence
    "=": 2, "+=": 2, "-=": 2, "*=": 2, "/=": 2, "%=": 2, "<<=": 2, ">>=": 2,
    "||": 3,
    "^^": 4,
    "&&": 5,
    "|": 6,
    "^": 7,
    "&": 8,
    "==": 9, "!=": 9,
    "<": 10, ">": 10, "<=": 10, ">=": 10,
    "<<": 11, ">>": 11,
    "+": 12, "-": 12,
    "*": 13, "/": 13, "%": 13,
    ".": 14,  # member access handled as postfix
    "CALL": 15, "INDEX": 15,  # postfix
}

RIGHT_ASSOC = {
    "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=",
    # ternary is right-associative too but handled separately
}


TYPELIKE_KEYWORDS = {
    "void", "bool", "int", "uint", "float", "double",
    "vec2", "vec3", "vec4", "ivec2", "ivec3", "ivec4",
    "uvec2", "uvec3", "uvec4", "bvec2", "bvec3", "bvec4",
    "mat2", "mat3", "mat4",
    "sampler2D", "sampler3D", "samplerCube", "sampler2DArray",
}


QUALIFIERS = {"const", "in", "out", "inout", "uniform", "varying", "flat"} # This didn't have "varying" before... and also not "flat"
PRECISIONS = {"lowp", "mediump", "highp"}

STORAGE_QUALIFIERS = {"in", "out", "uniform", "buffer"}
INTERP_QUALIFIERS = {"flat", "smooth", "noperspective"}
PRECISION_QUALIFIERS = {"lowp", "mediump", "highp"}

ALL_QUALIFIERS = STORAGE_QUALIFIERS | INTERP_QUALIFIERS | PRECISION_QUALIFIERS














# shader_lexer.py:

KEYWORDS = {
    "struct", "uniform", "const", "in", "out", "inout", "varying", "flat", # This did not have varying originally...
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
    "layout", # Support layouts too...
}

# Ordered (longest-first) so ">>=" matches before ">>" etc.
OPERATORS = [
    ">>=", "<<=",
    "++", "--",
    "+=", "-=", "*=", "/=", "%=",
    "==", "!=", "<=", ">=",
    "&&", "||", "^^",
    "<<", ">>",
    "->",  # not GLSL, but harmless if appears
    "=", "+", "-", "*", "/", "%", "<", ">", "!", "~",
    "&", "|", "^",
    "?", ":",
    ".",  # member access
]

PUNCT = {"{", "}", "(", ")", "[", "]", ";", ",", "#"}

