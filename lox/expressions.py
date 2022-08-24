from dataclasses import dataclass
from typing import Any

from .token import Token


@dataclass
class Expr:

    def accept(self, visitor):
        return getattr(visitor, f'visit_{type(self).__name__}')(self)

    def __str__(self):
        from .astprinter import AstPrinter
        return AstPrinter().format(self)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: Any
