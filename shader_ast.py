# shader_ast.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union


# -----------------
# Base nodes
# -----------------

class Node:
    pass


class Expr(Node):
    pass


class Stmt(Node):
    pass


class TopLevel(Node):
    pass


# -----------------
# Expressions
# -----------------

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
    postfix: bool = False  # True for x++/x--


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
    member: str  # field or swizzle


# -----------------
# Types / Decls (simple)
# -----------------

@dataclass
class TypeName(Node):
    name: str
    precision: Optional[str] = None  # lowp/mediump/highp
    qualifiers: List[str] = field(default_factory=list)  # const, in, out, uniform, etc.


@dataclass
class VarDecl(Node):
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None
    init: Optional[Expr] = None


# -----------------
# Statements
# -----------------

@dataclass
class EmptyStmt(Stmt):
    pass


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
    init: Optional[Union[DeclStmt, ExprStmt]]  # GLSL allows decl or expr or empty
    cond: Optional[Expr]
    loop: Optional[Expr]
    body: Stmt


@dataclass
class ReturnStmt(Stmt):
    expr: Optional[Expr] = None


@dataclass
class BreakStmt(Stmt):
    pass


@dataclass
class ContinueStmt(Stmt):
    pass


@dataclass
class DiscardStmt(Stmt):
    pass


# -----------------
# Top-level constructs
# -----------------

@dataclass
class StructField(Node):
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None


@dataclass
class StructDef(TopLevel):
    name: str
    fields: List[StructField]

@dataclass
class StructDecl:
    struct_type: StructType
    declarators: List[Declarator]   # may be empty

@dataclass
class FunctionParam(Node):
    type_name: TypeName
    name: str
    array_size: Optional[Expr] = None


@dataclass
class FunctionDef(TopLevel):
    return_type: TypeName
    name: str
    params: List[FunctionParam]
    body: BlockStmt  # for prototype, can be empty block or None if you want


@dataclass
class GlobalDecl(TopLevel):
    decls: List[VarDecl]


@dataclass
class TranslationUnit(Node):
    items: List[TopLevel]