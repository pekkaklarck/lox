import sys
from pathlib import Path

from .exceptions import LoxError
from .interpreter import Interpreter
from .parser import Parser
from .resolver import Resolver
from .scanner import Scanner
from .token import Token, TokenType


class Lox:

    def __init__(self):
        self.interpreter = Interpreter(self.runtime_error)
        self.error_code = 0

    def run_prompt(self):
        while True:
            try:
                line = input('> ')
            except EOFError:
                break
            else:
                self.run(line)
                self.error_code = 0
        print()

    def run_script(self, path: Path):
        self.run(path.read_text())
        if self.error_code:
            sys.exit(self.error_code)

    def run(self, source: str):
        tokens = Scanner(source, self.scan_error).scan_tokens()
        statements = Parser(tokens, self.parse_error).parse()
        Resolver(self.interpreter, self.parse_error).resolve(statements)
        if not self.error_code:
            self.interpreter.interpret(statements)

    def scan_error(self, line: int, message: str):
        self.report(message, line)

    def parse_error(self, token: Token, message: str):
        where = 'at end' if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        self.report(message, token.line, where)

    def runtime_error(self, error: LoxError):
        self.report(error.message, error.token.line, runtime_error=True)

    def report(self, message: str, line: int, where: str = '', runtime_error=False):
        if where:
            where = ' ' + where
        print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
        self.error_code = 70 if runtime_error else 65
