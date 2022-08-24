from .expressions import Binary, Expr, Grouping, Literal, Unary
from .statements import Expression, Print, Stmt
from .visitor import Visitor


class AstPrinter(Visitor):

    def print(self, node: Expr|Stmt):
        print(self.format(node))

    def format(self, node: Expr|Stmt):
        return node.accept(self)

    def visit_Binary(self, expr: Binary):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_Unary(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_Grouping(self, expr: Grouping):
        return self._parenthesize('group', expr.expression)

    def visit_Literal(self, expr: Literal):
        return str(expr)

    def visit_Print(self, stmt: Print):
        return self._parenthesize('print', stmt.expression)

    def _parenthesize(self, name: str, *exprs: Expr | Stmt):
        parts = [name] + [e.accept(self) for e in exprs]
        return f'({" ".join(parts)})'
