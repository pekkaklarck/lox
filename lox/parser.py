from typing import Callable

from .expressions import Binary, Grouping, Expr, Literal, Unary
from .token import Token, TokenType


class ParseError(Exception):
    pass


class Parser:

    def __init__(self, tokens: list[Token], error_reporter: Callable):
        self.tokens = tokens
        self.current = 0
        self.error_reporter = error_reporter

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.error(self.peek(), 'Expect expression.')

    def match(self, *types: TokenType) -> bool:
        for typ in types:
            if self.check(typ):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        self.error_reporter(token, message)
        return ParseError()
