# shader_mutator.py
from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional, Tuple, Union
import copy
import random

from shader_ast import *

# For the builtin functions etc...
from builtin_data import BUILTIN_FUNCTIONS

# Debugging???

# DEBUG = True

DEBUG = False

# if DEBUG:# Originally was conditional
import shader_unparser

stop = False

def dlog(msg: str): # Debug logging...
    if DEBUG:
        print("[DEBUG] "+str(msg))
    return

def dexit(msg: str = None): # Exit with error code 1 if in debugging mode...
    if DEBUG:
        if msg != None:
            dlog("[EXITING]: "+str(msg))
        exit(1)
    return

# ----------------------------
# Utilities
# ----------------------------

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

NUMERIC_LITERALS = {
    "int":   lambda r: IntLiteral(r.randrange(0, 10)), # "int":   lambda r: IntLiteral(r.randrange(-10, 10)),
    "uint":  lambda r: IntLiteral(r.randrange(0, 10)),
    "float": lambda r: FloatLiteral(r.choice([0.0, 0.5, 1.0, -1.0, 2.0])),
    "bool":  lambda r: BoolLiteral(r.choice([True, False])),
}

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

def deepclone(x):
    # dataclasses + simple classes: copy.deepcopy is fine
    return copy.deepcopy(x)

def coin(rng: random.Random, p: float) -> bool:
    return rng.random() < p

def choose(rng: random.Random, xs: List):
    return xs[rng.randrange(len(xs))] if xs else None

def has_side_effect(e: Expr) -> bool:
    if isinstance(e, (CallExpr,)):
        return True
    if isinstance(e, UnaryExpr) and e.op in ("++", "--"):
        return True
    if isinstance(e, BinaryExpr) and e.op in ("=", "+=", "-=", "*=", "/="):
        return True
    return False


# These next utilities are for creating composite types more smartly...

def is_vector_name(name: str) -> bool:
    return name in VEC_TYPE_FLATTENED

def is_matrix_name(name: str) -> bool:
    return name in {"mat2","mat3","mat4"}

def is_struct_like(env, name: str) -> bool:
    return (name in env.struct_defs) or (name in env.interface_blocks)

def is_composite(ti: TypeInfo, env) -> bool:
    if ti is None:
        return False
    if ti.is_array():
        return True
    n = ti.name
    return is_vector_name(n) or is_matrix_name(n) or is_struct_like(env, n)

def gen_struct_vardecl(scope: Scope, env: Env, rng: random.Random) -> Optional[DeclStmt]:
    if not env.struct_defs:
        return None

    sname = rng.choice(list(env.struct_defs.keys()))
    vname = f"s_{rng.randrange(10000)}"

    ti = TypeInfo(sname)
    scope.define(vname, ti)

    init = None
    if coin(rng, 0.7):
        init = gen_constructor_expr(ti, scope, env, rng)

    vd = VarDecl(TypeName(sname), vname, init=init, array_dims=None)
    return DeclStmt([vd])

def abort(msg: str): # Crash with message
    assert False, msg

def is_lvalue_expr(e: Expr) -> bool: # left hand side value???
    return isinstance(e, (Identifier, IndexExpr, MemberExpr))

def infer_expr_type(e: Expr, scope: Scope, env: Env) -> Optional[TypeInfo]: # Try to infer type from expression...
    if isinstance(e, IntLiteral):
        return TypeInfo("int")

    if isinstance(e, FloatLiteral):
        return TypeInfo("float")

    if isinstance(e, BoolLiteral):
        return TypeInfo("bool")

    if isinstance(e, Identifier):
        return scope.lookup(e.name) or env.globals.get(e.name)

    if isinstance(e, UnaryExpr):
        return infer_expr_type(e.operand, scope, env)

    if isinstance(e, BinaryExpr):
        if e.op in ("&&", "||", "<", ">", "<=", ">=", "==", "!="):
            return TypeInfo("bool")
        return infer_expr_type(e.left, scope, env)

    if isinstance(e, TernaryExpr):
        return infer_expr_type(e.then_expr, scope, env)

    if isinstance(e, CallExpr):
        if isinstance(e.callee, Identifier):
            fn = env.funcs.get(e.callee.name)
            if fn:
                ret, _ = fn
                return ret
        return None

    if isinstance(e, MemberExpr):
        base_t = infer_expr_type(e.base, scope, env)
        if base_t and base_t.name in env.struct_defs:
            for f in env.struct_defs[base_t.name]:
                if f.name == e.member:
                    return structfield_to_typeinfo(f)
        return None

    if isinstance(e, IndexExpr):
        base_t = infer_expr_type(e.base, scope, env)
        if base_t:
            return base_t.elem()
        return None

    return None

def mutate_expr_typed(e, want, rng, scope, env):
    if coin(rng, 0.05):
        return gen_expr(want, scope, env, rng)
    return mutate_expr(e, rng, scope, env)

# This is used to select the qualifiers

def mutate_declarator_qualifiers(
    d: Declarator,
    rng: random.Random,
    *,
    storage_pool=STORAGE_QUALIFIERS,
    precision_pool=PRECISION_QUALIFIERS,
    interp_pool=None,
    p_add=0.4,
    p_remove=0.3,
    p_replace=0.2,
) -> None:
    """
    Mutate qualifiers in-place on a Declarator.
    """

    qs = set(d.qualifiers or [])

    all_allowed = set(storage_pool)
    if interp_pool:
        all_allowed |= set(interp_pool)
    all_allowed |= set(precision_pool)

    # remove
    if qs and coin(rng, p_remove):
        qs.remove(rng.choice(list(qs)))

    # add
    if coin(rng, p_add):
        q = rng.choice(list(all_allowed))
        if q is not None:
            qs.add(q)

    # replace
    if qs and coin(rng, p_replace):
        qs.clear()
        q = rng.choice(list(all_allowed))
        if q is not None:
            qs.add(q)

    d.qualifiers = list(qs)


def pick_builtin_image(scope: Scope, env: Env, rng: random.Random) -> Identifier | None:
    candidates = []

    # Collect all visible variables
    all_vars = scope.all_vars()
    for name, ti in env.globals.items():
        if name not in all_vars:
            all_vars[name] = ti

    for name, ti in all_vars.items():
        if ti.name in IMAGE_TYPE_TO_COORD:
            candidates.append(name)

    # dlog("Here is the candidates list for type")

    if not candidates:
        return None  # caller should gracefully bail

    return Identifier(rng.choice(candidates))


# THESE NEXT ONES ARE FOR SPECIAL HAVOC!!!



# Chooses a function which returns a scalar value. This is used in the special mutation of return values and function calls...
def pick_function_for_array_return(items, env, rng):
    candidates = []
    for item in items:
        if isinstance(item, FunctionDef):
            ret = typename_to_typeinfo(item.return_type)
            if ret.name in ("int", "uint", "float", "bool"):
                candidates.append(item)
    return rng.choice(candidates) if candidates else None


def rewrite_call_sites(items, fn_name, array_len, rng):
    def visit_expr(e):
        if isinstance(e, CallExpr) and isinstance(e.callee, Identifier):
            if e.callee.name == fn_name:
                idx = rng.choice([0, 0, 1, array_len - 1])
                return IndexExpr(e, IntLiteral(idx))
        # recurse
        for attr in vars(e):
            v = getattr(e, attr)
            if isinstance(v, Expr):
                setattr(e, attr, visit_expr(v))
            elif isinstance(v, list):
                setattr(e, attr, [visit_expr(x) if isinstance(x, Expr) else x for x in v])
        return e

    for item in items:
        if isinstance(item, FunctionDef):
            item.body = visit_expr(item.body)


