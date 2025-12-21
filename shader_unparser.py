from __future__ import annotations
from shader_ast import *


# ======================
# Expressions
# ======================

def unparse_expr(e: Expr) -> str:
    if isinstance(e, Identifier):
        return e.name
    if isinstance(e, IntLiteral):
        return str(e.value)
    if isinstance(e, FloatLiteral):
        return repr(e.value)
    if isinstance(e, BoolLiteral):
        return "true" if e.value else "false"
    if isinstance(e, UnaryExpr):
        if e.postfix:
            return f"{unparse_expr(e.operand)}{e.op}"
        return f"{e.op}{unparse_expr(e.operand)}"
    if isinstance(e, BinaryExpr):
        return f"({unparse_expr(e.left)} {e.op} {unparse_expr(e.right)})"
    if isinstance(e, TernaryExpr):
        return f"({unparse_expr(e.cond)} ? {unparse_expr(e.then_expr)} : {unparse_expr(e.else_expr)})"
    if isinstance(e, CallExpr):
        return f"{unparse_expr(e.callee)}({', '.join(unparse_expr(a) for a in e.args)})"
    if isinstance(e, IndexExpr):
        return f"{unparse_expr(e.base)}[{unparse_expr(e.index)}]"
    if isinstance(e, MemberExpr):
        return f"{unparse_expr(e.base)}.{e.member}"
    raise TypeError(f"Unhandled expr: {type(e)}")


# ======================
# Types / Declarators
# ======================

def unparse_type(t: TypeName) -> str:
    parts = []
    parts.extend(t.qualifiers)
    if t.precision:
        parts.append(t.precision)
    parts.append(t.name)
    return " ".join(parts)


def unparse_declarator(d: Declarator) -> str:
    s = d.name
    if d.array_size is not None:
        s += f"[{unparse_expr(d.array_size)}]"
    if d.init is not None:
        s += f" = {unparse_expr(d.init)}"
    return s


# ======================
# Statements
# ======================

def unparse_stmt(s: Stmt, indent: int = 0) -> str:
    pad = "  " * indent

    if isinstance(s, EmptyStmt):
        return pad + ";\n"

    if isinstance(s, ExprStmt):
        return pad + f"{unparse_expr(s.expr)};\n"

    if isinstance(s, DeclStmt):
        t = s.decls[0].type_name
        decls = ", ".join(unparse_declarator(d) for d in s.decls)
        return pad + f"{unparse_type(t)} {decls};\n"

    if isinstance(s, BlockStmt):
        out = pad + "{\n"
        for st in s.stmts:
            out += unparse_stmt(st, indent + 1)
        out += pad + "}\n"
        return out

    if isinstance(s, IfStmt):
        out = pad + f"if ({unparse_expr(s.cond)})\n"
        out += unparse_stmt(s.then_branch, indent)
        if s.else_branch:
            out += pad + "else\n"
            out += unparse_stmt(s.else_branch, indent)
        return out

    if isinstance(s, WhileStmt):
        return pad + f"while ({unparse_expr(s.cond)})\n" + unparse_stmt(s.body, indent)

    if isinstance(s, DoWhileStmt):
        return pad + "do\n" + unparse_stmt(s.body, indent) + pad + f"while ({unparse_expr(s.cond)});\n"

    if isinstance(s, ForStmt):
        init = unparse_stmt(s.init, 0).strip()[:-1] if s.init else ""
        cond = unparse_expr(s.cond) if s.cond else ""
        loop = unparse_expr(s.loop) if s.loop else ""
        out = pad + f"for ({init}; {cond}; {loop})\n"
        out += unparse_stmt(s.body, indent)
        return out

    if isinstance(s, ReturnStmt):
        return pad + ("return;\n" if s.expr is None else f"return {unparse_expr(s.expr)};\n")

    if isinstance(s, BreakStmt):
        return pad + "break;\n"

    if isinstance(s, ContinueStmt):
        return pad + "continue;\n"

    if isinstance(s, DiscardStmt):
        return pad + "discard;\n"

    raise TypeError(f"Unhandled stmt: {type(s)}")


# ======================
# Top-level
# ======================

def unparse_tu(tu: TranslationUnit) -> str:
    out = ""

    for item in tu.items:

        # struct foo { ... };
        if isinstance(item, StructDef):
            out += f"struct {item.name} {{\n"
            for f in item.fields:
                line = f"  {unparse_type(f.type_name)} {f.name}"
                if f.array_size:
                    line += f"[{unparse_expr(f.array_size)}]"
                out += line + ";\n"
            out += "};\n\n"

        # struct foo { ... } a, b;
        elif isinstance(item, Declaration) and isinstance(item.type, StructType):
            out += "struct "
            if item.type.name:
                out += item.type.name + " "
            out += "{\n"
            for m in item.type.members:
                line = f"  {unparse_type(m.type_name)} {m.name}"
                if m.array_size:
                    line += f"[{unparse_expr(m.array_size)}]"
                out += line + ";\n"
            out += "}"
            if item.declarators:
                out += " " + ", ".join(unparse_declarator(d) for d in item.declarators)
            out += ";\n\n"

        elif isinstance(item, FunctionDef):
            params = []
            for p in item.params:
                s = f"{unparse_type(p.type_name)} {p.name}"
                if p.array_size:
                    s += f"[{unparse_expr(p.array_size)}]"
                params.append(s)
            out += f"{unparse_type(item.return_type)} {item.name}({', '.join(params)})\n"
            out += unparse_stmt(item.body)
            out += "\n"

        elif isinstance(item, GlobalDecl):
            out += unparse_stmt(DeclStmt(item.decls)) + "\n"

    return out