from dataclasses import dataclass

from .expressions import Expr
from .token import Token


@dataclass(eq=False)
class Stmt:

    def accept(self, visitor):
        return visitor.visit(self)


@dataclass(eq=False)
class Block(Stmt):
    statements: list[Stmt]


@dataclass(eq=False)
class Break(Stmt):
    keyword: Token    # For error reporting purposes.


@dataclass(eq=False)
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]


@dataclass(eq=False)
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt|None


@dataclass(eq=False)
class Expression(Stmt):
    expression: Expr


@dataclass(eq=False)
class Print(Stmt):
    expression: Expr


@dataclass(eq=False)
class Return(Stmt):
    keyword: Token    # For error reporting.
    value: Expr|None


@dataclass(eq=False)
class Var(Stmt):
    name: Token
    initializer: Expr|None


@dataclass(eq=False)
class While(Stmt):
    condition: Expr
    body: Stmt
