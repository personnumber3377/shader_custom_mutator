# shader_mutator.py
from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional, Tuple, Union
import copy
import random

from shader_ast import *


# ----------------------------
# Utilities
# ----------------------------

BUILTIN_NUMERIC_TYPES = {
    "bool", "int", "uint", "float", "double",
    "vec2", "vec3", "vec4",
    "ivec2", "ivec3", "ivec4",
    "uvec2", "uvec3", "uvec4",
    "bvec2", "bvec3", "bvec4",
    "mat2", "mat3", "mat4",
}

MAX_EXPR_DEPTH = 4

NUMERIC_LITERALS = {
    "int":   lambda r: IntLiteral(r.randrange(-10, 10)),
    "uint":  lambda r: IntLiteral(r.randrange(0, 10)),
    "float": lambda r: FloatLiteral(r.choice([0.0, 0.5, 1.0, -1.0, 2.0])),
    "bool":  lambda r: BoolLiteral(r.choice([True, False])),
}

def deepclone(x):
    # dataclasses + simple classes: copy.deepcopy is fine
    return copy.deepcopy(x)

def coin(rng: random.Random, p: float) -> bool:
    return rng.random() < p

def choose(rng: random.Random, xs: List):
    return xs[rng.randrange(len(xs))] if xs else None


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
    return names


def all_struct_field_names(env: Env, struct_name: str) -> List[str]:
    if struct_name in env.struct_defs:
        return [f.name for f in env.struct_defs[struct_name]]
    if struct_name in env.interface_blocks:
        return [f.name for f in env.interface_blocks[struct_name]]
    return []

# ----------------------------
# Mutations: generate expressions
# ----------------------------

def gen_expr(
    want: Optional[TypeInfo],
    scope: Scope,
    env: Env,
    rng: random.Random,
    depth: int = 0,
) -> Expr:

    if depth >= MAX_EXPR_DEPTH:
        return gen_leaf(want, scope, env, rng)

    choices = []

    # leaf
    choices.append(lambda: gen_leaf(want, scope, env, rng))

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

def gen_leaf(want, scope, env, rng):
    # Prefer existing variables
    vars = candidates_by_type(scope, env, want)
    if vars and rng.random() < 0.7:
        return Identifier(rng.choice(vars))

    # Literal fallback
    if want and want.name in NUMERIC_LITERALS:
        return NUMERIC_LITERALS[want.name](rng)

    # Totally random fallback
    return IntLiteral(rng.randrange(10))

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
    "int": ["+", "-", "~"],
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

def gen_call(want, scope, env, rng, depth):
    candidates = []

    for fname, (ret, params) in env.funcs.items():
        if want is None or ret.name == want.name:
            candidates.append((fname, params))

    if not candidates:
        return gen_leaf(want, scope, env, rng)

    fname, params = rng.choice(candidates)
    args = [gen_expr(pt, scope, env, rng, depth + 1) for pt in params]

    return CallExpr(Identifier(fname), args)

def gen_member_access(want, scope, env, rng, depth):
    candidates = []

    for name, ti in scope.all_vars().items():
        if ti.name in env.struct_defs:
            fields = env.struct_defs[ti.name]
            for f in fields:
                if want is None or typename_to_typeinfo(f.type_name).name == want.name:
                    candidates.append((name, f.name))

    if not candidates:
        return gen_leaf(want, scope, env, rng)

    var, field = rng.choice(candidates)
    return MemberExpr(Identifier(var), field)

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
# Mutations: expressions
# ----------------------------

