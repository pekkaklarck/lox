from dataclasses import dataclass
from typing import Any

from .token import Token


@dataclass
class Expr:

    def accept(self, visitor: 'Visitor'):
        return getattr(visitor, f'visit_{type(self).__name__}')(self)


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


class Visitor:

    def visit_Binary(self, expr: Binary):
        expr.left.accept(self)
        expr.right.accept(self)

    def visit_Unary(self, expr: Unary):
        expr.right.accept(self)

    def visit_Grouping(self, expr: Grouping):
        expr.expression.accept(self)

    def visit_Literal(self, expr: Literal):
        pass
