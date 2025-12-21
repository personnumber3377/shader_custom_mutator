# shader_unparse.py
from __future__ import annotations
from shader_ast import *


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
        args = ", ".join(unparse_expr(a) for a in e.args)
        return f"{unparse_expr(e.callee)}({args})"
    if isinstance(e, IndexExpr):
        return f"{unparse_expr(e.base)}[{unparse_expr(e.index)}]"
    if isinstance(e, MemberExpr):
        return f"{unparse_expr(e.base)}.{e.member}"
    raise TypeError(f"Unhandled expr: {type(e)}")


def unparse_type(t: TypeName) -> str:
    parts = []
    parts.extend(t.qualifiers)
    if t.precision:
        parts.append(t.precision)
    parts.append(t.name)
    return " ".join(parts)


def unparse_stmt(s: Stmt, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(s, EmptyStmt):
        return pad + ";\n"
    if isinstance(s, ExprStmt):
        return pad + f"{unparse_expr(s.expr)};\n"
    if isinstance(s, DeclStmt):
        # reprint as "type a = ... , b;"
        if not s.decls:
            return pad + ";\n"
        t = s.decls[0].type_name
        parts = []
        for d in s.decls:
            frag = d.name
            if d.array_size is not None:
                frag += f"[{unparse_expr(d.array_size)}]"
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
        out += unparse_stmt(s.then_branch, indent + 1 if not isinstance(s.then_branch, BlockStmt) else indent)
        if s.else_branch is not None:
            out += pad + "else\n"
            out += unparse_stmt(s.else_branch, indent + 1 if not isinstance(s.else_branch, BlockStmt) else indent)
        return out
    if isinstance(s, WhileStmt):
        return pad + f"while ({unparse_expr(s.cond)})\n" + unparse_stmt(s.body, indent)
    if isinstance(s, DoWhileStmt):
        out = pad + "do\n" + unparse_stmt(s.body, indent)
        out += pad + f"while ({unparse_expr(s.cond)});\n"
        return out
    if isinstance(s, ForStmt):
        def uinit(x):
            if x is None:
                return ""
            if isinstance(x, DeclStmt):
                # DeclStmt already includes trailing ';' in unparser, strip it
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
    if isinstance(s, DiscardStmt):
        return pad + "discard;\n"
    raise TypeError(f"Unhandled stmt: {type(s)}")


def unparse_tu(tu: TranslationUnit) -> str:
    out = ""
    for item in tu.items:
        if isinstance(item, StructDef):
            out += f"struct {item.name} {{\n"
            for f in item.fields:
                line = f"  {unparse_type(f.type_name)} {f.name}"
                if f.array_size is not None:
                    line += f"[{unparse_expr(f.array_size)}]"
                out += line + ";\n"
            out += "};\n"
        elif isinstance(item, FunctionDef):
            params = []
            for p in item.params:
                s = f"{unparse_type(p.type_name)} {p.name}"
                if p.array_size is not None:
                    s += f"[{unparse_expr(p.array_size)}]"
                params.append(s)
            out += f"{unparse_type(item.return_type)} {item.name}(" + ", ".join(params) + ")\n"
            out += unparse_stmt(item.body, 0)
        elif isinstance(item, GlobalDecl):
            # reuse DeclStmt formatting
            out += unparse_stmt(DeclStmt(item.decls), 0)
        else:
            # ignore unknown
            pass
        out += "\n"
    return out
