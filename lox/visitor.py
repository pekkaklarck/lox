from .expressions import Assign, Binary, Grouping, Literal, Logical, Unary, Variable
from .statements import Block, If, Expression, Print, Var, While


class Visitor:

    def visit_Block(self, stmt: Block):
        for st in stmt.statements:
            st.accept(self)

    def visit_If(self, stmt: If):
        stmt.then_branch.accept(self)
        if stmt.else_branch is not None:
            stmt.else_branch.accept(self)

    def visit_Expression(self, stmt: Expression):
        stmt.expression.accept(self)

    def visit_Print(self, stmt: Print):
        stmt.expression.accept(self)

    def visit_Var(self, stmt: Var):
        if stmt.initializer is not None:
            stmt.initializer.accept(self)

    def visit_While(self, stmt: While):
        stmt.body.accept(self)

    def visit_Assign(self, expr: Assign):
        expr.value.accept(self)

    def visit_Binary(self, expr: Binary):
        expr.left.accept(self)
        expr.right.accept(self)

    def visit_Grouping(self, expr: Grouping):
        expr.expression.accept(self)

    def visit_Literal(self, expr: Literal):
        pass

    def visit_Logical(self, expr: Logical):
        expr.left.accept(self)
        expr.right.accept(self)

    def visit_Unary(self, expr: Unary):
        expr.right.accept(self)

    def visit_Variable(self, expr: Variable):
        pass