def mutate_expr(e: Expr, rng: random.Random, scope: Scope, env: Env) -> Expr:
    """
    Returns possibly-mutated expression.
    """

    # Randomly also generate new statements...

    if coin(rng, 0.15):
        return gen_expr(None, scope, env, rng)

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
            op = rng.choice(["+", "-", "!", "~", "++", "--"])
        return UnaryExpr(op, operand, postfix=e.postfix)

    # Binary
    if isinstance(e, BinaryExpr):
        left = mutate_expr(e.left, rng, scope, env)
        right = mutate_expr(e.right, rng, scope, env)
        op = e.op
        if coin(rng, 0.15):
            # keep it mostly sane: swap among common ops
            buckets = [
                ["+", "-", "*", "/"],
                ["<", "<=", ">", ">=", "==", "!="],
                ["&&", "||"],
                ["=", "+=", "-=", "*=", "/="],
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
        if args and coin(rng, 0.15):
            rng.shuffle(args)
        if coin(rng, 0.10) and args:
            # drop or duplicate an arg sometimes
            if coin(rng, 0.5) and len(args) > 1:
                args.pop(rng.randrange(len(args)))
            else:
                args.insert(rng.randrange(len(args)+1), deepclone(rng.choice(args)))
        return CallExpr(callee, args)

    # Indexing
    if isinstance(e, IndexExpr):
        base = mutate_expr(e.base, rng, scope, env)
        idx = mutate_expr(e.index, rng, scope, env)
        if coin(rng, 0.20):
            # nudge constant indices
            if isinstance(idx, IntLiteral):
                idx = IntLiteral(idx.value + rng.choice([-1, 1, 2, -2]))
        return IndexExpr(base, idx)

    # Member access: obj.x -> obj.y if obj is known struct/interface type
    if isinstance(e, MemberExpr):
        base = mutate_expr(e.base, rng, scope, env)

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


def mutate_vardecl(v: VarDecl, rng: random.Random, scope: Scope, env: Env) -> VarDecl:
    v2 = deepclone(v)

    # mutate initializer
    if v2.init is not None and coin(rng, 0.35):
        v2.init = mutate_expr(v2.init, rng, scope, env)
    elif v2.init is None and coin(rng, 0.15):
        # create a simple initializer
        # (for fuzzing we don't care if types mismatch sometimes)
        v2.init = rng.choice([IntLiteral(0), IntLiteral(1), FloatLiteral(1.0), BoolLiteral(True)])
    else:
        if v2.init is None:
            ti = vardecl_to_typeinfo(v2)
            v2.init = gen_expr(ti, scope, env, rng)

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
        for st in s.stmts:
            out_stmts.append(mutate_stmt(st, rng, child, env))

            # Occasionally insert an extra harmless stmt
            if coin(rng, 0.10):
                out_stmts.append(ExprStmt(IntLiteral(rng.randrange(10))))
        # Add a new expression too maybe???
        if coin(rng, 0.30):
            want = TypeInfo("int")
            expr = gen_expr(want, child, env, rng)
            out_stmts.append(ExprStmt(expr))

        # shuffle within block rarely (can break semantics but fine for fuzzing)
        if len(out_stmts) > 2 and coin(rng, 0.05):
            rng.shuffle(out_stmts)

        return BlockStmt(out_stmts)

    if isinstance(s, DeclStmt):
        # define vars into scope, and mutate decls
        new_decls = []
        for d in s.decls:
            d2 = mutate_vardecl(d, rng, scope, env)
            new_decls.append(d2)
            # register in scope
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
        it = deepclone(item)
        dummy_scope = Scope(None)
        it.struct_type.members = mutate_struct_fields(it.struct_type.members, rng, dummy_scope, env)

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

    return item


# ----------------------------
# Public entrypoint
# ----------------------------

def mutate_translation_unit(tu: TranslationUnit, rng: random.Random) -> TranslationUnit:
    """
    High-level mutator: collects env then mutates items.
    Returns a NEW TranslationUnit.
    """
    tu2 = deepclone(tu)
    env = build_env(tu2)

    # Mutate each item; keep env updated as we go.
    new_items: List[TopLevel] = []
    for item in tu2.items:
        new_items.append(mutate_toplevel(item, rng, env))

    # occasional top-level reorder (dangerous but good for fuzzing)
    if len(new_items) > 2 and coin(rng, 0.03):
        rng.shuffle(new_items)

    tu2.items = new_items
    return tu2