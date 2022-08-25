from decimal import Decimal
import time
from typing import Any

from .environment import Environment
from .exceptions import BreakControl, LoxError, ReturnControl, RunError
from .expressions import (Assign, Binary, Call, Expr, Grouping, Literal, Logical,
                          Unary, Variable)
from .functions import Callable, NativeFunction, UserFunction
from .statements import (Block, Break, Expression, Function, If, Print, Return,
                         Stmt, Var, While)
from .token import Token, TokenType
from .visitor import Visitor


class Interpreter(Visitor):

    def __init__(self, error_reporter):
        self.globals = self.environment = Environment(
            initial={'clock': NativeFunction('clock', 0, time.time),
                     'str': NativeFunction('str', 1, str)}
        )
        self.locals: dict[Expr, int] = {}
        self.error_reporter = error_reporter

    def interpret(self, statements: list[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except LoxError as err:
            self.error_reporter(err)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous, self.environment = self.environment, environment
        try:
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_Block(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_Break(self, stmt: Break):
        raise BreakControl(stmt.keyword)

    def visit_Expression(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_Function(self, stmt: Function):
        func = UserFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, func)

    def visit_If(self, stmt: If):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_Print(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(Literal(value))

    def visit_Return(self, stmt: Return):
        value = self.evaluate(stmt.value) if stmt.value is not None else None
        raise ReturnControl(value, stmt.keyword)

    def visit_Var(self, stmt: Var):
        value = self.evaluate(stmt.initializer) if stmt.initializer is not None else None
        self.environment.define(stmt.name.lexeme, value)

    def visit_While(self, stmt: While):
        while self.evaluate(stmt.condition):
            try:
                self.execute(stmt.body)
            except BreakControl:
                break

    def visit_Assign(self, expr: Assign):
        value = self.evaluate(expr.value)
        if expr in self.locals:
            distance = self.locals[expr]
            self.environment.assign_at(distance, expr.name.lexeme, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_Binary(self, expr: Binary):
        left = self.evaluate(expr.left)
        operator = expr.operator
        right = self.evaluate(expr.right)
        match operator.type:
            case TokenType.MINUS:
                self.check_number_operands(operator, left, right)
                return left - right
            case TokenType.PLUS:
                self.check_number_or_string_operands(operator, left, right)
                return left + right
            case TokenType.SLASH:
                self.check_number_operands(operator, left, right)
                if right == 0:
                    raise RunError('Division by zero.', operator)
                return left / right
            case TokenType.STAR:
                self.check_number_operands(operator, left, right)
                return left * right
            case TokenType.GREATER:
                self.check_number_operands(operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right

    def visit_Call(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        if not isinstance(callee, Callable):
            raise RunError('Can only call functions and classes.', expr.paren)
        if callee.arity != len(arguments):
            raise RunError(f'Expected {callee.arity} arguments but got '
                               f'{len(arguments)}.', expr.paren)
        return callee.call(self, arguments)

    def visit_Grouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_Literal(self, expr: Literal):
        return expr.value

    def visit_Logical(self, expr: Logical):
        left = self.evaluate(expr.left)
        type = expr.operator.type
        if type == TokenType.OR and left or type == TokenType.AND and not left:
            return left
        return self.evaluate(expr.right)

    def visit_Unary(self, expr: Unary):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not right

    def visit_Variable(self, expr: Variable):
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr):
        if expr in self.locals:
            distance = self.locals[expr]
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get(name)

    def check_number_operands(self, operator: Token, *operands: Any):
        if not all(isinstance(o, Decimal) for o in operands):
            raise RunError(f'Operands must be numbers, got {operands}.', operator)

    def check_number_or_string_operands(self, operator: Token, *operands: Any):
        if all(isinstance(o, Decimal) for o in operands):
            return
        if all(isinstance(o, str) for o in operands):
            return
        raise RunError(f'Operands must be two numbers or two strings, got {operands}.',
                       operator)
