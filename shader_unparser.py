# shader_unparse.py
from __future__ import annotations

from shader_ast import *


# -------------------------
# Expressions
# -------------------------

def unparse_expr(e: Expr) -> str:
    if isinstance(e, Identifier):
        return e.name
    if isinstance(e, IntLiteral):
        return str(e.value)
    if isinstance(e, FloatLiteral):
        # Keep it simple and stable. repr(float) is fine for fuzzing,
        # but it can emit "1.0" or "0.5" etc; that's OK.
        return repr(e.value)
    if isinstance(e, BoolLiteral):
        return "true" if e.value else "false"
    if isinstance(e, UnaryExpr):
        if e.postfix:
            return f"{unparse_expr(e.operand)}{e.op}"
        return f"{e.op}{unparse_expr(e.operand)}"
    if isinstance(e, BinaryExpr):
        # Parenthesize everything to keep precedence unambiguous.
        return f"({unparse_expr(e.left)} {e.op} {unparse_expr(e.right)})"
    if isinstance(e, TernaryExpr):
        return f"({unparse_expr(e.cond)} ? {unparse_expr(e.then_expr)} : {unparse_expr(e.else_expr)})"
    if isinstance(e, CallExpr):
        args = ", ".join(unparse_expr(a) for a in e.args)
        return f"{unparse_expr(e.callee)}({args})"
    if isinstance(e, IndexExpr):
        return f"{unparse_expr(e.base)}[{unparse_expr(e.index)}]"
    if isinstance(e, MemberExpr):
        return f"{unparse_expr(e.base)}.{e.member}"
    raise TypeError(f"Unhandled expr: {type(e)}")


# -------------------------
# Types
# -------------------------

def unparse_type(t: TypeName) -> str:
    parts = []
    # qualifiers first (e.g. uniform, const, in/out)
    if getattr(t, "qualifiers", None):
        parts.extend(t.qualifiers)
    # precision (lowp/mediump/highp)
    if getattr(t, "precision", None):
        parts.append(t.precision)
    parts.append(t.name)
    return " ".join(parts)


# -------------------------
# Helpers for declarators
# -------------------------

def _unparse_array_suffix(array_size) -> str:
    if array_size is None:
        return ""
    # unsized arrays can be represented as None or some sentinel;
    # your parser uses None only when no brackets, and supports "[]"
    # by matching ']' immediately and leaving array_size None.
    # But that loses whether brackets existed.
    # If you want to preserve unsized arrays, store a sentinel in AST.
    return f"[{unparse_expr(array_size)}]"

def unparse_array_dims(dims):
    out = ""
    for d in dims:
        if d is None:
            out += "[]"
        else:
            out += f"[{unparse_expr(d)}]"
    return out

def _unparse_vardecl_fragment(d: VarDecl) -> str:
    frag = d.name
    # if getattr(d, "array_size", None) is not None:
    #     frag += f"[{unparse_expr(d.array_size)}]"

    for dim in d.array_dims:
        if dim is None:
            frag += "[]"
        else:
            frag += f"[{unparse_expr(dim)}]"

    if getattr(d, "init", None) is not None:
        frag += f" = {unparse_expr(d.init)}"
    return frag


def _unparse_declarator_fragment(d) -> str:
    # Declarator(name, base_type, array_size, init)
    frag = d.name
    '''
    if getattr(d, "array_size", None) is not None:
        frag += f"[{unparse_expr(d.array_size)}]"
    '''

    for dim in d.array_dims:
        if dim is None:
            frag += "[]"
        else:
            frag += f"[{unparse_expr(dim)}]"

    if getattr(d, "init", None) is not None:
        frag += f" = {unparse_expr(d.init)}"
    return frag


def _unparse_struct_body(struct_type: StructType) -> str:
    out = "{\n"
    for m in struct_type.members:
        line = f"  {unparse_type(m.type_name)} {m.name}"
        if m.array_size is not None:
            line += f"[{unparse_expr(m.array_size)}]"
        out += line + ";\n"
    out += "}"
    return out


