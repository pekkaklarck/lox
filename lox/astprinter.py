from .expressions import Expr
from .statements import Stmt
from .visitor import Visitor


class AstPrinter(Visitor):

    def __init__(self):
        self.level = 0

    @property
    def indent(self):
        return self.level * 2

    def print(self, node: Expr|Stmt):
        return self.visit(node)

    def start(self, node: Stmt|Expr):
        self.output(type(node).__name__)
        self.level += 1

    def output(self, message: str):
        print(' ' * self.indent, end='')
        print(message)

    def end(self, node: Stmt|Expr):
        self.level -= 1