# END SPECIAL HAVOC FUNCTIONS



def gen_coord_for_image(image_expr: Identifier, scope: Scope, env: Env, rng: random.Random) -> Expr:
    ti = scope.lookup(image_expr.name) or env.globals.get(image_expr.name)
    if ti is None:
        # Extremely defensive fallback
        return IntLiteral(0)

    coord_type = IMAGE_TYPE_TO_COORD.get(ti.name)
    if coord_type is None:
        # Should never happen if pick_builtin_image is correct
        return IntLiteral(0)

    return gen_expr(TypeInfo(coord_type), scope, env, rng)

def find_struct_def_index(items, struct_name: str) -> int | None:
    for i, item in enumerate(items):
        if isinstance(item, StructDef) and item.name == struct_name:
            return i
    return None

# ----------------------------
# Type info helpers
# ----------------------------

class TypeInfo:
    """
    Minimal typing support.
    name: like "float" or "foo" (user struct)
    array_dims: list of dims (None means unsized)
    """
    def __init__(self, name: str, array_dims: Optional[List[Optional[Expr]]] = None):
        self.name = name
        self.array_dims = list(array_dims or [])

    def is_array(self) -> bool:
        return len(self.array_dims) > 0

    def elem(self) -> "TypeInfo":
        if not self.array_dims:
            return self
        return TypeInfo(self.name, self.array_dims[1:])

    def __repr__(self):
        return f"TypeInfo({self.name}, dims={len(self.array_dims)})"


def typename_to_typeinfo(t: Union[TypeName, StructType]) -> TypeInfo:
    if isinstance(t, TypeName):
        return TypeInfo(t.name, [])
    if isinstance(t, StructType):
        # struct specifier type: name may be None
        return TypeInfo(t.name or "<anon_struct>", [])
    # fallback
    return TypeInfo(str(t), [])


def vardecl_to_typeinfo(v: VarDecl) -> TypeInfo:
    base = typename_to_typeinfo(v.type_name)
    return TypeInfo(base.name, getattr(v, "array_dims", []) or [])


def structfield_to_typeinfo(f: StructField) -> TypeInfo:
    base = typename_to_typeinfo(f.type_name)
    # StructField currently has array_size (single) OR you may later add array_dims.
    dims = []
    if hasattr(f, "array_dims") and f.array_dims is not None:
        dims = list(f.array_dims)
    elif getattr(f, "array_size", None) is not None:
        dims = [f.array_size]
    return TypeInfo(base.name, dims)


# ----------------------------
# Symbol table + environment
# ----------------------------

class Env:
    def __init__(self):
        # struct name -> list of StructField (definition shape)
        self.struct_defs: Dict[str, List[StructField]] = {}

        # var name -> TypeInfo
        self.globals: Dict[str, TypeInfo] = {}

        # function name -> signature (optional; not needed much)
        self.funcs: Dict[str, Tuple[TypeInfo, List[TypeInfo]]] = {}

        # interface block "names" are essentially types too
        # (we treat them like structs for member mutation)
        self.interface_blocks: Dict[str, List[StructField]] = {}

    def clone(self) -> "Env":
        e = Env()
        e.struct_defs = deepclone(self.struct_defs)
        e.globals = deepclone(self.globals)
        e.funcs = deepclone(self.funcs)
        e.interface_blocks = deepclone(self.interface_blocks)
        return e


class Scope:
    def __init__(self, parent: Optional["Scope"] = None):
        self.parent = parent
        self.vars: Dict[str, TypeInfo] = {}

    def define(self, name: str, ti: TypeInfo):
        self.vars[name] = ti

    def lookup(self, name: str) -> Optional[TypeInfo]:
        s: Optional[Scope] = self
        while s is not None:
            if name in s.vars:
                return s.vars[name]
            s = s.parent
        return None

    def all_vars(self) -> Dict[str, TypeInfo]:
        out = {}
        s: Optional[Scope] = self
        while s is not None:
            out.update(s.vars)
            s = s.parent
        return out


# ----------------------------
# Collect definitions
# ----------------------------

def _flatten_members(members):
    out = []
    for m in members:
        if isinstance(m, list):
            out.extend(m)
        else:
            out.append(m)
    return out

def build_env(tu: TranslationUnit) -> Env:
    env = Env()
    for item in tu.items:
        if isinstance(item, StructDef):
            env.struct_defs[item.name] = list(item.fields)

        elif isinstance(item, StructDecl):
            # If it is a named struct specifier, capture fields as a "def"
            st = item.struct_type
            if st.name:
                env.struct_defs[st.name] = list(st.members)

        elif isinstance(item, InterfaceBlock):
            # Treat interface block type name as a struct-like thing with members
            members = _flatten_members(item.members)
            env.interface_blocks[item.name] = list(members)
            # Also: its "instance" becomes a global var with that "type"
            if item.instance:
                env.globals[item.instance] = TypeInfo(item.name, [])

        elif isinstance(item, GlobalDecl):
            for d in item.decls:
                env.globals[d.name] = vardecl_to_typeinfo(d)

        elif isinstance(item, FunctionDef):
            # record function name, return + param types
            ret = typename_to_typeinfo(item.return_type)
            params = [typename_to_typeinfo(p.type_name) for p in item.params]
            env.funcs[item.name] = (ret, params)

    return env


# ----------------------------
# Candidate pools
# ----------------------------

def candidates_by_type(scope: Scope, env: Env, want: Optional[TypeInfo]) -> List[str]:
    """
    Prefer same base type name (ignore array dims for now),
    otherwise allow anything.
    """
    allv = scope.all_vars()
    # add globals into scope view (if not already)
    for k, v in env.globals.items():
        if k not in allv:
            allv[k] = v

    names = list(allv.keys())
    if not want:
        return names

    same = [n for n, ti in allv.items() if ti.name == want.name]
    if same:
        return same
    # return names
    # Here actually return an empty list, because otherwise we get bogus types...
    return []


def all_struct_field_names(env: Env, struct_name: str) -> List[str]:
    if struct_name in env.struct_defs:
        return [f.name for f in env.struct_defs[struct_name]]
    if struct_name in env.interface_blocks:
        return [f.name for f in env.interface_blocks[struct_name]]
    return []

def array_len_from_typeinfo(ti: TypeInfo) -> int | None:
    dims = getattr(ti, "array_dims", None)
    if not dims:
        return None  # not an array

    # True multidimensional array (e.g. int a[2][3])
    if len(dims) > 1:
        abort("Multidimensional arrays not supported...")

    d0 = dims[0]

    # Case: unsized array -> float a[];
    if d0 == []:
        return None

    # Flatten accidental nesting: [[100]] → [100]
    if isinstance(d0, list):
        if len(d0) != 1:
            abort("Unexpected array dimension structure")
        d0 = d0[0]

    # Constant integer
    if isinstance(d0, int):
        return d0

    # AST literal like IntLiteral(100)
    if hasattr(d0, "value") and isinstance(d0.value, int):
        return d0.value

    # String token "100"
    if isinstance(d0, str) and d0.isdigit():
        return int(d0)

    # Non-constant expression → cannot expand
    return None

def get_indexable_length(ti: TypeInfo) -> Optional[int]:
    if ti is None:
        return None
    if ti.is_array():
        return array_len_from_typeinfo(ti)
    if ti.name in ("vec2", "ivec2", "uvec2", "bvec2"):
        return 2
    if ti.name in ("vec3", "ivec3", "uvec3", "bvec3"):
        return 3
    if ti.name in ("vec4", "ivec4", "uvec4", "bvec4"):
        return 4
    return None

