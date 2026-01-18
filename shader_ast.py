from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

# --- Types ---

@dataclass
class TypeName:
    name: str
    precision: Optional[str] = None
    qualifiers: List[str] = None

    # This is basically for the function definitions which return arrays...

    array_dims: List[Optional[Expr]] = None

    def __post_init__(self):
        if self.qualifiers is None:
            self.qualifiers = []


# --- Expressions ---

class Expr: ...

@dataclass
class Identifier(Expr):
    name: str

@dataclass
class IntLiteral(Expr):
    value: int

@dataclass
class FloatLiteral(Expr):
    value: float

@dataclass
class BoolLiteral(Expr):
    value: bool

@dataclass
class UnaryExpr(Expr):
    op: str
    operand: Expr
    postfix: bool = False

@dataclass
class BinaryExpr(Expr):
    op: str
    left: Expr
    right: Expr

@dataclass
class TernaryExpr(Expr):
    cond: Expr
    then_expr: Expr
    else_expr: Expr

@dataclass
class CallExpr(Expr):
    callee: Expr
    args: List[Expr]

@dataclass
class IndexExpr(Expr):
    base: Expr
    index: Expr

@dataclass
class MemberExpr(Expr):
    base: Expr
    member: str


# --- Decls / Struct ---

@dataclass
class StructField:
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None

@dataclass
class StructType:
    name: Optional[str]
    members: List[StructField]

'''
@dataclass
class Declarator:
    name: str
    base_type: object
    array_size: Optional[Expr] = None
    init: Optional[Expr] = None
'''

'''
@dataclass
class Declarator:
    name: str
    base_type: object
    array_size: Optional[Expr] = None
    init: Optional[Expr] = None
    storage: Optional[str] = None   # 👈 ADD THIS
'''

class DeclaratorLayout:
    def __init__(self, name)

class Declarator:
    def __init__(self, name, base_type, array_size, init, qualifiers=None):
        self.name = name
        self.base_type = base_type
        self.array_size = array_size
        self.init = init
        self.qualifiers = qualifiers or []
    def __str__(self):
        # Print as string...
        out_str = "Declarator("+", ".join([str(self.name), str(self.base_type), str(self.array_size), str(self.init), str(self.qualifiers)])+")"
        return out_str

@dataclass
class VarDecl:
    type_name: TypeName
    name: str
    # array_size: Optional[Expr] = None
    array_dims: List[Optional[Expr]]
    init: Optional[Expr] = None


# --- Statements ---

class Stmt: ...

@dataclass
class EmptyStmt(Stmt): ...

@dataclass
class ExprStmt(Stmt):
    expr: Expr

@dataclass
class DeclStmt(Stmt):
    decls: List[VarDecl]

@dataclass
class BlockStmt(Stmt):
    stmts: List[Stmt]

@dataclass
class IfStmt(Stmt):
    cond: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt] = None

@dataclass
class WhileStmt(Stmt):
    cond: Expr
    body: Stmt

@dataclass
class DoWhileStmt(Stmt):
    body: Stmt
    cond: Expr

@dataclass
class ForStmt(Stmt):
    init: Optional[Stmt]
    cond: Optional[Expr]
    loop: Optional[Expr]
    body: Stmt

@dataclass
class ReturnStmt(Stmt):
    expr: Optional[Expr]

@dataclass
class BreakStmt(Stmt): ...

@dataclass
class ContinueStmt(Stmt): ...

@dataclass
class DiscardStmt(Stmt): ...


# --- Switch Statement ---

class SwitchStmt(Stmt):
    def __init__(self, expr: Expr, body: BlockStmt):
        self.expr = expr
        self.body = body


class CaseStmt(Stmt):
    def __init__(self, expr: Expr, stmts: list[Stmt]):
        self.expr = expr
        self.stmts = stmts


class DefaultStmt(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

# --- Top level ---

class TopLevel: ...

@dataclass
class StructDecl:
    struct_type: StructType
    declarators: List[Declarator]   # may be empty

@dataclass
class StructDef(TopLevel):
    name: str
    fields: List[StructField]

@dataclass
class FunctionParam:
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None

# This is for function definitions without a body...
@dataclass
class FunctionDecl:
    return_type: TypeName
    name: str
    params: List[FunctionParam]

@dataclass
class FunctionDef(TopLevel):
    return_type: TypeName
    name: str
    params: List[FunctionParam]
    body: BlockStmt

@dataclass
class GlobalDecl(TopLevel):
    decls: List[VarDecl]

# This is a special case, since this is a toplevel expression that doesn't end in a newline...
@dataclass
class LayoutQualifier(TopLevel):
    declarators: List[Declarator]

# This is the "struct specifier + declarators" case:
@dataclass
class Declaration(TopLevel):
    type: object               # can be StructType or other
    declarators: List[Declarator]

# This next class is used for the more complex struct blocks like:   buffer buffer_block { float w; };

class InterfaceBlock(TopLevel):
    def __init__(self, storage, name, members, instance, array_dims):
        self.storage = storage
        self.name = name
        self.members = members
        self.instance = instance
        # array_dims: List[Optional[Expr]]
        self.array_dims = array_dims

# Directives (version and extensions...)
class VersionDirective:
    def __init__(self, version: str):
        self.version = version

class ExtensionDirective:
    def __init__(self, name: str, behavior: str):
        self.name = name
        self.behavior = behavior

class PragmaDirective:
    def __init__(self, pragma_string: str):
        self.pragma_string = pragma_string
        # self.behavior = behavior

@dataclass
class TranslationUnit:
    items: List[TopLevel]
    # directives: List[str] # These are the directives shit here...
