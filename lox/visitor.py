from .expressions import Binary, Grouping, Literal, Unary


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
