from dataclasses import dataclass

from .expressions import Expr
from .token import Token


@dataclass
class Stmt:

    def accept(self, visitor):
        return getattr(visitor, f'visit_{type(self).__name__}')(self)

    def __str__(self):
        from .astprinter import AstPrinter
        return AstPrinter().format(self)


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr|None


@dataclass
class Block(Stmt):
    statements: list[Stmt]