# ----------------------------
# Mutations: generate expressions
# ----------------------------

MAX_EXPLICIT_ARRAY = 150 # Don't try to generate explicit arrays larger than this, because otherwise it takes two years to generate one...

def gen_atom(want: TypeInfo, scope, env, rng) -> Expr:

    if not want: # Just an extra check. TODO: Get rid of this bullshit here...
        return NUMERIC_LITERALS["int"](rng)

    name = want.name

    n = array_len_from_typeinfo(want)

    # Array case
    if n is not None:
        base = TypeInfo(name)  # IMPORTANT: strip array dims
        if n > MAX_EXPLICIT_ARRAY:
            zero = gen_atom(base, scope, env, rng)
            return CallExpr(Identifier(f"{name}[{n}]"), [zero])
        else:
            elems = [gen_atom(base, scope, env, rng) for _ in range(n)]
            return CallExpr(Identifier(f"{name}[{n}]"), elems)

    # Unsized array → generate a reasonable default
    if want.array_dims == [[]]:
        base = TypeInfo(name)
        zero = gen_atom(base, scope, env, rng)
        return CallExpr(Identifier(f"{name}[1]"), [zero])

    # if n is not None and want.array_dims == [[]]:
    #     return gen_atom(TypeInfo(name), scope, env, rng)

    # Scalars
    if name in NUMERIC_LITERALS:
        return NUMERIC_LITERALS[name](rng)
    if name == "bool":
        return BoolLiteral(bool(rng.getrandbits(1)))

    # Vectors / matrices
    if "vec" in name: # name.startswith("vec"):
        return gen_vector(name, scope, env, rng, atom=True)
    if "mat" in name: # name.startswith("mat"):
        return gen_matrix(name, scope, env, rng, atom=True)

    # Structs
    if name in env.struct_defs:
        fields = env.struct_defs[name]
        args = [gen_atom(structfield_to_typeinfo(f), scope, env, rng) for f in fields]
        return CallExpr(Identifier(name), args)

    abort(f"gen_atom: cannot build {want}")

# What kind of expression?

class ExprKind:
    RVALUE = "rvalue"
    LVALUE = "lvalue"

def gen_expr(
    want: Optional[TypeInfo],
    scope: Scope,
    env: Env,
    rng: random.Random,
    depth: int = 0,
    kind=ExprKind.RVALUE,
) -> Expr:
    
    if depth >= MAX_EXPR_DEPTH:
        # abort("Max depth exceeded...")
        l = gen_leaf(want, scope, env, rng, kind)
        return l

    choices = []

    # composite type (matrixes etc...)

    if want is None and coin(rng, 0.9): # 90% chance of trying to generatae some inferred type...
        want = rng.choice([
            TypeInfo("float"),
            TypeInfo("vec4"),
            TypeInfo("ivec2"),
            TypeInfo(rng.choice(list(env.struct_defs.keys()))) if env.struct_defs else TypeInfo("float")
        ])

    if want and is_composite(want, env) and coin(rng, 0.90): # 30 percent change to to something like this...
        # print("Hit the thing...")
        ctor = gen_constructor_expr(want, scope, env, rng)
        if ctor:
            return ctor

    # leaf
    choices.append(lambda: gen_leaf(want, scope, env, rng, kind))

    # unary
    if want and want.name in ("int", "float", "bool"):
        choices.append(lambda: gen_unary(want, scope, env, rng, depth))

    # binary
    if want and want.name in ("int", "float", "bool"):
        choices.append(lambda: gen_binary(want, scope, env, rng, depth))

    # ternary (boolean condition)
    if want:
        choices.append(lambda: gen_ternary(want, scope, env, rng, depth))

    # function call
    choices.append(lambda: gen_call(want, scope, env, rng, depth))

    # struct member access
    choices.append(lambda: gen_member_access(want, scope, env, rng, depth))

    return rng.choice(choices)()

def gen_leaf(want, scope, env, rng, kind):

    if not want: # want is null, so any type goes...
        return gen_atom(want, scope, env, rng)

    name = want.name # Get name

    vars = candidates_by_type(scope, env, want)

    if vars and coin(rng, 0.20): # Instead of automatically using a variable, throw a coin instead...
        name = rng.choice(vars)
        return Identifier(name)

    if kind == ExprKind.LVALUE:
        # cannot generate literal as lvalue
        return Identifier(rng.choice(list(scope.all_vars().keys())))

    if want and name in NUMERIC_LITERALS:
        return NUMERIC_LITERALS[name](rng)

    # Check for banned types...
    if want and name in OPAQUE_TYPES:
        # Only valid leaf is an identifier of that type
        vars = candidates_by_type(scope, env, want)
        if vars:
            return Identifier(rng.choice(vars))
        # otherwise: give up gracefully
        return NUMERIC_LITERALS["int"](rng)

    # Instead of aborting, just call the atom thing...
    return gen_atom(want, scope, env, rng)
    # abort("Reached end of gen_leaf with want == "+str(want))
    # return IntLiteral(0)

def gen_assignment_stmt(scope, env, rng):
    lhs = gen_expr(None, scope, env, rng, kind=ExprKind.LVALUE)
    rhs = gen_expr(None, scope, env, rng)
    op = rng.choice(["=", "+=", "-=", "*=", "/="])
    return ExprStmt(BinaryExpr(op, lhs, rhs))

BIN_OPS = {
    "int":   ["+", "-", "*", "/", "%"],
    "float": ["+", "-", "*", "/"],
    "bool":  ["&&", "||"],
}

def gen_binary(want, scope, env, rng, depth):
    op = rng.choice(BIN_OPS.get(want.name, ["+"]))

    left = gen_expr(want, scope, env, rng, depth + 1)
    right = gen_expr(want, scope, env, rng, depth + 1)

    return BinaryExpr(op, left, right)

UNARY_OPS = {
    "int": ["+", "-"], # This originally had "~" too...
    "float": ["+", "-"],
    "bool": ["!"],
}

def gen_unary(want, scope, env, rng, depth):
    op = rng.choice(UNARY_OPS.get(want.name, ["+"]))

    operand = gen_expr(want, scope, env, rng, depth + 1)
    return UnaryExpr(op, operand, postfix=False)

def gen_ternary(want, scope, env, rng, depth):
    cond = gen_expr(TypeInfo("bool"), scope, env, rng, depth + 1)
    t = gen_expr(want, scope, env, rng, depth + 1)
    f = gen_expr(want, scope, env, rng, depth + 1)
    return TernaryExpr(cond, t, f)


def gen_builtin_call(want, scope, env, rng, depth):
    candidates = []

    for fname, info in BUILTIN_FUNCTIONS.items():
        ret = info["return"]
        if want is None or ret == want.name:
            candidates.append((fname, info))

    if not candidates:
        return None

    fname, info = rng.choice(candidates)
    args = []

    for p in info["params"]:
        base = p.split("[", 1)[0]
        # generic family
        if base in GENERIC_EXPANSION:
            concrete = rng.choice(GENERIC_EXPANSION[base])
            args.append(gen_expr(TypeInfo(concrete), scope, env, rng, depth + 1)) # Originally had "gen_expr(Type(concrete), ...)"
            continue

        # the IMAGE_PARAMS is a very special type. Handle it before handling other special types...

        if base == 'IMAGE_PARAMS':
            # exit(0)
            image_var = pick_builtin_image(scope, env, rng)
            if not image_var:
                return None # Unable to generate such a call...
            coord_expr = gen_coord_for_image(image_var)
            args.extend([image_var, coord_expr])
            continue

        # special opaque types → use builtin variables
        if base in SPECIAL_TYPES:
            var = env.get_builtin_var(base)
            if var is None:
                return None
            args.append(Identifier(var))
            continue

        # normal type
        args.append(gen_expr(TypeInfo(base), scope, env, rng, depth + 1)) # Originally had "gen_expr(Type(concrete), ...)"
    # dlog("Generated this thing here: "+str(fname)+"("+str(",".join([str(x) for x in args]))+")")
    # exit(0)
    return CallExpr(Identifier(fname), args)

