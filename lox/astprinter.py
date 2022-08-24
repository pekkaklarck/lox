from .expressions import Binary, Expr, Grouping, Literal, Unary, Visitor


class AstPrinter(Visitor):

    def print(self, expr: Expr):
        print( expr.accept(self))

    def visit_Binary(self, expr: Binary):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_Unary(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_Grouping(self, expr: Grouping):
        return self._parenthesize('group', expr.expression)

    def visit_Literal(self, expr: Literal):
        return str(expr.value) if expr.value is not None else 'nil'

    def _parenthesize(self, name: str, *exprs: Expr):
        parts = [name] + [e.accept(self) for e in exprs]
        return f'({" ".join(parts)})'
