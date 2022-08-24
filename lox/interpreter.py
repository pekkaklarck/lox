from decimal import Decimal
from typing import Any

from .expressions import Binary, Expr, Grouping, Literal, Unary
from .token import Token, TokenType
from .visitor import Visitor


class Interpreter(Visitor):

    def __init__(self, error_reporter):
        self.error_reporter = error_reporter

    def interpret(self, expression: Expr):
        try:
            value = self.evaluate(expression)
        except RuntimeError as err:
            self.error_reporter(err)
        else:
            print(self.stringify(value))

    def visit_Literal(self, expr: Literal):
        return expr.value

    def visit_Grouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_Unary(self, expr: Unary):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.is_truthy(right)

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

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def check_number_operands(self, operator: Token, *operands: Any):
        if not all(isinstance(o, Decimal) for o in operands):
            raise RuntimeError('Operands must be numbers.', operator)

    def check_number_or_string_operands(self, operator: Token, *operands: Any):
        if all(isinstance(o, Decimal) for o in operands):
            return
        if all(isinstance(o, str) for o in operands):
            return
        raise RuntimeError('Operands must be two numbers or two strings.', operator)

    def is_truthy(self, value):
        return value is not None and value is not False

    def stringify(self, value: Any):
        if value is None:
            return 'nil'
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, Decimal):
            return str(value)
        return value