def unparse_struct_specifier(struct_type) -> str:
    """
    Unparse an inline struct specifier:
      struct foo { float x; }
    or anonymous:
      struct { float x; }
    """
    name = getattr(struct_type, "name", None)
    if name:
        return f"struct {name} {_unparse_struct_body(struct_type)}"
    return f"struct {_unparse_struct_body(struct_type)}"


# -------------------------
# Statements
# -------------------------

def unparse_stmt(s: Stmt, indent: int = 0) -> str:
    pad = "  " * indent

    if isinstance(s, EmptyStmt):
        return pad + ";\n"

    if isinstance(s, ExprStmt):
        return pad + f"{unparse_expr(s.expr)};\n"

    if isinstance(s, DeclStmt):
        # type a = ... , b;
        if not s.decls:
            return pad + ";\n"
        t = s.decls[0].type_name
        parts = [_unparse_vardecl_fragment(d) for d in s.decls]
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
        def uinit(x):
            if x is None:
                return ""
            if isinstance(x, DeclStmt):
                txt = unparse_stmt(x, 0).strip()
                return txt[:-1] if txt.endswith(";") else txt
            if isinstance(x, ExprStmt):
                txt = unparse_stmt(x, 0).strip()
                return txt[:-1] if txt.endswith(";") else txt
            return ""

        init = uinit(s.init)
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

    if isinstance(s, DiscardStmt):
        return pad + "discard;\n"

    raise TypeError(f"Unhandled stmt: {type(s)}")


# -------------------------
# Top-level
# -------------------------

def unparse_tu(tu: TranslationUnit) -> str:
    out = ""

    for item in tu.items:
        # 1) struct definition: struct Name { ... };
        if isinstance(item, StructDef):
            out += f"struct {item.name} {{\n"
            for f in item.fields:
                # line = f"  {unparse_type(f.type_name)} {f.name}"
                # if getattr(f, "array_size", None) is not None:
                #     line += f"[{unparse_expr(f.array_size)}]"

                line = f"  {unparse_type(f.type_name)} {f.name}"
                line += unparse_array_dims(f.array_dims)


                out += line + ";\n"
            out += "};\n\n"
            continue

        # 2) function
        if isinstance(item, FunctionDef):
            params = []
            for p in item.params:
                s = f"{unparse_type(p.type_name)} {p.name}"
                if getattr(p, "array_size", None) is not None:
                    s += f"[{unparse_expr(p.array_size)}]"
                params.append(s)
            out += f"{unparse_type(item.return_type)} {item.name}(" + ", ".join(params) + ")\n"
            out += unparse_stmt(item.body, 0)
            out += "\n"
            continue

        # 3) global decl: mat4 a, b;
        if isinstance(item, GlobalDecl):
            out += unparse_stmt(DeclStmt(item.decls), 0)
            out += "\n"
            continue

        # 4) Interface blocks
        elif isinstance(item, InterfaceBlock):
            out += f"{item.storage} {item.name} {{\n"
            for m in item.members:
                line = f"  {unparse_type(m.type_name)} {m.name}"
                line += unparse_array_dims(m.array_dims)
                out += line + ";\n"
            out += "}"
            if item.instance:
                out += f" {item.instance}"
            out += ";\n\n"

        # 5) inline struct specifier + declarators: struct foo { ... } a, b;
        # Your parser returns StructDecl(struct_type, declarators)
        try:
            StructDecl  # type: ignore[name-defined]
            if isinstance(item, StructDecl):
                st = item.struct_type
                decls = item.declarators

                out += unparse_struct_specifier(st)
                if decls:
                    out += " " + ", ".join(_unparse_declarator_fragment(d) for d in decls)
                out += ";\n\n"
                continue
        except NameError:
            pass

        # 6) some code paths return Declaration(struct_type, declarators)
        try:
            Declaration  # type: ignore[name-defined]
            if isinstance(item, Declaration):
                # item.type could be StructType or something else
                ty = item.type
                decls = item.declarators

                # If it looks like a struct specifier
                if hasattr(ty, "members"):
                    out += unparse_struct_specifier(ty)
                    if decls:
                        out += " " + ", ".join(_unparse_declarator_fragment(d) for d in decls)
                    out += ";\n\n"
                    continue
        except NameError:
            pass

        # Unknown top-level: ignore (but separate with newline so output doesn't glue)
        # out += "\n"

    return out
    