def gen_call(want, scope, env, rng, depth):
    candidates = []

    if coin(rng, 0.10): # 10% chance to generate a builtin function call...
        call = gen_builtin_call(want, scope, env, rng, depth)
        if call: # Return the generated call if one was found...
            # assert False
            return call

    for fname, (ret, params) in env.funcs.items():
        if want is None or ret.name == want.name:
            candidates.append((fname, params))

    if not candidates:
        return gen_leaf(want, scope, env, rng, ExprKind.RVALUE)

    fname, params = rng.choice(candidates)
    args = [gen_expr(pt, scope, env, rng, depth + 1) for pt in params]

    return CallExpr(Identifier(fname), args)

# This code did not use nested structs correctly...
'''
def gen_member_access(want, scope, env, rng, depth):
    vars = [(n, ti) for n, ti in scope.all_vars().items()
            if ti.name in env.struct_defs]

    if not vars:
        return gen_leaf(want, scope, env, rng, ExprKind.RVALUE)

    name, ti = rng.choice(vars)
    fields = env.struct_defs[ti.name]

    f = rng.choice(fields)
    return MemberExpr(Identifier(name), f.name)
'''

def gen_member_access(want, scope, env, rng, depth):
    candidates = [(n, ti) for n, ti in scope.all_vars().items()
                  if ti.name in env.struct_defs]

    if not candidates:
        return gen_leaf(want, scope, env, rng, ExprKind.RVALUE)

    name, ti = rng.choice(candidates)
    expr = Identifier(name)

    for _ in range(rng.randint(1, 3)):
        fields = env.struct_defs.get(ti.name)
        if not fields:
            break
        f = rng.choice(fields)
        expr = MemberExpr(expr, f.name)
        ti = structfield_to_typeinfo(f)
        # Stop here for now...
        # global stop
        # stop = True

        if ti.name not in env.struct_defs:
            break

    return expr

def gen_if(scope, env, rng):
    cond = gen_expr(TypeInfo("bool"), scope, env, rng)
    thenb = BlockStmt([ExprStmt(gen_expr(None, scope, env, rng))])
    elseb = BlockStmt([ExprStmt(gen_expr(None, scope, env, rng))])
    return IfStmt(cond, thenb, elseb)

def gen_switch(scope, env, rng):
    expr = gen_expr(TypeInfo("int"), scope, env, rng)

    cases = []
    for i in range(rng.randint(1, 3)):
        body = [ExprStmt(gen_expr(None, scope, env, rng)), BreakStmt()]
        cases.append(CaseStmt(IntLiteral(i), body))

    if coin(rng, 0.5):
        cases.append(DefaultStmt([BreakStmt()]))

    return SwitchStmt(expr, BlockStmt(cases))

# ----------------------------
# Mutations: structure generation
# ----------------------------

def weighted_choice(rng, items):
    total = sum(w for _, w in items)
    r = rng.uniform(0, total)
    acc = 0
    for val, w in items:
        acc += w
        if acc >= r:
            return val

def gen_random_typename(rng, env, depth=0):
    """
    Returns a TypeName or StructType reference.
    depth limits recursive struct nesting.
    """

    choices = []

    # Scalars
    choices += [("scalar", 4)]

    # Vectors
    choices += [("vector", 4)]

    # Matrices
    choices += [("matrix", 2)]

    # Existing structs (allow nesting)
    if env.struct_defs and depth < 2:
        choices += [("struct", 3)]

    kind = weighted_choice(rng, choices)

    if kind == "scalar":
        return TypeName(rng.choice(SCALAR_TYPES))

    if kind == "vector":
        base = rng.choice(list(VECTOR_TYPES.keys()))
        return TypeName(rng.choice(VECTOR_TYPES[base]))

    if kind == "matrix":
        return TypeName(rng.choice(MATRIX_TYPES))

    if kind == "struct":
        name = rng.choice(list(env.struct_defs.keys()))
        return TypeName(name)

    # Fallback
    return TypeName("float")

def gen_random_struct_field(rng, env, depth): # Generate random structfield object
    t = gen_random_typename(rng, env, depth)

    name = f"f_{rng.randrange(10000)}"

    field = StructField(
        type_name=t,
        name=name,
        array_size=None
    )

    # Occasionally make it an array
    if rng.random() < 0.25:
        field.array_size = IntLiteral(rng.choice([1, 2, 3, 4, 8]))

    return field

def gen_struct_definition(new_items, rng, env):
    name = f"FuzzStruct{rng.randrange(100000)}"

    field_count = rng.randint(1, 6)

    fields = []
    for _ in range(field_count):
        fields.append(gen_random_struct_field(rng, env, depth=1))

    struct = StructDef(name, fields)

    new_items.insert(0, struct)
    env.struct_defs[name] = fields

def gen_matrix(name, scope, env, rng, atom=False):
    # Generate matrix
    n = int(name[-1])
    # args = [gen_expr(TypeInfo("float"), scope, env, rng) for _ in range(n * n)]
    integer = name[0] == "i" # Check for integer...
    # args = [gen_expr(TypeInfo("float"), scope, env, rng) for _ in range(n)]
    if integer:
        if atom:
            args = [IntLiteral(rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0, 2.0])) for _ in range(n * n)]
        else:
            args = [gen_expr(TypeInfo("int"), scope, env, rng) for _ in range(n * n)]
    else:
        if atom:
            args = [FloatLiteral(rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0, 2.0])) for _ in range(n * n)]
        else:
            args = [gen_expr(TypeInfo("float"), scope, env, rng) for _ in range(n * n)]

    return CallExpr(Identifier(name), args)

def gen_vector(name, scope, env, rng, atom=False):
    n = int(name[-1])
    integer = name[0] == "i" # Check for integer...
    # args = [gen_expr(TypeInfo("float"), scope, env, rng) for _ in range(n)]
    if integer:
        if atom:
            args = [IntLiteral(rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0, 2.0])) for _ in range(n)]
        else:
            args = [gen_expr(TypeInfo("int"), scope, env, rng) for _ in range(n)]
    else:
        if atom:
            args = [FloatLiteral(rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0, 2.0])) for _ in range(n)]
        else:
            args = [gen_expr(TypeInfo("float"), scope, env, rng) for _ in range(n)]

    return CallExpr(Identifier(name), args)

# This is used to generate more interesting built in types such as matrixes etc...
def gen_constructor_expr(ti: TypeInfo, scope, env, rng):
    name = ti.name

    if "vec" in name: # name.startswith("vec"):
        return gen_vector(name, scope, env, rng)

    if "mat" in name: # name.startswith("mat"):
        return gen_matrix(name, scope, env, rng)

    if name in env.struct_defs:
        fields = env.struct_defs[name]
        args = []
        for f in fields:
            fti = structfield_to_typeinfo(f)
            args.append(gen_expr(fti, scope, env, rng))
        return CallExpr(Identifier(name), args)

    return None

# ----------------------------
# Mutations: expressions
# ----------------------------

# This class is used to keep track when we have already mutated something...

