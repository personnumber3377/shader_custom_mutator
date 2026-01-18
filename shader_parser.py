# shader_parser.py
from __future__ import annotations
from typing import List, Optional, Union

from shader_lexer import Token, lex
from shader_ast import *
from const import *

from collections.abc import Iterable

class ParseError(Exception):
    pass

DEBUG = True

current_input = None

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
        if DEBUG:
            print("Got failure here: "+str(current_input[t.pos:t.pos+100]))
        raise ParseError(f"Expected {kind} {value or ''} at {t.pos}, got {t.kind}:{t.value}")

    # -----------------------
    # Expression parsing (Pratt)
    # -----------------------

    # This is a helper for parsing inline struct definitions...

    def _looks_like_struct_decl_stmt(self) -> bool:
        j = self.i

        # Skip qualifiers like const, in, out, uniform, etc.
        while j < len(self.toks):
            t = self.toks[j]
            if t.kind == "KW" and t.value in QUALIFIERS:
                j += 1
                continue
            break

        # Now must see 'struct'
        return j < len(self.toks) and self.toks[j].kind == "KW" and self.toks[j].value == "struct"

    # This function basically just skips over the layout things. We do not currently support them in the thing...
    def parse_layout_qualifier(self):
        # assumes current token is 'layout'
        self.advance()              # 'layout'
        self.expect("(")
        depth = 1
        while depth > 0:
            t = self.advance()
            if t.kind == "(":
                depth += 1
            elif t.kind == ")":
                depth -= 1

    def parse_expr(self, min_prec: int = 0) -> Expr:
        left = self.parse_prefix()

        while True:
            t = self.peek()
            if t.kind == "OP" and t.value in ("++", "--"):
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
            # if self.match("="):
            #     init = self.parse_expr(0)

            if self.peek().kind == "OP" and self.peek().value == "=":
                self.advance()
                init = self.parse_expr(0)
                # init = self.parse_expr(PRECEDENCE[","] + 1)
                if self.peek().kind == ",":
                    pass

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
        if DEBUG:
            print("Got error here: "+str(current_input[t.pos:t.pos+100])) # Print for debugging the thing...
        raise ParseError(f"Expected type name at {t.pos}, got {t.kind}:{t.value}")

    def parse_struct_member(self) -> list[StructField]:
        # NEW: skip optional layout qualifiers
        # TODO: Support layouts inside struct members???
        while self.peek().kind == "KW" and self.peek().value == "layout":
            self.parse_layout_qualifier()

        tname = self.parse_type_name()
        fields = []

        while True:
            name = self.expect("ID").value

            array_dims = []
            while self.match("["):
                if not self.match("]"):
                    array_dims.append(self.parse_expr(0))
                    self.expect("]")
                else:
                    array_dims.append(None)

            fields.append(StructField(tname, name, array_dims))

            if not self.match(","):
                break

        self.expect(";")
        return fields

    def parse_var_decl(self, type_name: TypeName) -> VarDecl:
        name = self.expect("ID").value

        array_dims = []
        while self.match("["):
            if self.match("]"):
                array_dims.append(None)
            else:
                array_dims.append(self.parse_expr(0))
                self.expect("]")

        init = None
        if self.match("OP", "="):
            init = self.parse_expr(0)
            # init = self.parse_expr(PRECEDENCE[","] + 1)
            if self.peek().kind == ",":
                pass

        return VarDecl(type_name, name, array_dims, init)

    def parse_struct_specifier(self):
        self.expect("KW", "struct")

        name = None
        if self.peek().kind == "ID":
            name = self.advance().value

        self.expect("{")
        members = []

        while not self.match("}"):
            fields = self.parse_struct_member()
            members.extend(fields)   # ✅ always safe now

        return StructType(name, members)

    def parse_decl_stmt(self) -> DeclStmt:
        if self.peek().value == "struct":
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

    def parse_case_stmt(self) -> CaseStmt:
        self.expect("ID", "case")
        expr = self.parse_expr(0)
        # We need to get rid of this here...
        # self.expect(":")
        self.advance() # Consume the ":"
        stmts = []

        while True:
            t = self.peek()
            if (t.value in ("case", "default")) or t.kind == "}":
                break
            stmts.append(self.parse_stmt())

        return CaseStmt(expr, stmts)


    def parse_default_stmt(self) -> DefaultStmt:
        self.expect("ID", "default")
        # We need to get rid of this here...
        # self.expect(":")
        self.advance() # Consume the ":"
        stmts = []

        while True:
            t = self.peek()
            # if (t.kind == "KW" and t.value in ("case", "default")) or t.kind == "}":
            if (t.value in ("case", "default")) or t.kind == "}":
                break
            stmts.append(self.parse_stmt())

        return DefaultStmt(stmts)

    # -----------------------
    # Switch statements
    # -----------------------

    def parse_switch_block(self) -> BlockStmt:
        self.expect("{")
        stmts = []

        while not self.match("}"):
            t = self.peek()

            if t.value == "case":
                stmts.append(self.parse_case_stmt())
                continue

            if t.value == "default":
                stmts.append(self.parse_default_stmt())
                continue

            # statements inside a case
            stmts.append(self.parse_stmt())

        return BlockStmt(stmts)

    # -----------------------
    # Statements
    # -----------------------

    def parse_stmt(self) -> Stmt:
        t = self.peek()

        # switch statements
        if t.value == "switch": # This originally was t.kind == "KW"
            self.advance()
            self.expect("(")
            expr = self.parse_expr(0)
            self.expect(")")
            body = self.parse_switch_block()
            return SwitchStmt(expr, body)


        # block
        if t.kind == "{":
            return self.parse_block()

        # struct definition inside a block (???)
        # if t.kind == "KW" and t.value == "struct": # TODO: This check here fails, because struct definitions can have "const" in the front of it etc..
        if self._looks_like_struct_decl_stmt():
            struct_decl = self.parse_struct_toplevel_decl()
            return struct_decl

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
        # if not ((t.kind == "KW" and t.value in TYPELIKE_KEYWORDS) or t.kind == "ID"):
        #     return False

        # The previous codeblock didn't handle inline structs properly, therefore put the thing here...

        
        if not (
            (t.kind == "KW" and t.value in TYPELIKE_KEYWORDS)
            or t.kind == "ID"
            # or (t.kind == "KW" and t.value == "struct")
        ):
            return False
        

        # next must exist and be an identifier (var name) or '(' (function)
        if j + 1 >= len(self.toks):
            return False
        
        # This is to handle potential functions that returns an array...
        j2 = j + 1
        while j2 < len(self.toks) and self.toks[j2].kind == "[":
            j2 += 1
            if j2 < len(self.toks) and self.toks[j2].kind != "]":
                j2 += 1
            if j2 < len(self.toks) and self.toks[j2].kind == "]":
                j2 += 1

        if j2 >= len(self.toks):
            return False

        return self.toks[j2].kind == "ID"

        # t2 = self.toks[j + 1]
        # return t2.kind == "ID"

    # -----------------------
    # Top-level parsing
    # -----------------------

    '''
    def parse_struct_toplevel_decl(self):
        # token is KW struct
        struct_type = self.parse_struct_specifier()

        declarators = []
        # After `}` may come `;` or declarators
        # if self.peek().kind == "ID":
        #     declarators = self.parse_declarator_list(struct_type)

        if not self.peek().kind == ";":
            declarators = self.parse_declarator_list(struct_type)

        self.expect(";")
        return StructDecl(struct_type, declarators)
    '''

    '''
    def parse_struct_toplevel_decl(self):
        # ---- NEW: parse qualifiers first ----
        qualifiers = []
        while self.peek().kind == "KW" and self.peek().value in QUALIFIERS:
            qualifiers.append(self.advance().value)

        # Now we MUST see 'struct'
        struct_type = self.parse_struct_specifier()

        # Attach qualifiers to the struct type
        if qualifiers:
            struct_type.qualifiers = qualifiers

        declarators = []

        # After `}` may come `;` or declarators
        if self.peek().kind != ";":
            declarators = self.parse_declarator_list(struct_type)

        self.expect(";")
        return StructDecl(struct_type, declarators)
    '''

    '''
    def parse_struct_toplevel_decl(self):
        qualifiers = []
        while self.peek().kind == "KW" and self.peek().value in QUALIFIERS:
            print("self.peek().kind: "+str(self.peek().kind))
            print("self.peek().kind: "+str(self.peek().value))
            qualifiers.append(self.advance().value)

        struct_type = self.parse_struct_specifier()

        declarators = []
        if self.peek().kind != ";":
            declarators = self.parse_declarator_list(struct_type)

            # 👇 APPLY STORAGE TO DECLARATORS, NOT STRUCT
            for d in declarators:
                d.storage = qualifiers[0] if qualifiers else None

        self.expect(";")
        return StructDecl(struct_type, declarators)
    '''

    def parse_struct_toplevel_decl(self):
        qualifiers = []
        while self.peek().kind == "KW" and self.peek().value in QUALIFIERS:
            # print("self.peek().kind: "+str(self.peek().kind))
            # print("self.peek().kind: "+str(self.peek().value))
            qualifiers.append(self.advance().value)

        struct_type = self.parse_struct_specifier()

        declarators = []
        if self.peek().kind != ";":
            declarators = self.parse_declarator_list(struct_type)
            for d in declarators:
                d.qualifiers = qualifiers.copy()

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

    def parse_function_def_or_decl(self) -> FunctionDef:
        ret = self.parse_type_name()

        # parse array dimensions on return type
        array_dims = []
        while self.match("["):
            if self.match("]"):
                array_dims.append(None)
            else:
                array_dims.append(self.parse_expr(0))
                self.expect("]")

        if array_dims:
            ret = TypeName(
                name=ret.name,
                precision=ret.precision,
                qualifiers=ret.qualifiers,
                array_dims=array_dims
            )

        fname = self.expect("ID").value
        self.expect("(")
        params: List[FunctionParam] = []
        if not self.match(")"):
            while True:
                '''
                ptype = self.parse_type_name()
                pname = self.expect("ID").value
                parr: Optional[Expr] = None
                if self.match("["):
                    if not self.match("]"):
                        parr = self.parse_expr(0)
                        self.expect("]")
                '''

                ptype = self.parse_type_name()

                # Parameter name is OPTIONAL
                pname = None
                if self.peek().kind == "ID":
                    pname = self.expect("ID").value

                parr = None
                if self.match("["):
                    if not self.match("]"):
                        parr = self.parse_expr(0)
                        self.expect("]")
                params.append(FunctionParam(ptype, pname, parr))
                if self.match(")"):
                    break
                self.expect(",")
        # Declaration or definition?
        if self.peek().kind == "{": # Function definition (normal route...)
            body = self.parse_block()
            return FunctionDef(ret, fname, params, body)
        else:
            self.expect(";") # The semicolon after the declaration...
            return FunctionDecl(ret, fname, params)

    def _looks_like_interface_block(self) -> bool:
        j = self.i
        # storage qualifier
        if self.toks[j].value not in ("uniform", "in", "out", "buffer"):
            return False
        j += 1
        # block name
        if j >= len(self.toks) or self.toks[j].kind != "ID":
            return False
        j += 1
        # must be followed by '{'
        return j < len(self.toks) and self.toks[j].kind == "{"

    def parse_interface_block(self) -> InterfaceBlock:
        storage = self.advance().value          # uniform / in / out / buffer
        name = self.expect("ID").value

        self.expect("{")
        members = []
        while self.peek().kind != "}":
            members.append(self.parse_struct_member())
        self.expect("}")

        # This next snippet of code doesn't support arrays
        '''
        instance = None
        if self.peek().kind == "ID":
            instance = self.advance().value

        self.expect(";")
        return InterfaceBlock(storage, name, members, instance)
        '''

        instance = None
        array_dims = []

        if self.peek().kind == "ID":
            instance = self.advance().value

            # ---- NEW: parse optional array dimensions ----
            while self.match("["):
                if self.match("]"):
                    array_dims.append(None)
                else:
                    array_dims.append(self.parse_expr(0))
                    self.expect("]")

        self.expect(";")
        return InterfaceBlock(storage, name, members, instance, array_dims)

    def parse_global_decl(self) -> GlobalDecl:
        # parse type then one or more var decls then ;
        tname = self.parse_type_name()
        decls: List[VarDecl] = [self.parse_var_decl(tname)]
        while self.match(","):
            decls.append(self.parse_var_decl(tname))
        self.expect(";")
        return GlobalDecl(decls)

    '''
    class DeclaratorLayout:
    def __init__(self, name, value = None): # If value is None, then this qualifier thing doesn't need a value for example "std140" if value is not None, then for example "location=0" is emitted, these objects are then joined with a comma to become layout(std140, location=0) etc...
        self.name = name
        self.value = value

    # This is a special case, since this is a toplevel expression that doesn't end in a newline...
    @dataclass
    class LayoutQualifier(TopLevel):
        declarators: List[DeclaratorLayout]
    '''

    def parse_layout(self):
        # Now try to parse the layout...
        self.expect("KW", "layout") # Get the layout, then do the stuff...
        self.expect("(") # opening paranthesis
        decls = [] # Initialize declarator list...
        while self.peek().kind == "ID":
            # Check if name or name=value thing...
            name = self.advance().value
            # Now check for the equal sign...
            if self.peek().value == "=":
                self.advance() # Eat the equal sign...
                value = self.advance().value
                obj = DeclaratorLayout(name, value=value)
                decls.append(obj)
                # Now check for the comma or paranthesis
                if self.peek().value == ",":
                    self.advance()
                    continue
                elif self.peek().value == ")": # Close???
                    # We are done so just break out of the thing...
                    self.advance()
                    break
            elif self.peek().value == ",": # Layouts that do not require a value... (for example "std140" and others...)
                # Just consume the comma and generate the DeclaratorLayout object...
                obj = DeclaratorLayout(name)
                decls.append(obj)
                self.advance() # Eat the comma such that we are on the next (potential) qualifier
            elif self.peek().value == ")": # End of the thing???
                obj = DeclaratorLayout(name)
                decls.append(obj)
                self.advance()
                break
        # Show where we breaked...
        print("self.peek(): "+str(self.peek().kind)+", "+str(self.peek().value))
        # Now we assume that all the qualifiers are in the list "decls" . Create the actual layout object...
        layout_object = LayoutQualifier(decls)
        return layout_object

    def parse_translation_unit(self) -> TranslationUnit:
        items: List[TopLevel] = []
        while self.peek().kind != "EOF":
            t = self.peek()
            print("t.value: "+str(t.value))
            print("t.kind: "+str(t.kind))
            # if t.kind == "KW" and t.value == "struct":

            # Try to parse layouts first...
            if t.value == "layout" and t.kind == "KW": # layout?
                items.append(self.parse_layout())
                continue

            if self._looks_like_struct_decl_stmt():
                items.append(self.parse_struct_toplevel_decl())
                continue

            if t.value in ("uniform", "in", "out", "buffer") and self._looks_like_interface_block():
                items.append(self.parse_interface_block())
                continue

            if self._looks_like_decl():
                '''
                save = self.i
                _ = self.parse_type_name()
                _ = self.expect("ID")
                if self.peek().kind == "(":
                    self.i = save
                    # print("Function definition...")
                    items.append(self.parse_function_def_or_decl())
                else:
                    # print("Function definition...")
                    self.i = save
                    items.append(self.parse_global_decl())
                '''

                save = self.i

                # Parse return type
                _ = self.parse_type_name()

                # skip array dimensions on return type
                while self.match("["):
                    if not self.match("]"):
                        self.parse_expr(0)
                        self.expect("]")

                # Now expect function / variable name
                _ = self.expect("ID")

                if self.peek().kind == "(":
                    self.i = save
                    items.append(self.parse_function_def_or_decl())
                else:
                    self.i = save
                    items.append(self.parse_global_decl())

                continue
            # print("Ignoring this stuff here: "+str(self.peek().kind)+" , "+str(self.peek().value))
            self.advance()

        return TranslationUnit(items)

