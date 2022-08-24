from decimal import Decimal
from typing import Any

from .environment import Environment
from .expressions import Assign, Binary, Expr, Grouping, Literal, Logical, Unary, Variable
from .statements import Block, If, Expression, Print, Stmt, Var, While
from .token import Token, TokenType
from .visitor import Visitor


class Interpreter(Visitor):

    def __init__(self, error_reporter):
        self.environment = Environment()
        self.error_reporter = error_reporter

    def interpret(self, statements: list[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as err:
            self.error_reporter(err)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

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

    def visit_If(self, stmt: If):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_Expression(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_Print(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(Literal(value))

    def visit_Var(self, stmt: Var):
        value = self.evaluate(stmt.initializer) if stmt.initializer is not None else None
        self.environment.define(stmt.name.lexeme, value)

    def visit_While(self, stmt: While):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)

    def visit_Assign(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
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
                    raise RuntimeError('Division by zero.', operator)
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
        return self.environment.get(expr.name)

    def check_number_operands(self, operator: Token, *operands: Any):
        if not all(isinstance(o, Decimal) for o in operands):
            raise RuntimeError('Operands must be numbers.', operator)

    def check_number_or_string_operands(self, operator: Token, *operands: Any):
        if all(isinstance(o, Decimal) for o in operands):
            return
        if all(isinstance(o, str) for o in operands):
            return
        raise RuntimeError('Operands must be two numbers or two strings.', operator)
