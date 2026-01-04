# shader_unparser.py
from __future__ import annotations

from shader_ast import *


# -----------------------------
# Small helpers
# -----------------------------

def _is_dim_list(x) -> bool:
    return isinstance(x, list)

def _flatten_members(members):
    """
    Accepts:
      - List[StructField]
      - List[List[StructField]]
      - mixed (because fuzzing 😈)

    Returns:
      - flat List[StructField]
    """
    out = []
    for m in members:
        if isinstance(m, list):
            out.extend(m)
        else:
            out.append(m)
    return out

def flatten_commas(e: Expr) -> list[Expr]:
    if isinstance(e, BinaryExpr) and e.op == ",":
        return flatten_commas(e.left) + flatten_commas(e.right)
    return [e]

def unparse_expr(e: Expr) -> str:
    if isinstance(e, Identifier):
        return e.name
    if isinstance(e, IntLiteral):
        return str(e.value)
    if isinstance(e, FloatLiteral):
        # keep stable-ish textual form
        return repr(e.value)
    if isinstance(e, BoolLiteral):
        return "true" if e.value else "false"
    if isinstance(e, UnaryExpr):
        if e.postfix:
            return f"{unparse_expr(e.operand)}{e.op}"
        return f"{e.op}{unparse_expr(e.operand)}"
    if isinstance(e, BinaryExpr):
        # print("e.left: "+str(e.left))
        # print("e.right: "+str(e.right))
        # if e.op == "," or e.op == "=": # Check for the comma "operator" which is actually used to separate function arguments and such... Also do not wrap when assigning variables etc etc...
        if e.op == "=" or e.op == ",":
            return f"{unparse_expr(e.left)} {e.op} {unparse_expr(e.right)}"
        return f"({unparse_expr(e.left)} {e.op} {unparse_expr(e.right)})"
    if isinstance(e, TernaryExpr):
        return f"({unparse_expr(e.cond)} ? {unparse_expr(e.then_expr)} : {unparse_expr(e.else_expr)})"
    if isinstance(e, CallExpr):
        # args = ", ".join(unparse_expr(a) for a in e.args)

        flat_args = []
        for a in e.args:
            flat_args.extend(flatten_commas(a))
        args = ", ".join(unparse_expr(a) for a in flat_args)

        return f"{unparse_expr(e.callee)}({args})" # This originally had the paranthesis around it, but because we actually break the call convention, because we get function calls like "pow((1, 2))" instead of "pow(1, 2)"
    if isinstance(e, IndexExpr):
        return f"{unparse_expr(e.base)}[{unparse_expr(e.index)}]"
    if isinstance(e, MemberExpr):
        return f"{unparse_expr(e.base)}.{e.member}"
    raise TypeError(f"Unhandled expr: {type(e)}")


def unparse_type(t: TypeName) -> str:
    parts = []
    if getattr(t, "qualifiers", None):
        parts.extend(t.qualifiers)
    if getattr(t, "precision", None):
        parts.append(t.precision)
    parts.append(t.name)
    return " ".join(parts)


def unparse_array_suffix(dims) -> str:
    """
    Accepts:
      - None
      - Expr (single dimension)
      - list[Optional[Expr]] (multi-dim; None => unsized [])
    Returns: "", "[..]", "[..][..]" etc.
    """
    if dims is None:
        return ""

    # single-dim legacy: Expr
    if isinstance(dims, Expr):
        return f"[{unparse_expr(dims)}]"

    # multi-dim: list
    if _is_dim_list(dims):
        out = ""
        for d in dims:
            if d is None:
                out += "[]"
            else:
                out += f"[{unparse_expr(d)}]"
        return out

    # sometimes you accidentally store a tuple; handle it too
    if isinstance(dims, tuple):
        out = ""
        for d in dims:
            if d is None:
                out += "[]"
            else:
                out += f"[{unparse_expr(d)}]"
        return out

    raise TypeError(f"Unhandled array dims type: {type(dims)}")


# -----------------------------
# Struct specifier + body
# -----------------------------

def _unparse_struct_body(struct_type: StructType) -> str:
    out = "{\n"

    members = _flatten_members(struct_type.members)

    for m in members:
        line = f"  {unparse_type(m.type_name)} {m.name}"

        dims = getattr(m, "array_dims", None)
        if dims is None:
            dims = getattr(m, "array_size", None)

        line += unparse_array_suffix(dims)
        out += line + ";\n"

    out += "}"
    return out


def unparse_struct_specifier(struct_type: StructType) -> str:
    name = struct_type.name if struct_type.name else ""
    if name:
        return f"struct {name} {_unparse_struct_body(struct_type)}"
    return f"struct {_unparse_struct_body(struct_type)}"

# -----------------------------
# Statements
# -----------------------------

def unparse_stmt(s: Stmt, indent: int = 0) -> str:
    pad = "  " * indent

    if isinstance(s, EmptyStmt):
        return pad + ";\n"

    if isinstance(s, ExprStmt):
        return pad + f"{unparse_expr(s.expr)};\n"

    if isinstance(s, DeclStmt):
        if not s.decls:
            return pad + ";\n"

        # all decls share same type_name by construction in your parser
        t = s.decls[0].type_name
        parts = []
        for d in s.decls:
            frag = d.name

            # multi-dim arrays
            frag += unparse_array_suffix(d.array_dims)

            if d.init is not None:
                frag += f" = {unparse_expr(d.init)}"
            parts.append(frag)

        return pad + f"{unparse_type(t)} " + ", ".join(parts) + ";\n"

    if isinstance(s, BlockStmt):
        out = pad + "{\n"
        for st in s.stmts:
            out += unparse_stmt(st, indent + 1)
        out += pad + "}\n"
        return out

    if isinstance(s, IfStmt):
        out = pad + f"if ({unparse_expr(s.cond)})\n"
        out += unparse_stmt(s.then_branch, indent + (0 if isinstance(s.then_branch, BlockStmt) else 1))
        if s.else_branch is not None:
            out += pad + "else\n"
            out += unparse_stmt(s.else_branch, indent + (0 if isinstance(s.else_branch, BlockStmt) else 1))
        return out

    if isinstance(s, WhileStmt):
        out = pad + f"while ({unparse_expr(s.cond)})\n"
        out += unparse_stmt(s.body, indent)
        return out

    if isinstance(s, DoWhileStmt):
        out = pad + "do\n"
        out += unparse_stmt(s.body, indent)
        out += pad + f"while ({unparse_expr(s.cond)});\n"
        return out

    if isinstance(s, ForStmt):
        def _uinit(x):
            if x is None:
                return ""
            txt = unparse_stmt(x, 0).strip()
            return txt[:-1] if txt.endswith(";") else txt

        init = _uinit(s.init)
        cond = unparse_expr(s.cond) if s.cond else ""
        loop = unparse_expr(s.loop) if s.loop else ""
        out = pad + f"for ({init}; {cond}; {loop})\n"
        out += unparse_stmt(s.body, indent)
        return out

    if isinstance(s, ReturnStmt):
        if s.expr is None:
            return pad + "return;\n"
        return pad + f"return {unparse_expr(s.expr)};\n"

    if isinstance(s, BreakStmt):
        return pad + "break;\n"

    if isinstance(s, ContinueStmt):
        return pad + "continue;\n"

    if isinstance(s, DiscardStmt):
        return pad + "discard;\n"

    # ---- Switch support (your custom classes) ----
    if isinstance(s, SwitchStmt):
        out = pad + f"switch ({unparse_expr(s.expr)})\n"
        out += unparse_stmt(s.body, indent)
        return out

    if isinstance(s, CaseStmt):
        out = pad + f"case {unparse_expr(s.expr)}:\n"
        for st in s.stmts:
            out += unparse_stmt(st, indent + 1)
        return out

    if isinstance(s, DefaultStmt):
        out = pad + "default:\n"
        for st in s.stmts:
            out += unparse_stmt(st, indent + 1)
        return out

    # This is to handle inline struct definitions inside functions...
    if isinstance(s, StructDecl):
        # assert False
        storage = None
        if s.declarators and getattr(s.declarators[0], "storage", None):
            storage = s.declarators[0].storage

        out = ""
        if storage:
            out += storage + " "

        out += unparse_struct_specifier(s.struct_type) # Originally was +=
        if s.declarators:
            out += " " + ", ".join(_unparse_declarator(d) for d in s.declarators)
        out += ";\n\n"
        # continue
        return out

    raise TypeError(f"Unhandled stmt: {type(s)}")


# -----------------------------
# Top-level
# -----------------------------

def _unparse_declarator(d: Declarator) -> str:
    s = d.name
    s += unparse_array_suffix(getattr(d, "array_dims", None) or getattr(d, "array_size", None))
    if getattr(d, "init", None) is not None:
        s += f" = {unparse_expr(d.init)}"
    return s