class MutCtx:
    def __init__(self, budget: int):
        self.budget = budget

    def can_mutate(self) -> bool:
        return self.budget > 0

    def consume(self):
        assert self.budget > 0
        self.budget -= 1

def mutate_expr(e: Expr, rng: random.Random, scope: Scope, env: Env) -> Expr:
    """
    Returns possibly-mutated expression.
    """
    # Randomly also generate new statements...
    if coin(rng, 0.05):
        t = infer_expr_type(e, scope, env)
        return gen_expr(t, scope, env, rng, depth=1)

    # Ban comma operators... this would lead to silly statements like "srcValue(((srcValue , srcValue) , (srcValue , srcValue)))"...
    if isinstance(e, BinaryExpr) and e.op == ",":
        return e.left  # or e.right

    # Identifier replacement (type-aware)
    if isinstance(e, Identifier):
        ti = scope.lookup(e.name) or env.globals.get(e.name)
        if coin(rng, 0.20):
            pool = candidates_by_type(scope, env, ti)
            if pool:
                new_name = choose(rng, pool)
                return Identifier(new_name)
        return e

    # Literals
    if isinstance(e, IntLiteral):
        # TODO: Make sure we do not mutate the index to negative shit... aka array[-1] is invalid...
        if coin(rng, 0.30):
            delta = rng.choice([-2, -1, 1, 2, 8, -8, 16, -16])
            return IntLiteral(e.value + delta)
        return e

    if isinstance(e, FloatLiteral):
        if coin(rng, 0.30):
            # multiply / add tiny value
            if coin(rng, 0.5):
                return FloatLiteral(e.value * rng.choice([0.5, 2.0, -1.0]))
            else:
                return FloatLiteral(e.value + rng.choice([-1.0, -0.5, 0.5, 1.0]))
        return e

    if isinstance(e, BoolLiteral):
        if coin(rng, 0.30):
            return BoolLiteral(not e.value)
        return e

    # Unary
    if isinstance(e, UnaryExpr):
        op = e.op
        operand = mutate_expr(e.operand, rng, scope, env)
        if coin(rng, 0.20):
            # op = rng.choice(["+", "-", "!", "~", "++", "--"])
            # candidates = ["+", "-", "!", "~"]
            
            candidates = ["+", "-", "!"] # Remove the not operator which doesn't even actually exist...

            # if not is_lvalue_expr(e): # If right hand value, then add the things.
            #     candidates.extend(["--", "++"])
            op = rng.choice(candidates)
        return UnaryExpr(op, operand, postfix=e.postfix)

    # Binary
    if isinstance(e, BinaryExpr):
        # left = mutate_expr(e.left, rng, scope, env)
        lt = infer_expr_type(e.left, scope, env)
        left = mutate_expr_typed(e.left, lt, rng, scope, env)
        


        right = mutate_expr(e.right, rng, scope, env)
        op = e.op
        if coin(rng, 0.15):
            # keep it mostly sane: swap among common ops
            buckets = [
                ["+", "-", "*", "/"],
                ["<", "<=", ">", ">=", "==", "!="],
                ["&&", "||", "^^"],
                # ["=", "+=", "-=", "*=", "/="], # Allowing these leads to silly source code snippets like "(main()(srcValue.g) *= srcValue.g);"
            ]
            for b in buckets:
                if op in b:
                    op = rng.choice(b)
                    break
        if coin(rng, 0.10):
            # occasional operand swap
            left, right = right, left
        return BinaryExpr(op, left, right)

    # Ternary
    if isinstance(e, TernaryExpr):
        cond = mutate_expr(e.cond, rng, scope, env)
        t = mutate_expr(e.then_expr, rng, scope, env)
        f = mutate_expr(e.else_expr, rng, scope, env)
        if coin(rng, 0.10):
            t, f = f, t
        return TernaryExpr(cond, t, f)

    # Call
    if isinstance(e, CallExpr):
        callee = mutate_expr(e.callee, rng, scope, env)
        args = [mutate_expr(a, rng, scope, env) for a in e.args]
        
        # TODO: These next things break the calling convention too often and causes compile errors, therefore these are commented out (for now)
        '''
        if args and coin(rng, 0.15):
            rng.shuffle(args)
        if coin(rng, 0.10) and args:
            # drop or duplicate an arg sometimes
            if coin(rng, 0.5) and len(args) > 1:
                args.pop(rng.randrange(len(args)))
            else:
                args.insert(rng.randrange(len(args)+1), deepclone(rng.choice(args)))
        '''

        return CallExpr(callee, args)

    # Indexing
    if isinstance(e, IndexExpr):
        # get_indexable_length
        base = mutate_expr(e.base, rng, scope, env)
        idx = mutate_expr(e.index, rng, scope, env)
        if coin(rng, 0.20):
            # nudge constant indices
            base_t = infer_expr_type(base, scope, env)
            limit = get_indexable_length(base_t)
            if isinstance(idx, IntLiteral) and limit is not None:
                # idx = IntLiteral(idx.value + rng.choice([-1, 1, 2, -2]))
                new = idx.value + rng.choice([-1, 1])
                new = max(0, min(limit - 1, new))
                idx = IntLiteral(new)
        return IndexExpr(base, idx)

    # Member access: obj.x -> obj.y if obj is known struct/interface type
    if isinstance(e, MemberExpr):
        base = mutate_expr(e.base, rng, scope, env)
        if not isinstance(base, Identifier):
            return e # Just return the normal thing...
        # best-effort: only when base is Identifier
        if isinstance(base, Identifier):
            bti = scope.lookup(base.name) or env.globals.get(base.name)
            if bti and coin(rng, 0.35):
                fields = all_struct_field_names(env, bti.name)
                if fields and e.member in fields:
                    # pick a different field name
                    other = [x for x in fields if x != e.member]
                    if other:
                        return MemberExpr(base, choose(rng, other))
        return MemberExpr(base, e.member)

    return e


# ----------------------------
# Mutations: declarations
# ----------------------------

def mutate_array_dims(dims: List[Optional[Expr]], rng: random.Random, scope: Scope, env: Env) -> List[Optional[Expr]]:
    dims = list(dims)
    if not dims:
        if coin(rng, 0.10):
            # add one dimension sometimes
            dims.append(IntLiteral(rng.choice([1, 2, 3, 4, 8, 16])))
        return dims

    # tweak one dim
    if coin(rng, 0.25):
        k = rng.randrange(len(dims))
        if dims[k] is None:
            if coin(rng, 0.5):
                dims[k] = IntLiteral(rng.choice([1, 2, 4, 8]))
        else:
            dims[k] = mutate_expr(dims[k], rng, scope, env)

    # sometimes add/remove dims
    if coin(rng, 0.10) and len(dims) < 4:
        dims.append(IntLiteral(rng.choice([1, 2, 3, 4])))
    if coin(rng, 0.05) and len(dims) > 1:
        dims.pop(rng.randrange(len(dims)))

    return dims

# Used for mutating qualifiers of typenames primarily...

def mutate_typename(t: TypeName, rng: random.Random) -> TypeName:
    t2 = deepclone(t)

    # Exit for debugging...
    # exit(1)

    dlog("Exiting because reached mutate_typename...")
    if DEBUG:
        exit(1)

    qs = set(t2.qualifiers or [])

    # remove qualifier
    if qs and coin(rng, 0.3):
        qs.remove(rng.choice(list(qs)))

    # add storage qualifier
    if coin(rng, 0.3):
        # exit(1) # Debug exit...
        q = rng.choice(list(STORAGE_QUALIFIERS))
        qs.add(q)

    t2.qualifiers = list(qs)

    # precision is exclusive
    if coin(rng, 0.3):
        t2.precision = rng.choice(list(PRECISION_QUALIFIERS) + [None])

    return t2

