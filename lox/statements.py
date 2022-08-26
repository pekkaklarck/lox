from dataclasses import dataclass
from typing import Literal

from .expressions import Expr, Variable
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
class Class(Stmt):
    name: Token
    superclass: Variable|None
    methods: list['Function']


@dataclass(eq=False)
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]
    kind: Literal['function', 'method']

    @property
    def is_init(self) -> bool:
        return self.kind == 'method' and self.name.lexeme == 'init'


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