def _unparse_var_decl(d: VarDecl) -> str:
    s = d.name + unparse_array_suffix(d.array_dims)
    if d.init is not None:
        s += f" = {unparse_expr(d.init)}"
    return s


def unparse_tu(tu: TranslationUnit) -> str:
    out = ""
    # Process directives first
    for d in getattr(tu, "directives", []):
        if isinstance(d, PragmaDirective):
            out += f"#pragma {d.pragma_string}"
        elif isinstance(d, VersionDirective):
            out += f"#version {d.version}\n"
        elif isinstance(d, ExtensionDirective):
            print("d.name: "+str(d.name))
            if ":" in d.name: # Check for potential errors here. This is a parsing artifact due to the way we process these...
                d.name = d.name.replace(":", "")
            out += f"#extension {d.name} : {d.behavior}\n"
    if out:
        out += "\n"

        # Check for the mandatory precision statements. If these do not exist, then the shader gets rejected right out the gate...

    if "precision mediump float" not in out and "highp" not in out: # Check for the high precision floats, if they do exist, then do not emit the mediump preamble thing...

        prec_preamble = '''precision mediump float;\nprecision mediump int;\n\n'''
        out += prec_preamble #  + out # Prepend that...

    for item in tu.items:
        # old explicit struct definition form (if you still use it)
        if isinstance(item, StructDef):
            out += f"struct {item.name} {{\n"
            for f in item.fields:
                line = f"  {unparse_type(f.type_name)} {f.name}"
                # StructField may carry list dims in array_size too
                dims = getattr(f, "array_dims", None)
                if dims is None:
                    dims = getattr(f, "array_size", None)
                line += unparse_array_suffix(dims)
                out += line + ";\n"
            out += "};\n\n"
            continue

        # struct specifier + declarators (your common case)
        if isinstance(item, StructDecl):
            storage = None
            if item.declarators and getattr(item.declarators[0], "storage", None):
                storage = item.declarators[0].storage
            # out = ""
            if storage:
                out += storage + " "

            out += unparse_struct_specifier(item.struct_type)
            if item.declarators:
                out += " " + ", ".join(_unparse_declarator(d) for d in item.declarators)
            out += ";\n\n"
            continue

        # generic "Declaration" used by your parser for struct-specifier declarations too
        if isinstance(item, Declaration):
            # if it's a struct specifier:
            if isinstance(item.type, StructType):
                out += unparse_struct_specifier(item.type)
                if item.declarators:
                    out += " " + ", ".join(_unparse_declarator(d) for d in item.declarators)
                out += ";\n\n"
            else:
                # fallback: try like a normal decl statement
                # (you can extend this later)
                out += ";\n\n"
            continue

        if isinstance(item, InterfaceBlock):
            # storage is like: uniform/in/out/buffer
            out += f"{item.storage} {item.name} "
            # members should be list[StructField]-like
            tmp_struct = StructType(name=None, members=item.members)
            out += _unparse_struct_body(tmp_struct)
            if item.instance:
                out += f" {item.instance}"
                # Add possible array lengths...
                out += unparse_array_suffix(item.array_dims)
            out += ";\n\n"
            continue

        if isinstance(item, FunctionDef):
            params = []
            for p in item.params:
                ps = f"{unparse_type(p.type_name)} {p.name}"
                ps += unparse_array_suffix(getattr(p, "array_dims", None) or getattr(p, "array_size", None))
                params.append(ps)
            out += f"{unparse_type(item.return_type)} {item.name}(" + ", ".join(params) + ")\n"
            out += unparse_stmt(item.body, 0)
            out += "\n"
            continue

        if isinstance(item, FunctionDecl):
            params = []
            for p in item.params:
                ps = f"{unparse_type(p.type_name)} {p.name}"
                ps += unparse_array_suffix(getattr(p, "array_dims", None) or getattr(p, "array_size", None))
                params.append(ps)
            out += f"{unparse_type(item.return_type)} {item.name}(" + ", ".join(params) + ");\n"
            # out += unparse_stmt(item.body, 0)
            # out += "\n"
            continue

        if isinstance(item, GlobalDecl):
            # group as single declaration statement
            out += unparse_stmt(DeclStmt(item.decls), 0)
            out += "\n"
            continue

        # unknown => ignore safely
        out += "\n"

    return out