def mutate_vardecl(v: VarDecl, rng: random.Random, scope: Scope, env: Env) -> VarDecl:
    v2 = deepclone(v)

    # mutate initializer
    if v2.init is not None and coin(rng, 0.35):
        v2.init = mutate_expr(v2.init, rng, scope, env)

    elif v2.init is None and coin(rng, 0.15): # TODO: Disabled for now...
        # create a simple initializer
        # (for fuzzing we don't care if types mismatch sometimes)
        # abort("Called the invalid type mutator...")
        # v2.init = rng.choice([IntLiteral(0), IntLiteral(1), FloatLiteral(1.0), BoolLiteral(True)])

        ti = vardecl_to_typeinfo(v2)
        v2.init = gen_atom(ti, scope, env, rng)

    else:
        if v2.init is None:
            ti = vardecl_to_typeinfo(v2)
            if ti.is_array(): # This is to prevent generating "int i[1] = 0;" etc
                v2.init = gen_atom(ti, scope, env, rng)
            else:
                v2.init = gen_expr(ti, scope, env, rng)

    # TODO: Here we actually mutate the qualifiers. Make this smart such that it know which variables you can add which qualifier to???
    # mutate qualifiers
    '''
    if hasattr(v2, "qualifiers") and coin(rng, 0.30):
        qs = set(v2.qualifiers or [])

        # randomly drop
        if qs and coin(rng, 0.5):
            qs.pop()

        # randomly add
        if coin(rng, 0.5):
            q = rng.choice(STORAGE_QUALIFIERS)
            if q:
                qs.add(q)

        # precision
        if coin(rng, 0.5):
            q = rng.choice(PRECISION_QUALIFIERS)
            if q:
                qs.add(q)

        v2.qualifiers = list(qs)
    '''

    if DEBUG:
        exit(1)

    if coin(rng, 0.25): # Mutate qualifiers???
        v2.type_name = mutate_typename(v2.type_name, rng)

    # mutate array dims
    if hasattr(v2, "array_dims"):
        if coin(rng, 0.25):
            v2.array_dims = mutate_array_dims(v2.array_dims, rng, scope, env)

    return v2


# ----------------------------
# Mutations: statements
# ----------------------------

def mutate_stmt(s: Stmt, rng: random.Random, scope: Scope, env: Env) -> Stmt:
    # Block introduces scope
    if isinstance(s, BlockStmt):
        child = Scope(scope)
        out_stmts: List[Stmt] = []
        '''
        for st in s.stmts:
            out_stmts.append(mutate_stmt(st, rng, child, env))

            # Occasionally insert an extra harmless stmt
            if coin(rng, 0.10):
                # out_stmts.append(ExprStmt(IntLiteral(rng.randrange(10))))
                sd = gen_struct_vardecl(child, env, rng)
                if sd:
                    out_stmts.append(sd)
        '''

        out_stmts = copy.deepcopy(s.stmts)
        if out_stmts:
            rand_ind = rng.randrange(len(out_stmts))
            out_stmts[rand_ind] = mutate_stmt(out_stmts[rand_ind], rng, child, env)
            if coin(rng, 0.10):
                sd = gen_struct_vardecl(child, env, rng)
                if sd:
                    out_stmts.insert(rng.randrange(len(out_stmts)+1), sd)
        # Add a new expression too maybe???
        if coin(rng, 0.30):
            '''
            want = TypeInfo("int")
            expr = gen_expr(want, child, env, rng)
            out_stmts.append(ExprStmt(expr))
            '''


            # Maybe something like this here???

            e = gen_expr(None, child, env, rng)
            if has_side_effect(e):
                out_stmts.append(ExprStmt(e))
            
            # out_stmts.append(gen_assignment_stmt(child, env, rng))

        # shuffle within block rarely (can break semantics but fine for fuzzing)
        if len(out_stmts) > 2 and coin(rng, 0.05):
            rng.shuffle(out_stmts)

        return BlockStmt(out_stmts)

    if isinstance(s, DeclStmt):
        # define vars into scope, and mutate decls
        '''
        new_decls = []
        for d in s.decls:
            d2 = mutate_vardecl(d, rng, scope, env)
            new_decls.append(d2)
            # register in scope
            scope.define(d2.name, vardecl_to_typeinfo(d2))
        '''

        new_decls = []
        mut_i = rng.randrange(len(s.decls)) if s.decls else None

        for i, d in enumerate(s.decls):
            if i == mut_i:
                d2 = mutate_vardecl(d, rng, scope, env)
            else:
                d2 = d  # reuse original object (or deepclone if needed)

            new_decls.append(d2)
            scope.define(d2.name, vardecl_to_typeinfo(d2))

        # maybe reorder decl list
        if len(new_decls) > 1 and coin(rng, 0.10):
            rng.shuffle(new_decls)
        return DeclStmt(new_decls)

    if isinstance(s, ExprStmt):
        return ExprStmt(mutate_expr(s.expr, rng, scope, env))

    if isinstance(s, IfStmt):
        if coin(rng, 0.10): # Generate new thing...
            return gen_if(scope, env, rng)
        cond = mutate_expr(s.cond, rng, scope, env)
        thenb = mutate_stmt(s.then_branch, rng, Scope(scope), env)
        elseb = mutate_stmt(s.else_branch, rng, Scope(scope), env) if s.else_branch else None
        if elseb and coin(rng, 0.05):
            thenb, elseb = elseb, thenb
        return IfStmt(cond, thenb, elseb)

    if isinstance(s, WhileStmt):
        cond = mutate_expr(s.cond, rng, scope, env)
        body = mutate_stmt(s.body, rng, Scope(scope), env)
        return WhileStmt(cond, body)

    if isinstance(s, DoWhileStmt):
        body = mutate_stmt(s.body, rng, Scope(scope), env)
        cond = mutate_expr(s.cond, rng, scope, env)
        return DoWhileStmt(body, cond)

    if isinstance(s, ForStmt):
        child = Scope(scope)
        init = mutate_stmt(s.init, rng, child, env) if s.init else None
        cond = mutate_expr(s.cond, rng, child, env) if s.cond else None
        loop = mutate_expr(s.loop, rng, child, env) if s.loop else None
        body = mutate_stmt(s.body, rng, child, env)
        return ForStmt(init, cond, loop, body)

    if isinstance(s, ReturnStmt):
        if s.expr is None:
            return s
        return ReturnStmt(mutate_expr(s.expr, rng, scope, env))

    if isinstance(s, (BreakStmt, ContinueStmt, DiscardStmt, EmptyStmt)):
        return s

    # Switch / case / default (your AST uses plain classes, not dataclasses)
    if isinstance(s, SwitchStmt):
        if coin(rng, 0.10): # Generate new thing...
            return gen_switch(scope, env, rng)
        expr = mutate_expr(s.expr, rng, scope, env)
        body = mutate_stmt(s.body, rng, Scope(scope), env)
        return SwitchStmt(expr, body)

    if isinstance(s, CaseStmt):
        expr = mutate_expr(s.expr, rng, scope, env)
        child = Scope(scope)
        stmts = [mutate_stmt(x, rng, child, env) for x in s.stmts]
        return CaseStmt(expr, stmts)

    if isinstance(s, DefaultStmt):
        assert False
        child = Scope(scope)
        stmts = [mutate_stmt(x, rng, child, env) for x in s.stmts]
        return DefaultStmt(stmts)

    return s


# ----------------------------
# Mutations: struct definitions
# ----------------------------

