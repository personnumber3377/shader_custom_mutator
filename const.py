

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



# These are needed for layout mutations...

# Identifier-only layouts
LAYOUT_NO_VALUE = [
    # block / matrix
    "shared", "packed", "std140", "std430",
    "row_major", "column_major",

    # fragment
    "early_fragment_tests", "noncoherent",
    "depth_any", "depth_greater", "depth_less", "depth_unchanged",

    # geometry
    "points", "lines", "lines_adjacency",
    "triangles", "triangles_adjacency",
    "line_strip", "triangle_strip",

    # tess eval
    "quads", "isolines",
    "equal_spacing", "fractional_even_spacing", "fractional_odd_spacing",
    "cw", "ccw", "point_mode",

    # image formats
    "rgba32f", "rgba16f", "r32f",
    "rgba8", "rgba8_snorm",
    "rgba32i", "rgba16i", "rgba8i", "r32i",
    "rgba32ui", "rgba16ui", "rgba8ui", "r32ui",
]

# Integer-valued layouts
LAYOUT_WITH_VALUE = [
    "location", "binding", "offset",
    "local_size_x", "local_size_y", "local_size_z",
    "num_views",
    "invocations",
    "max_vertices",
    "vertices",
    "index",
]






# Mutation related constants:



SPECIAL_TYPES = {
    "sampler2D",
    "samplerCube",
    "samplerExternalOES",
    "gsampler2D",
    "image2D",
    "atomic_uint",
    "IMAGE_PARAMS",
}

GENERIC_EXPANSION = {
    "genType": ["float", "vec2", "vec3", "vec4"],
    "genIType": ["int", "ivec2", "ivec3", "ivec4"],
    "genUType": ["uint", "uvec2", "uvec3", "uvec4"],
    "genBType": ["bool", "bvec2", "bvec3", "bvec4"],
}

BUILTIN_NUMERIC_TYPES = {
    "bool", "int", "uint", "float", "double",
    "vec2", "vec3", "vec4",
    "ivec2", "ivec3", "ivec4",
    # "uvec2", "uvec3", "uvec4",
    "bvec2", "bvec3", "bvec4",
    "mat2", "mat3", "mat4",
}

STORAGE_QUALIFIERS = [
    "const", "uniform", "in", "out", "inout",
    "attribute", "varying", "buffer", None
]

PRECISION_QUALIFIERS = [
    "lowp", "mediump", "highp", None
]

PARAM_QUALIFIERS = ["in", "out", "inout"]

MAX_EXPR_DEPTH = 3

MATRIX_TYPES = ["mat2", "mat3", "mat4"]

VEC_TYPE_FLATTENED = {
    "vec2","vec3","vec4",
    "ivec2","ivec3","ivec4",
    "uvec2","uvec3","uvec4",
    "bvec2","bvec3","bvec4",
}

VECTOR_TYPES = {
    "bool":  ["bvec2", "bvec3", "bvec4"],
    "int":   ["ivec2", "ivec3", "ivec4"],
    # "uint":  ["uvec2", "uvec3", "uvec4"],
    "float": ["vec2", "vec3", "vec4"],
}

SCALAR_TYPES = ["bool", "int", "uint", "float"]

BINOPS = [
    # arithmetic
    ("+",  "float", "float", "float"),
    ("-",  "float", "float", "float"),
    ("*",  "float", "float", "float"),
    ("/",  "float", "float", "float"),

    ("+",  "vec3",  "vec3",  "vec3"),
    ("-",  "vec3",  "vec3",  "vec3"),

    # comparisons
    ("<",  "float", "float", "bool"),
    (">",  "float", "float", "bool"),

    # logical
    ("&&", "bool",  "bool",  "bool"),
    ("||", "bool",  "bool",  "bool"),
    ("^^", "bool",  "bool",  "bool"), # This wasn't previously here, but was added later...
]

UNOPS = [
    ("!",  "bool",  "bool"),
    ("-",  "float", "float"),
    ("-",  "vec3",  "vec3"),
]

# These are types that can not be "generated", so ban these.
OPAQUE_TYPES = {
    "sampler2D", "sampler3D", "samplerCube",
    "sampler2DArray",
    "image2D", "image3D",
    "atomic_uint",
    "void",
}

# These are purely for the image operations...

IMAGE_TYPE_TO_COORD = {
    "image2D": "ivec2",
    "iimage2D": "ivec2",
    "uimage2D": "ivec2",

    "image3D": "ivec3",
    "iimage3D": "ivec3",
    "uimage3D": "ivec3",

    "imageCube": "ivec3",
    "iimageCube": "ivec3",
    "uimageCube": "ivec3",

    "image2DArray": "ivec3",
    "iimage2DArray": "ivec3",
    "uimage2DArray": "ivec3",

    "imageCubeArray": "ivec3",
    "iimageCubeArray": "ivec3",
    "uimageCubeArray": "ivec3",

    "imageBuffer": "int",
    "iimageBuffer": "int",
    "uimageBuffer": "int",
}