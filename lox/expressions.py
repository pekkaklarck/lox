from dataclasses import dataclass
from typing import Any

from .token import Token


@dataclass(eq=False)
class Expr:

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(eq=False)
class Assign(Expr):
    name: Token
    value: Expr


@dataclass(eq=False)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass(eq=False)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]


@dataclass(eq=False)
class Get(Expr):
    object: Expr
    name: Token


@dataclass(eq=False)
class Grouping(Expr):
    expression: Expr


@dataclass(eq=False)
class Literal(Expr):
    value: Any

    def __str__(self):
        if self.value is None:
            return 'nil'
        if isinstance(self.value, bool):
            return 'true' if self.value else 'false'
        return str(self.value)

    def __bool__(self):
        return self.value is not None and self.value is not False


@dataclass(eq=False)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass(eq=False)
class Set(Expr):
    object: Expr
    name: Token
    value: Expr


@dataclass(eq=False)
class Super(Expr):
    keyword: Token
    method: Token


@dataclass(eq=False)
class This(Expr):
    keyword: Token


@dataclass(eq=False)
class Unary(Expr):
    operator: Token
    right: Expr


@dataclass(eq=False)
class Variable(Expr):
    name: Token