def mutate_struct_fields(fields: List[StructField], rng: random.Random, scope: Scope, env: Env) -> List[StructField]:
    fields2 = deepclone(fields)

    # reorder fields sometimes
    if len(fields2) > 1 and coin(rng, 0.10):
        rng.shuffle(fields2)

    # rename one field sometimes (can break users; that’s ok for fuzzing)
    if fields2 and coin(rng, 0.08):
        f = fields2[rng.randrange(len(fields2))]
        f.name = f.name + rng.choice(["_", "0", "1", "x", "y"])

    # mutate one field array size/dims
    if fields2 and coin(rng, 0.20):
        f = fields2[rng.randrange(len(fields2))]
        # support either array_size or array_dims if you later add it
        if hasattr(f, "array_dims") and f.array_dims is not None:
            f.array_dims = mutate_array_dims(f.array_dims, rng, scope, env)
        else:
            if f.array_size is None:
                # TODO: Generate the array size expression instead???
                if coin(rng, 0.5):
                    f.array_size = IntLiteral(rng.choice([1, 2, 4, 8, 16]))
            else:
                f.array_size = mutate_expr(f.array_size, rng, scope, env)

    return fields2


# ----------------------------
# Mutations: top-level
# ----------------------------

def mutate_toplevel(item: TopLevel, rng: random.Random, env: Env) -> TopLevel:

    # StructDef
    if isinstance(item, StructDef):
        dlog("mutating struct definition")
        # if DEBUG:
        #     exit(1)
        dexit()
        # mutate fields
        dummy_scope = Scope(None)
        new_fields = mutate_struct_fields(item.fields, rng, dummy_scope, env)
        it = deepclone(item)
        it.fields = new_fields
        # update env (so member mutations later can use new field lists)
        env.struct_defs[it.name] = list(it.fields)
        return it

    # StructDecl: struct foo {..} a,b;
    if isinstance(item, StructDecl):

        # dlog("item: "+str(item))
        # dlog("item.declarators[0]: "+str(item.declarators[0]))
        # dexit(msg="StructDecl")
        
        # [DEBUG] item: StructDecl(struct_type=StructType(name='S1', members=[StructField(type_name=TypeName(name='samplerCube', precision=None, qualifiers=[]), name='ar', array_size=[])]), declarators=[<shader_ast.Declarator object at 0x7f3aaa261b70>])
        it = deepclone(item)
        dummy_scope = Scope(None)
        it.struct_type.members = mutate_struct_fields(it.struct_type.members, rng, dummy_scope, env)

        # 🔥 NEW: mutate struct storage qualifiers
        '''
        if coin(rng, 0.35):
            # dlog("Example"*1000)
            dlog("stuff...")
            dlog("it: "+str(it))
            it.struct_type = StructType(
                name=it.struct_type.name,
                members=it.struct_type.members,
            )
            dlog("it.struct_type.type_name: "+str(it.struct_type.type_name))
            old_qualifiers = copy.deepcopy(it.struct_type.type_name.qualifiers)
            dlog("old_qualifiers: "+str(old_qualifiers))

            it.struct_type.type_name = mutate_qualifiers(
                TypeName(it.struct_type.name),
                rng,
                storage_pool=["uniform", "buffer", "const", None],
            )
            
            # dlog("it.struct_type.type_name: "+str(it.struct_type.type_name))

            dlog("Here is the thing it.struct_type.type_name.qualifiers: "+str(it.struct_type.type_name.qualifiers))

            # Check for uniform...
            if "uniform" in it.struct_type.type_name.qualifiers and "uniform" not in old_qualifiers: # We added "uniform" ???
                # Stop the thing...
                global stop
                stop = True
        '''


        # 🔥 THIS IS THE IMPORTANT PART 🔥
        # if it.declarators and coin(rng, 0.35):
        if coin(rng, 0.50):
            d = rng.choice(it.declarators)

            old = list(d.qualifiers)
            dlog("stuff")
            mutate_declarator_qualifiers(
                d,
                rng,
                storage_pool=["uniform", "buffer", "const", None],
                precision_pool=PRECISION_QUALIFIERS,
            )

            # optional debug / assert-chasing hook
            # if "uniform" in d.qualifiers and "uniform" not in old:
            #     global stop
            #     stop = True


        # mutate declarators
        if it.declarators and coin(rng, 0.10):
            rng.shuffle(it.declarators)
        if it.declarators and coin(rng, 0.20):
            d = it.declarators[rng.randrange(len(it.declarators))]
            if d.array_size is not None:
                d.array_size = mutate_expr(d.array_size, rng, dummy_scope, env)

        # update env if named
        if it.struct_type.name:
            env.struct_defs[it.struct_type.name] = list(it.struct_type.members)

        return it

    # InterfaceBlock
    if isinstance(item, InterfaceBlock):
        it = deepclone(item)
        dummy_scope = Scope(None)
        members = _flatten_members(it.members)
        members = mutate_struct_fields(members, rng, dummy_scope, env)
        it.members = members  # normalize flat

        # maybe toggle instance name
        if coin(rng, 0.05):
            if it.instance:
                it.instance = None
            else:
                it.instance = it.name + "_inst"

        # update env
        env.interface_blocks[it.name] = list(it.members)
        if it.instance:
            env.globals[it.instance] = TypeInfo(it.name, [])
        return it

    # GlobalDecl
    if isinstance(item, GlobalDecl):
        it = deepclone(item)
        dummy_scope = Scope(None)
        it.decls = [mutate_vardecl(d, rng, dummy_scope, env) for d in it.decls]
        if len(it.decls) > 1 and coin(rng, 0.10):
            rng.shuffle(it.decls)
        for d in it.decls:
            env.globals[d.name] = vardecl_to_typeinfo(d)
        return it

    # FunctionDef
    if isinstance(item, FunctionDef):
        # TODO: Add qualifier mutation. Maybe something like the following? :
        '''
        for p in it.params:
            if coin(rng, 0.25):
                p.qualifier = rng.choice(PARAM_QUALIFIERS)
        '''




        it = deepclone(item)

        # build function scope with params
        fscope = Scope(None)
        for p in it.params:
            fscope.define(p.name, typename_to_typeinfo(p.type_name))

        # mutate body
        it.body = mutate_stmt(it.body, rng, fscope, env)

        # maybe reorder params sometimes
        if len(it.params) > 1 and coin(rng, 0.05):
            rng.shuffle(it.params)

        for p in it.params:
            if coin(rng, 0.25):
                # global stop
                # stop = True
                p.type_name = mutate_typename(p.type_name, rng)

        return it

    # Declaration (your old mixed top-level type)
    if isinstance(item, Declaration):
        it = deepclone(item)
        dummy_scope = Scope(None)
        # mutate declarators a bit
        if it.declarators and coin(rng, 0.10):
            rng.shuffle(it.declarators)
        for d in it.declarators:
            if d.init is not None and coin(rng, 0.25):
                d.init = mutate_expr(d.init, rng, dummy_scope, env)
        return it

    # TODO add function declarations here too...

    return item


# ----------------------------
# Special havoc mode with very specific mutations...
# ----------------------------

# TODO: Consider moving these special mutations to another python file???

