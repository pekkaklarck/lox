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
class Block(Stmt):
    statements: list[Stmt]


@dataclass
class Break(Stmt):
    keyword: Token    # For error reporting purposes.


@dataclass
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt|None


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Return(Stmt):
    keyword: Token    # For error reporting.
    value: Expr|None


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr|None


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt
