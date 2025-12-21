# shader_parser.py
from __future__ import annotations
from typing import List, Optional, Union

from shader_lexer import Token, lex
from shader_ast import *


class ParseError(Exception):
    pass


# Precedence table (higher = binds tighter)
# This is "good enough" for GLSL fuzzing purposes.
PRECEDENCE = {
    ",": 1,  # sequence
    "=": 2, "+=": 2, "-=": 2, "*=": 2, "/=": 2, "%=": 2, "<<=": 2, ">>=": 2,
    "||": 3,
    "&&": 4,
    "|": 5,
    "^": 6,
    "&": 7,
    "==": 8, "!=": 8,
    "<": 9, ">": 9, "<=": 9, ">=": 9,
    "<<": 10, ">>": 10,
    "+": 11, "-": 11,
    "*": 12, "/": 12, "%": 12,
    ".": 13,  # member access handled as postfix
    "CALL": 14, "INDEX": 14,  # postfix
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


QUALIFIERS = {"const", "in", "out", "inout", "uniform"}
PRECISIONS = {"lowp", "mediump", "highp"}


class Parser:
    def __init__(self, tokens: List[Token]):
        self.toks = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.toks[self.i]

    def advance(self) -> Token:
        t = self.toks[self.i]
        self.i += 1
        return t

    def match(self, kind: str, value: Optional[str] = None) -> bool:
        t = self.peek()
        if t.kind == kind:
            if value is None or t.value == value:
                self.advance()
                return True
        # punctuation encoded as kind==value, e.g. kind="{" value="{"
        if value is None and t.kind == kind and t.value == kind:
            self.advance()
            return True
        if value is not None and t.kind == kind and t.value == value:
            self.advance()
            return True
        return False

    def expect(self, kind: str, value: Optional[str] = None) -> Token:
        t = self.peek()
        if value is None:
            if t.kind == kind or (t.kind == kind and t.value == kind):
                return self.advance()
        else:
            if (t.kind == kind and t.value == value) or (t.kind == value and t.value == value):
                return self.advance()
        raise ParseError(f"Expected {kind} {value or ''} at {t.pos}, got {t.kind}:{t.value}")

    # -----------------------
    # Expression parsing (Pratt)
    # -----------------------

    def parse_expr(self, min_prec: int = 0) -> Expr:
        left = self.parse_prefix()

        while True:
            t = self.peek()
            print(t)
            if t.kind == "OP" and t.value in ("++", "--"):
                print("stuff")
                # postfix binds very tightly
                if PRECEDENCE["CALL"] < min_prec:
                    break
                op = self.advance().value
                left = UnaryExpr(op, left, postfix=True)
                continue

            # postfix: call
            if t.kind == "(":
                if PRECEDENCE["CALL"] < min_prec:
                    break
                left = self.parse_call(left)
                continue

            # postfix: indexing
            if t.kind == "[":
                if PRECEDENCE["INDEX"] < min_prec:
                    break
                left = self.parse_index(left)
                continue

            # postfix: member access (.)
            if t.kind == "OP" and t.value == ".":
                if PRECEDENCE["."] < min_prec:
                    break
                self.advance()
                ident = self.expect("ID")  # swizzle/field
                left = MemberExpr(left, ident.value)
                continue

            # ternary
            if t.kind == "OP" and t.value == "?":
                if 0 < min_prec:  # ternary is very low-ish; only parse if allowed
                    break
                self.advance()
                then_expr = self.parse_expr(0)
                self.expect("OP", ":")
                else_expr = self.parse_expr(0)
                left = TernaryExpr(left, then_expr, else_expr)
                continue

            # binary op
            if t.kind == "OP" and t.value in PRECEDENCE:
                op = t.value
                prec = PRECEDENCE[op]
                if prec < min_prec:
                    break
                self.advance()
                next_min = prec + (0 if op in RIGHT_ASSOC else 1)
                right = self.parse_expr(next_min)
                left = BinaryExpr(op, left, right)
                continue

            # sequence comma operator (treat as binary)
            if t.kind == ",":
                op = ","
                prec = PRECEDENCE[op]
                if prec < min_prec:
                    break
                self.advance()
                right = self.parse_expr(prec + 1)
                left = BinaryExpr(op, left, right)
                continue

            break

        return left

    def parse_declarator_list(self, base_type):
        decls = []
        while True:
            name = self.expect("ID").value

            array_size = None
            if self.match("["):
                if not self.match("]"):
                    array_size = self.parse_expr(0)
                    self.expect("]")

            init = None
            if self.match("="):
                init = self.parse_expr(0)

            decls.append(Declarator(name, base_type, array_size, init))

            if not self.match(","):
                break
        return decls

    def parse_prefix(self) -> Expr:
        t = self.peek()

        # parenthesized
        if t.kind == "(":
            self.advance()
            e = self.parse_expr(0)
            self.expect(")")
            return e

        # literals
        if t.kind == "INT":
            self.advance()
            s = t.value.lower()
            unsigned = False
            if s.endswith("u"):
                unsigned = True
                s = s[:-1]

            if s.startswith("0x"):
                val = int(s, 16)
            elif s.startswith("0") and len(s) > 1:
                val = int(s, 8)
            else:
                val = int(s, 10)

            return IntLiteral(val)

        if t.kind == "FLOAT":
            self.advance()
            s = t.value.rstrip("fFlL")
            return FloatLiteral(float(s))

        if t.kind == "KW" and t.value in ("true", "false"):
            self.advance()
            return BoolLiteral(t.value == "true")

        # unary
        if t.kind == "OP" and t.value in ("+", "-", "!", "~", "++", "--"):
            op = self.advance().value
            # operand = self.parse_expr(PRECEDENCE["*"])  # unary binds fairly tightly
            operand = self.parse_expr(PRECEDENCE["CALL"])
            return UnaryExpr(op, operand, postfix=False)

        # identifier
        if t.kind in ("ID", "KW"):
            # allow keywords as identifiers sometimes (GLSL constructors/types)
            self.advance()
            return Identifier(t.value)

        raise ParseError(f"Unexpected token in expression at {t.pos}: {t.kind}:{t.value}")

    def parse_call(self, callee: Expr) -> Expr:
        self.expect("(")
        args: List[Expr] = []
        if not self.match(")"):
            while True:
                args.append(self.parse_expr(0))
                if self.match(")"):
                    break
                self.expect(",")
        return CallExpr(callee, args)

    def parse_index(self, base: Expr) -> Expr:
        self.expect("[")
        idx = self.parse_expr(0)
        self.expect("]")
        return IndexExpr(base, idx)

    # -----------------------
    # Types / Decls
    # -----------------------

    def parse_type_name(self) -> TypeName:
        qualifiers: List[str] = []
        precision: Optional[str] = None

        while True:
            t = self.peek()
            if t.kind == "KW" and t.value in QUALIFIERS:
                qualifiers.append(self.advance().value)
                continue
            if t.kind == "KW" and t.value in PRECISIONS:
                precision = self.advance().value
                continue
            break

        # type identifier or built-in keyword
        t = self.peek()
        if t.kind == "KW" and t.value in TYPELIKE_KEYWORDS:
            name = self.advance().value
            return TypeName(name=name, precision=precision, qualifiers=qualifiers)

        if t.kind == "ID":
            name = self.advance().value
            return TypeName(name=name, precision=precision, qualifiers=qualifiers)

        raise ParseError(f"Expected type name at {t.pos}, got {t.kind}:{t.value}")
    '''
    def parse_struct_member(self) -> StructField:
        tname = self.parse_type_name()
        name = self.expect("ID").value

        arr = None
        if self.match("["):
            if not self.match("]"):
                arr = self.parse_expr(0)
                self.expect("]")
        self.expect(";")
        return StructField(tname, name, arr)
    '''

    def parse_struct_member(self) -> List[StructField]:
        tname = self.parse_type_name()
        fields = []

        while True:
            name = self.expect("ID").value

            arr = None
            if self.match("["):
                if not self.match("]"):
                    arr = self.parse_expr(0)
                    self.expect("]")

            fields.append(StructField(tname, name, arr))

            if not self.match(","):
                break

        self.expect(";")
        return fields

    def parse_var_decl(self, type_name: TypeName) -> VarDecl:
        ident = self.expect("ID")
        name = ident.value

        array_size: Optional[Expr] = None
        if self.match("["):
            if not self.match("]"):
                array_size = self.parse_expr(0)
                self.expect("]")
            # else unsized array

        init: Optional[Expr] = None
        if self.match("OP", "="):
            init = self.parse_expr(0)

        return VarDecl(type_name=type_name, name=name, array_size=array_size, init=init)

    def parse_struct_specifier(self):
        if self.peek().kind == "KW" and self.peek().value == "struct":
            self.advance()
        else:
            self.expect("KW", "struct")

        name = None
        if self.peek().kind == "ID":
            name = self.advance().value

        self.expect("{")
        members = []
        while not self.match("}"):
            fields = self.parse_struct_member()
            members.extend(fields)
        return StructType(name, members)

    def parse_decl_stmt(self) -> DeclStmt:
        # print("self.peek().value: "+str(self.peek().value))
        print("self.peek().value: "+str(self.peek().value))
        if self.peek().value == "struct":
            print("poopoo")
            struct_type = self.parse_struct_specifier()

            declarators = []
            if self.peek().kind == "ID":
                declarators = self.parse_declarator_list(struct_type)

            self.expect(";")
            return Declaration(struct_type, declarators)

        tname = self.parse_type_name()
        decls: List[VarDecl] = [self.parse_var_decl(tname)]
        while self.match(","):
            decls.append(self.parse_var_decl(tname))
        self.expect(";")
        return DeclStmt(decls)

    # -----------------------
    # Statements
    # -----------------------

    def parse_stmt(self) -> Stmt:
        t = self.peek()
        # print(t)

        # block
        if t.kind == "{":
            return self.parse_block()

        # empty
        if t.kind == ";":
            self.advance()
            return EmptyStmt()

        # if
        if t.kind == "KW" and t.value == "if":
            self.advance()
            self.expect("(")
            cond = self.parse_expr(0)
            self.expect(")")
            then_branch = self.parse_stmt()
            else_branch = None
            if self.peek().kind == "KW" and self.peek().value == "else":
                self.advance()
                else_branch = self.parse_stmt()
            return IfStmt(cond, then_branch, else_branch)

        # while
        if t.kind == "KW" and t.value == "while":
            self.advance()
            self.expect("(")
            cond = self.parse_expr(0)
            self.expect(")")
            body = self.parse_stmt()
            return WhileStmt(cond, body)

        # do-while
        if t.kind == "KW" and t.value == "do":
            self.advance()
            body = self.parse_stmt()
            self.expect("KW", "while")
            self.expect("(")
            cond = self.parse_expr(0)
            self.expect(")")
            self.expect(";")
            return DoWhileStmt(body, cond)

        # for
        if t.kind == "KW" and t.value == "for":
            self.advance()
            self.expect("(")
            init: Optional[Union[DeclStmt, ExprStmt]] = None

            # init can be decl, expr, or empty
            if self.peek().kind != ";":
                if self._looks_like_decl():
                    init = self.parse_decl_stmt()
                else:
                    e = self.parse_expr(0)
                    self.expect(";")
                    init = ExprStmt(e)
            else:
                self.expect(";")

            cond: Optional[Expr] = None
            if self.peek().kind != ";":
                cond = self.parse_expr(0)
            self.expect(";")

            loop: Optional[Expr] = None
            if self.peek().kind != ")":
                loop = self.parse_expr(0)
            self.expect(")")

            body = self.parse_stmt()
            return ForStmt(init, cond, loop, body)

        # jump statements
        if t.kind == "KW" and t.value == "return":
            self.advance()
            if self.peek().kind == ";":
                self.advance()
                return ReturnStmt(None)
            e = self.parse_expr(0)
            self.expect(";")
            return ReturnStmt(e)

        if t.kind == "KW" and t.value == "break":
            self.advance()
            self.expect(";")
            return BreakStmt()

        if t.kind == "KW" and t.value == "continue":
            self.advance()
            self.expect(";")
            return ContinueStmt()

        if t.kind == "KW" and t.value == "discard":
            self.advance()
            self.expect(";")
            return DiscardStmt()

        # declaration vs expression statement
        if self._looks_like_decl():
            return self.parse_decl_stmt()

        # expression statement
        e = self.parse_expr(0)
        self.expect(";")
        return ExprStmt(e)

    def parse_block(self) -> BlockStmt:
        self.expect("{")
        stmts: List[Stmt] = []
        while self.peek().kind != "}":
            if self.peek().kind == "EOF":
                raise ParseError("Unexpected EOF in block")
            stmts.append(self.parse_stmt())
        self.expect("}")
        return BlockStmt(stmts)

    def _looks_like_decl(self) -> bool:
        """
        Heuristic: qualifiers/precision/type then identifier.
        This is not perfect GLSL disambiguation but good enough for fuzzing.
        """
        j = self.i
        # skip qualifiers/precision
        while j < len(self.toks):
            t = self.toks[j]
            if t.kind == "KW" and (t.value in QUALIFIERS or t.value in PRECISIONS):
                j += 1
                continue
            break
        if j >= len(self.toks):
            return False
        t = self.toks[j]
        # type can be builtin keyword or identifier (user-defined struct type)
        if not ((t.kind == "KW" and t.value in TYPELIKE_KEYWORDS) or t.kind == "ID"):
            return False
        # next must exist and be an identifier (var name) or '(' (function)
        if j + 1 >= len(self.toks):
            return False
        t2 = self.toks[j + 1]
        return t2.kind == "ID"

    # -----------------------
    # Top-level parsing
    # -----------------------

    def parse_struct_toplevel_decl(self):
        # token is KW struct
        struct_type = self.parse_struct_specifier()

        declarators = []
        # After `}` may come `;` or declarators
        if self.peek().kind == "ID":
            declarators = self.parse_declarator_list(struct_type)

        self.expect(";")
        return StructDecl(struct_type, declarators)

    def parse_struct_def(self) -> StructDef:
        self.expect("KW", "struct")
        name = self.expect("ID").value
        self.expect("{")
        fields: List[StructField] = []
        while self.peek().kind != "}":
            tname = self.parse_type_name()
            fname = self.expect("ID").value
            arr: Optional[Expr] = None
            if self.match("["):
                if not self.match("]"):
                    arr = self.parse_expr(0)
                    self.expect("]")
            self.expect(";")
            fields.append(StructField(tname, fname, arr))
        self.expect("}")
        self.expect(";")
        return StructDef(name, fields)

    def parse_function_def(self) -> FunctionDef:
        ret = self.parse_type_name()
        fname = self.expect("ID").value
        self.expect("(")
        params: List[FunctionParam] = []
        if not self.match(")"):
            while True:
                ptype = self.parse_type_name()
                pname = self.expect("ID").value
                parr: Optional[Expr] = None
                if self.match("["):
                    if not self.match("]"):
                        parr = self.parse_expr(0)
                        self.expect("]")
                params.append(FunctionParam(ptype, pname, parr))
                if self.match(")"):
                    break
                self.expect(",")
        body = self.parse_block()
        return FunctionDef(ret, fname, params, body)

    def parse_global_decl(self) -> GlobalDecl:
        # parse type then one or more var decls then ;
        tname = self.parse_type_name()
        decls: List[VarDecl] = [self.parse_var_decl(tname)]
        while self.match(","):
            decls.append(self.parse_var_decl(tname))
        self.expect(";")
        return GlobalDecl(decls)

    def parse_translation_unit(self) -> TranslationUnit:
        items: List[TopLevel] = []
        while self.peek().kind != "EOF":
            t = self.peek()

            if t.kind == "KW" and t.value == "struct":
                items.append(self.parse_struct_toplevel_decl())
                continue

            if self._looks_like_decl():
                save = self.i
                _ = self.parse_type_name()
                _ = self.expect("ID")
                if self.peek().kind == "(":
                    self.i = save
                    items.append(self.parse_function_def())
                else:
                    self.i = save
                    items.append(self.parse_global_decl())
                continue

            self.advance()

        return TranslationUnit(items)


def parse_to_tree(shader_source: str) -> TranslationUnit:
    tokens = lex(shader_source)
    p = Parser(tokens)
    return p.parse_translation_unit()