def _havoc_apply_struct_decl_qualifiers_all(items: List[TopLevel], rng: random.Random, env: Env) -> List[TopLevel]:
    """
    Apply a coordinated qualifier mutation across ALL StructDecl declarators.

    Goal: make it easy to reach bugs that require multiple correlated qualifier changes
    (e.g. BOTH structs getting 'uniform' in the same iteration).
    """
    it_items = deepclone(items)

    # Decide a single global "plan" for this havoc iteration.
    # Keep it biased toward 'uniform' because that's what you care about here.
    plans = [
        "force_uniform",     # add uniform everywhere (keep existing qualifiers too)
        "replace_uniform",   # replace with exactly 'uniform'
        "toggle_uniform",    # flip uniform on/off everywhere
        "replace_random",    # replace with one random storage qualifier (uniform/buffer/const or none)
        "mix_add_remove",    # use mutate_declarator_qualifiers but with aggressive params everywhere
    ]
    plan = rng.choice(plans)

    # Pick a global storage qualifier for plans that need it
    # Heavily bias towards uniform
    storage_choices = ["uniform", "uniform", "uniform", "buffer", "const", None]
    global_storage = rng.choice(storage_choices)

    # Optional: also apply a single global precision choice sometimes
    # (struct declarators probably ignore precision, but it can perturb parser / AST)
    global_precision = rng.choice(PRECISION_QUALIFIERS)

    changed_any = False

    for i, item in enumerate(it_items):
        if not isinstance(item, StructDecl):
            continue
        if not getattr(item, "declarators", None):
            continue

        # Mutate all declarators of this struct decl
        for d in item.declarators:
            old = list(d.qualifiers or [])

            qs = set(old)

            if plan == "force_uniform":
                # Ensure uniform present, keep other qualifiers
                qs.add("uniform")

            elif plan == "replace_uniform":
                qs = {"uniform"}

            elif plan == "toggle_uniform":
                if "uniform" in qs:
                    qs.remove("uniform")
                else:
                    qs.add("uniform")

            elif plan == "replace_random":
                # Replace with exactly one chosen qualifier (or none)
                qs.clear()
                if global_storage is not None:
                    qs.add(global_storage)

            elif plan == "mix_add_remove":
                # Use your existing mutator but crank it up, applied everywhere.
                mutate_declarator_qualifiers(
                    d,
                    rng,
                    storage_pool=["uniform", "buffer", "const", None],
                    precision_pool=PRECISION_QUALIFIERS,
                    p_add=0.90,
                    p_remove=0.60,
                    p_replace=0.80,
                )
                # mutate_declarator_qualifiers already wrote d.qualifiers; continue
                if d.qualifiers != old:
                    changed_any = True
                continue

            # Apply global precision sometimes (harmless if ignored)
            # Note: Declarator has qualifiers; TypeName holds precision.
            # We can only store precision if Declarator supports it; otherwise skip.
            # If your Declarator doesn't have a precision field, this is a no-op.
            if hasattr(d, "precision") and coin(rng, 0.35):
                d.precision = global_precision

            # Commit qualifier set
            d.qualifiers = [q for q in qs if q is not None]

            if d.qualifiers != old:
                changed_any = True

    # Helpful for your assert-chasing debugging hook
    if changed_any and ("uniform" == global_storage or plan in ("force_uniform", "replace_uniform")):
        global stop
        stop = True

    return it_items

def mutate_function_return_to_array(fn: FunctionDef, rng):
    # N = rng.choice([2, 3, 4, 8, 16, 32, 64, 123])
    N = rng.choice([0, 2, 3, 4, 8, rng.randrange(0,1000)]) # Generate access index
    
    # Change return type
    fn.return_type = TypeName(fn.return_type.name)
    fn.return_type.array_dims = [IntLiteral(N)]

    # Rewrite return statements
    def rewrite_returns(stmt):
        if isinstance(stmt, ReturnStmt) and stmt.expr:
            base_type = fn.return_type.name
            stmt.expr = CallExpr(
                Identifier(f"{base_type}[{N}]"),
                [stmt.expr]
            )
        elif hasattr(stmt, "stmts"):
            for s in stmt.stmts:
                rewrite_returns(s)

    rewrite_returns(fn.body)

    return N

def _havoc_function_scalar_to_array(items, rng, env):
    items = deepclone(items)
    fn = pick_function_for_array_return(items, env, rng)
    print("fn: "+str(fn))
    if not fn:
        return items
    
    global stop
    stop = True
    
    array_len = mutate_function_return_to_array(fn, rng)
    rewrite_call_sites(items, fn.name, array_len, rng)

    return items

def special_havoc(items, rng, env):
    # Check for the thing here...
    print("special_havoc")
    strats = ["struct_qualifier_all", "function_scalar_to_array"]
    strat = rng.choice(strats)
    if strat == "struct_qualifier_all": # Replace the qualifiers of here with the certain thing.
        return _havoc_apply_struct_decl_qualifiers_all(items, rng, env)
    elif strat == "function_scalar_to_array":
        return _havoc_function_scalar_to_array(items, rng, env)

    return items

# ----------------------------
# Public entrypoint
# ----------------------------

DEBUG_STOP = True

def debug_source(tu, tu2): # Debug the stuff here...
    # exit(0)
    if DEBUG_STOP:
        # exit(0)
        if stop:
            # exit(0)
            try:
                result = shader_unparser.unparse_tu(tu2) # Unparse that shit...
            except Exception as e:
                # ???
                print(e)
                exit(1)
            # Now print the thing...
            print("Mutated source code when hit the thing: "+str(result))
            print("Original code was this here: "+str(shader_unparser.unparse_tu(tu)))
            exit(0)

def mutate_translation_unit(tu: TranslationUnit, rng: random.Random) -> TranslationUnit:
    """
    High-level mutator: collects env then mutates items.
    Returns a NEW TranslationUnit.
    """
    tu2 = deepclone(tu)
    env = build_env(tu2)

    # Mutate each item; keep env updated as we go.
    new_items: List[TopLevel] = []
    # for item in tu2.items:
    #     new_items.append(mutate_toplevel(item, rng, env))

    # Instead of mutating each expression, just mutate a randomly chosen one...

    new_items = copy.deepcopy(tu2.items) # Copy...

    # Check for the special havoc mode.

    if coin(rng, 0.99): # 10 percent chance of special havoc mode...
        mutated_items = special_havoc(new_items, rng, env)
        tu2.items = mutated_items
        debug_source(tu, tu2) # Debug that stuff...
        return tu2 # Return the mutated structure...


    # Now get one...

    ind = rng.randrange(len(new_items))

    # Now pop that ...

    item = new_items.pop(ind)

    # Mutate

    item = mutate_toplevel(item, rng, env)

    # Now add that back...

    new_items.insert(ind, item)

    # Structural additions etc...

    # Add struct?
    if coin(rng, 0.02):
        gen_struct_definition(new_items, rng, env)

    # occasional top-level reorder (dangerous but good for fuzzing)
    if len(new_items) > 2 and coin(rng, 0.03):
        rng.shuffle(new_items)

    if coin(rng, 0.10) and env.struct_defs:
        sname = rng.choice(list(env.struct_defs.keys()))
        vname = f"g_{rng.randrange(10000)}"
        init = gen_constructor_expr(TypeInfo(sname), Scope(None), env, rng)

        decl = GlobalDecl([
            VarDecl(
                TypeName(sname),
                vname,
                init=init,
                array_dims=[]
            )
        ])

        # 🔴 FIND STRUCT DEF LOCATION
        idx = find_struct_def_index(new_items, sname)

        if idx is not None:
            # insert immediately AFTER struct definition
            new_items.insert(idx + 1, decl)
        else:
            # fallback (should be rare)
            # assert False
            new_items.insert(0, decl)

        env.globals[vname] = TypeInfo(sname)
        # global stop
        # stop = True

    tu2.items = new_items

    # Now try to unparse that shit...
    # exit(1)
    if DEBUG:
        # return tu2 # Short circuit here...
        debug_source(tu, tu2)
    

    return tu2
