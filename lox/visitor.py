from .expressions import (Assign, Binary, Call, Expr, Grouping, Literal, Logical,
                          Unary, Variable)
from .statements import (Block, Break, Expression, Function, If, Print, Return,
                         Stmt, Var, While)


class Visitor:

    def visit(self, node: Stmt|Expr):
        return getattr(self, f'visit_{type(node).__name__}')(node)

    def start(self, node: Stmt|Expr):
        pass

    def end(self, node: Stmt|Expr):
        pass

    def visit_Block(self, stmt: Block):
        self.start_Block(stmt)
        for st in stmt.statements:
            st.accept(self)
        self.end_Block(stmt)

    def start_Block(self, stmt: Block):
        self.start(stmt)

    def end_Block(self, stmt: Block):
        self.end(stmt)

    def visit_Break(self, stmt: Break):
        self.start_Break(stmt)
        self.end_Break(stmt)

    def start_Break(self, stmt: Break):
        self.start(stmt)

    def end_Break(self, stmt: Break):
        self.end(stmt)

    def visit_Expression(self, stmt: Expression):
        self.start_Expression(stmt)
        stmt.expression.accept(self)
        self.end_Expression(stmt)

    def start_Expression(self, stmt: Expression):
        self.start(stmt)

    def end_Expression(self, stmt: Expression):
        self.end(stmt)

    def visit_Function(self, stmt: Function):
        self.start_Function(stmt)
        for st in stmt.body:
            st.accept(self)
        self.end_Function(stmt)

    def start_Function(self, stmt: Function):
        self.start(stmt)

    def end_Function(self, stmt: Function):
        self.end(stmt)

    def visit_If(self, stmt: If):
        self.start_If(stmt)
        stmt.condition.accept(self)
        stmt.then_branch.accept(self)
        if stmt.else_branch is not None:
            stmt.else_branch.accept(self)
        self.end_If(stmt)

    def start_If(self, stmt: If):
        self.start(stmt)

    def end_If(self, stmt: If):
        self.end(stmt)

    def visit_Print(self, stmt: Print):
        self.start_Print(stmt)
        stmt.expression.accept(self)
        self.end_Print(stmt)

    def start_Print(self, stmt: Print):
        self.start(stmt)

    def end_Print(self, stmt: Print):
        self.end(stmt)

    def visit_Return(self, stmt: Return):
        self.start_Return(stmt)
        if stmt.value is not None:
            stmt.value.accept(self)
        self.end_Return(stmt)

    def start_Return(self, stmt: Return):
        self.start(stmt)

    def end_Return(self, stmt: Return):
        self.end(stmt)

    def visit_Var(self, stmt: Var):
        self.start_Var(stmt)
        if stmt.initializer is not None:
            stmt.initializer.accept(self)
        self.end_Var(stmt)

    def start_Var(self, stmt: Var):
        self.start(stmt)

    def end_Var(self, stmt: Var):
        self.end(stmt)

    def visit_While(self, stmt: While):
        self.start_While(stmt)
        stmt.condition.accept(self)
        stmt.body.accept(self)
        self.end_While(stmt)

    def start_While(self, stmt: While):
        self.start(stmt)

    def end_While(self, stmt: While):
        self.end(stmt)

    def visit_Assign(self, expr: Assign):
        self.start_Assign(expr)
        expr.value.accept(self)
        self.end_Assign(expr)

    def start_Assign(self, expr: Assign):
        self.start(expr)

    def end_Assign(self, expr: Assign):
        self.end(expr)

    def visit_Binary(self, expr: Binary):
        self.start_Binary(expr)
        expr.left.accept(self)
        expr.right.accept(self)
        self.end_Binary(expr)

    def start_Binary(self, expr: Binary):
        self.start(expr)

    def end_Binary(self, expr: Binary):
        self.end(expr)

    def visit_Call(self, expr: Call):
        self.start_Call(expr)
        expr.callee.accept(self)
        for arg in expr.arguments:
            arg.accept(self)
        self.end_Call(expr)

    def start_Call(self, expr: Call):
        self.start(expr)

    def end_Call(self, expr: Call):
        self.end(expr)

    def visit_Grouping(self, expr: Grouping):
        self.start_Grouping(expr)
        expr.expression.accept(self)
        self.end_Grouping(expr)

    def start_Grouping(self, expr: Grouping):
        self.start(expr)

    def end_Grouping(self, expr: Grouping):
        self.end(expr)

    def visit_Literal(self, expr: Literal):
        self.start_Literal(expr)
        self.end_Literal(expr)

    def start_Literal(self, expr: Literal):
        self.start(expr)

    def end_Literal(self, expr: Literal):
        self.end(expr)

    def visit_Logical(self, expr: Logical):
        self.start_Logical(expr)
        expr.left.accept(self)
        expr.right.accept(self)
        self.end_Logical(expr)

    def start_Logical(self, expr: Logical):
        self.start(expr)

    def end_Logical(self, expr: Logical):
        self.end(expr)

    def visit_Unary(self, expr: Unary):
        self.start_Unary(expr)
        expr.right.accept(self)
        self.end_Unary(expr)

    def start_Unary(self, expr: Unary):
        self.start(expr)

    def end_Unary(self, expr: Unary):
        self.end(expr)

    def visit_Variable(self, expr: Variable):
        self.start_Variable(expr)
        self.end_Variable(expr)

    def start_Variable(self, expr: Variable):
        self.start(expr)

    def end_Variable(self, expr: Variable):
        self.end(expr)
