from decimal import Decimal
from string import ascii_letters, digits
from typing import Any, Callable

from .token import Token, TokenType


class Scanner:
    keywords = {
        'and': TokenType.AND,
        'break': TokenType.BREAK,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
    }

    def __init__(self, source: str, error_reporter: Callable):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_reporter = error_reporter

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        match char:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!' if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            case '!':
                self.add_token(TokenType.BANG)
            case '=' if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            case '=':
                self.add_token(TokenType.EQUAL)
            case '<' if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            case '<':
                self.add_token(TokenType.LESS)
            case '>' if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            case '>':
                self.add_token(TokenType.GREATER)
            case '/' if self.match('/'):
                self.comment()
            case '/':
                self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _ if self.is_digit(char):
                self.number()
            case _ if self.is_identifier_start(char):
                self.identifier()
            case _:
                self.error(f'Unexpected character {char}.')

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected: str):
        if self.peek() != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        try:
            return self.source[self.current]
        except IndexError:
            return '\x00'

    def peek_next(self):
        try:
            return self.source[self.current + 1]
        except IndexError:
            return '\x00'

    def comment(self):
        while self.peek() not in ('\n', '\x00'):
            self.advance()

    def string(self):
        while self.peek() not in ('"', '\x00'):
            if self.advance() == '\n':
                self.line += 1
        if self.is_at_end():
            self.error('Unterminated string.')
            return
        self.advance()    # Consume closing '"'.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()    # Consume '.'.
            while self.is_digit(self.peek()):
                self.advance()
        value = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, Decimal(value))

    def identifier(self):
        while self.is_identifier_body(self.peek()):
            self.advance()
        value = self.source[self.start:self.current]
        if value in self.keywords:
            self.add_token(self.keywords[value])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def is_digit(self, char):
        return char in digits

    def is_identifier_start(self, char):
        return char in ascii_letters or char == '_'

    def is_identifier_body(self, char):
        return self.is_identifier_start(char) or self.is_digit(char)

    def add_token(self, type: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def error(self, message: str):
        self.error_reporter(self.line, message)
