from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

# --- Types ---

@dataclass
class TypeName:
    name: str
    precision: Optional[str] = None
    qualifiers: List[str] = None

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


@dataclass
class Declarator:
    name: str
    base_type: object
    array_size: Optional[Expr] = None
    init: Optional[Expr] = None

@dataclass
class VarDecl:
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None
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

@dataclass
class FunctionDef(TopLevel):
    return_type: TypeName
    name: str
    params: List[FunctionParam]
    body: BlockStmt

@dataclass
class GlobalDecl(TopLevel):
    decls: List[VarDecl]

# This is the "struct specifier + declarators" case:
@dataclass
class Declaration(TopLevel):
    type: object               # can be StructType or other
    declarators: List[Declarator]

@dataclass
class TranslationUnit:
    items: List[TopLevel]