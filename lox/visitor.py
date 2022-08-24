from .expressions import Assign, Binary, Grouping, Literal, Unary, Variable
from .statements import Block, Expression, Print, Var


class Visitor:

    def visit_Block(self, stmt: Block):
        for st in stmt.statements:
            st.accept(self)

    def visit_Expression(self, stmt: Expression):
        stmt.expression.accept(self)

    def visit_Print(self, stmt: Print):
        stmt.expression.accept(self)

    def visit_Var(self, stmt: Var):
        if stmt.initializer is not None:
            stmt.initializer.accept(self)

    def visit_Assign(self, expr: Assign):
        expr.value.accept(self)

    def visit_Binary(self, expr: Binary):
        expr.left.accept(self)
        expr.right.accept(self)

    def visit_Unary(self, expr: Unary):
        expr.right.accept(self)

    def visit_Grouping(self, expr: Grouping):
        expr.expression.accept(self)

    def visit_Variable(self, expr: Variable):
        pass

    def visit_Literal(self, expr: Literal):
        pass