'''
def parse_to_tree(shader_source: str) -> TranslationUnit:
    if DEBUG:
        global current_input
        current_input = shader_source
    tokens = lex(shader_source)
    p = Parser(tokens)
    return p.parse_translation_unit()
'''

def parse_directive(line: str):
    parts = line.split()
    if parts[0] == "#version":
        # return VersionDirective(parts[1]) # Doesn't work for example "#version 300 es" has two string parts after the "#version" token...
        return VersionDirective(" ".join(parts[1:]))
    if parts[0] == "#extension":
        # "#extension GL_EXT_YUV_target : require"
        name = parts[1]
        behavior = parts[-1]
        return ExtensionDirective(name, behavior)
    if parts[0] == "#pragma": # Pragma directives too...
        pragma_string = " ".join(parts[1:])
        return PragmaDirective(pragma_string)
    return None

# This here also supports the directives...
def parse_to_tree(shader_source: str) -> TranslationUnit:
    if DEBUG:
        global current_input
        current_input = shader_source

    lines = shader_source.splitlines()
    directives = []
    body_lines = []

    for line in lines:
        s = line.strip()
        if s.startswith("#version"):
            directives.append(("version", s))
        elif s.startswith("#extension"):
            directives.append(("extension", s))
        elif s.startswith("#pragma"):
            directives.append(("pragma", s))
        else:
            body_lines.append(line)

    tokens = lex("\n".join(body_lines))
    p = Parser(tokens)
    print("tokens: "+str(tokens))
    tu = p.parse_translation_unit()

    # tu.directives = directives
    tu.directives = [parse_directive(s) for _, s in directives]

    return tu
