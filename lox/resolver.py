from typing import Callable

from .expressions import Assign, Expr, Super, This, Variable
from .interpreter import Interpreter
from .statements import Block, Break, Class, Function, Return, Stmt, Var, While
from .token import Token
from .visitor import Visitor


class Resolver(Visitor):

    def __init__(self, interpreter: Interpreter,
                 error_reporter: Callable[[Token, str], None]):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.classes: list[Class] = []
        self.functions: list[Function] = []
        self.loops = 0
        self.error_reporter = error_reporter

    def resolve(self, statements: list[Stmt]):
        for stmt in statements:
            stmt.accept(self)

    def start_Block(self, stmt: Block):
        self.begin_scope()

    def end_Block(self, stmt: Block):
        self.end_scope()

    def start_Var(self, stmt: Var):
        self.declare(stmt.name)

    def end_Var(self, stmt: Var):
        self.define(stmt.name)

    def visit_Variable(self, expr: Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            self.error_reporter(expr.name,
                                'Cannot read local variable in its own initializer.')
        self.resolve_local(expr, expr.name)

    def end_Assign(self, expr: Assign):
        self.resolve_local(expr, expr.name)

    def start_Function(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.functions.append(stmt)
        self.begin_scope()
        self.resolve_function(stmt)

    def end_Function(self, stmt: Function):
        self.end_scope()
        self.functions.pop()

    def start_Class(self, stmt: Class):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.classes.append(stmt)
        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                self.error_reporter(stmt.superclass.name,
                                    'Class cannot inherit from itself.')
            self.begin_scope()
            self.scopes[-1]['super'] = True
        self.begin_scope()
        self.scopes[-1]['this'] = True

    def end_Class(self, stmt: Class):
        self.end_scope()
        if stmt.superclass is not None:
            self.end_scope()
        self.classes.pop()

    def start_Super(self, expr: Super):
        if not self.classes:
            self.error_reporter(expr.keyword, "Cannot use 'super' outside class.")
        elif not self.classes[-1].superclass:
            self.error_reporter(expr.keyword, "Cannot use 'super' in a class "
                                              "with no superclass.")
        self.resolve_local(expr, expr.keyword)

    def start_This(self, expr: This):
        if self.classes:
            self.resolve_local(expr, expr.keyword)
        else:
            self.error_reporter(expr.keyword, "Cannot use 'this' outside method.")

    def start_While(self, stmt: While):
        self.loops += 1

    def end_While(self, stmt: While):
        self.loops -= 1

    def start_Return(self, stmt: Return):
        if not self.functions:
            self.error_reporter(stmt.keyword, 'Cannot return from top-level code.')
        elif self.functions[-1].is_init and stmt.value is not None:
            self.error_reporter(stmt.keyword, "Cannot return value from 'init'.")

    def start_Break(self, stmt: Break):
        if not self.loops:
            self.error_reporter(stmt.keyword, "Cannot use 'break' outside loop.")

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if self.scopes:
            scope = self.scopes[-1]
            if name.lexeme in scope:
                self.error_reporter(name, f"A variable with name '{name.lexeme}' "
                                          f"exists in this scope already.")
            scope[name.lexeme] = False

    def define(self, name: Token):
        if self.scopes:
            self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for depth, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, depth)
                return

    def resolve_function(self, function: Function):
        for param in function.params:
            self.declare(param)
            self.define(param)
