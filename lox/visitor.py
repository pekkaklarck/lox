from .expressions import (Assign, Binary, Call, Expr, Get, Grouping, Literal, Logical,
                          Set, Super, This, Unary, Variable)
from .statements import (Block, Break, Class, Expression, Function, If, Print, Return,
                         Stmt, Var, While)


class Visitor:
    """Visitor base class.

    Overriding `visit_Node` methods stops visiting child nodes unless the
    superclass method is explicitly called. Alternatively it is possible to
    implement `start_Node/end_Node` methods that are called before and after
    visiting child nodes, respectively. Their default implementations do
    nothing.
    """

    def visit(self, node: Stmt|Expr):
        return getattr(self, f'visit_{type(node).__name__}')(node)

    def visit_Block(self, stmt: Block):
        self.start_Block(stmt)
        for st in stmt.statements:
            st.accept(self)
        self.end_Block(stmt)

    def start_Block(self, stmt: Block):
        pass

    def end_Block(self, stmt: Block):
        pass

    def visit_Break(self, stmt: Break):
        self.start_Break(stmt)
        self.end_Break(stmt)

    def start_Break(self, stmt: Break):
        pass

    def end_Break(self, stmt: Break):
        pass

    def visit_Class(self, stmt: Class):
        self.start_Class(stmt)
        if stmt.superclass is not None:
            stmt.superclass.accept(self)
        for method in stmt.methods:
            method.accept(self)
        self.end_Class(stmt)

    def start_Class(self, stmt: Class):
        pass

    def end_Class(self, stmt: Class):
        pass

    def visit_Expression(self, stmt: Expression):
        self.start_Expression(stmt)
        stmt.expression.accept(self)
        self.end_Expression(stmt)

    def start_Expression(self, stmt: Expression):
        pass

    def end_Expression(self, stmt: Expression):
        pass

    def visit_Function(self, stmt: Function):
        self.start_Function(stmt)
        for st in stmt.body:
            st.accept(self)
        self.end_Function(stmt)

    def start_Function(self, stmt: Function):
        pass

    def end_Function(self, stmt: Function):
        pass

    def visit_If(self, stmt: If):
        self.start_If(stmt)
        stmt.condition.accept(self)
        stmt.then_branch.accept(self)
        if stmt.else_branch is not None:
            stmt.else_branch.accept(self)
        self.end_If(stmt)

    def start_If(self, stmt: If):
        pass

    def end_If(self, stmt: If):
        pass

    def visit_Print(self, stmt: Print):
        self.start_Print(stmt)
        stmt.expression.accept(self)
        self.end_Print(stmt)

    def start_Print(self, stmt: Print):
        pass

    def end_Print(self, stmt: Print):
        pass

    def visit_Return(self, stmt: Return):
        self.start_Return(stmt)
        if stmt.value is not None:
            stmt.value.accept(self)
        self.end_Return(stmt)

    def start_Return(self, stmt: Return):
        pass

    def end_Return(self, stmt: Return):
        pass

    def visit_Var(self, stmt: Var):
        self.start_Var(stmt)
        if stmt.initializer is not None:
            stmt.initializer.accept(self)
        self.end_Var(stmt)

    def start_Var(self, stmt: Var):
        pass

    def end_Var(self, stmt: Var):
        pass

    def visit_While(self, stmt: While):
        self.start_While(stmt)
        stmt.condition.accept(self)
        stmt.body.accept(self)
        self.end_While(stmt)

    def start_While(self, stmt: While):
        pass

    def end_While(self, stmt: While):
        pass

    def visit_Assign(self, expr: Assign):
        self.start_Assign(expr)
        expr.value.accept(self)
        self.end_Assign(expr)

    def start_Assign(self, expr: Assign):
        pass

    def end_Assign(self, expr: Assign):
        pass

    def visit_Binary(self, expr: Binary):
        self.start_Binary(expr)
        expr.left.accept(self)
        expr.right.accept(self)
        self.end_Binary(expr)

    def start_Binary(self, expr: Binary):
        pass

    def end_Binary(self, expr: Binary):
        pass

    def visit_Call(self, expr: Call):
        self.start_Call(expr)
        expr.callee.accept(self)
        for arg in expr.arguments:
            arg.accept(self)
        self.end_Call(expr)

    def start_Call(self, expr: Call):
        pass

    def end_Call(self, expr: Call):
        pass

    def visit_Get(self, expr: Get):
        self.start_Get(expr)
        expr.object.accept(self)
        self.end_Get(expr)

    def start_Get(self, expr: Get):
        pass

    def end_Get(self, expr: Get):
        pass

    def visit_Grouping(self, expr: Grouping):
        self.start_Grouping(expr)
        expr.expression.accept(self)
        self.end_Grouping(expr)

    def start_Grouping(self, expr: Grouping):
        pass

    def end_Grouping(self, expr: Grouping):
        pass

    def visit_Literal(self, expr: Literal):
        self.start_Literal(expr)
        self.end_Literal(expr)

    def start_Literal(self, expr: Literal):
        pass

    def end_Literal(self, expr: Literal):
        pass

    def visit_Logical(self, expr: Logical):
        self.start_Logical(expr)
        expr.left.accept(self)
        expr.right.accept(self)
        self.end_Logical(expr)

    def start_Logical(self, expr: Logical):
        pass

    def end_Logical(self, expr: Logical):
        pass

    def visit_Unary(self, expr: Unary):
        self.start_Unary(expr)
        expr.right.accept(self)
        self.end_Unary(expr)

    def start_Unary(self, expr: Unary):
        pass

    def end_Unary(self, expr: Unary):
        pass

    def visit_Set(self, expr: Set):
        self.start_Set(expr)
        expr.object.accept(self)
        expr.value.accept(self)
        self.end_Set(expr)

    def start_Set(self, expr: Set):
        pass

    def end_Set(self, expr: Set):
        pass

    def visit_Super(self, expr: Super):
        self.start_Super(expr)
        self.end_Super(expr)

    def start_Super(self, expr: Super):
        pass

    def end_Super(self, expr: Super):
        pass

    def visit_This(self, expr: This):
        self.start_This(expr)
        self.end_This(expr)

    def start_This(self, expr: This):
        pass

    def end_This(self, expr: This):
        pass

    def visit_Variable(self, expr: Variable):
        self.start_Variable(expr)
        self.end_Variable(expr)

    def start_Variable(self, expr: Variable):
        pass

    def end_Variable(self, expr: Variable):
        pass
