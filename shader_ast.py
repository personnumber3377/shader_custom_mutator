# shader_ast.py

from __future__ import annotations
from typing import List, Optional


class Expression:
    """Base class for all top-level shader expressions."""
    def unparse(self) -> str:
        raise NotImplementedError


class RawText(Expression):
    """Anything we don’t structurally understand."""
    def __init__(self, text: str):
        self.text = text

    def unparse(self) -> str:
        return self.text


class StructField:
    def __init__(self, type_name: str, name: str):
        self.type_name = type_name
        self.name = name

    def unparse(self) -> str:
        return f"    {self.type_name} {self.name};"


class StructDefinition(Expression):
    def __init__(self, name: str, fields: List[StructField]):
        self.name = name
        self.fields = fields

    def unparse(self) -> str:
        body = "\n".join(f.unparse() for f in self.fields)
        return f"struct {self.name} {{\n{body}\n}};\n"


class FunctionParameter:
    def __init__(self, type_name: str, name: str):
        self.type_name = type_name
        self.name = name

    def unparse(self) -> str:
        return f"{self.type_name} {self.name}"


class FunctionDefinition(Expression):
    def __init__(
        self,
        return_type: str,
        name: str,
        params: List[FunctionParameter],
        body: str,
    ):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body  # raw text inside braces

    def unparse(self) -> str:
        params = ", ".join(p.unparse() for p in self.params)
        return f"{self.return_type} {self.name}({params}) {{\n{self.body}\n}}\n"


class UniformBlock(Expression):
    def __init__(self, struct_name: str, var_name: str, body: str):
        self.struct_name = struct_name
        self.var_name = var_name
        self.body = body

    def unparse(self) -> str:
        return f"uniform struct {self.struct_name} {{\n{self.body}\n}} {self.var_name};\n"

