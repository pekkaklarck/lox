from typing import Any

from .token import Token


class Environment:

    def __init__(self, enclosing=None, initial=None):
        self.values = initial or {}
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(f"Undefined variable '{name.lexeme}'.", name)

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise RuntimeError(f"Undefined variable '{name.lexeme}'.", name)
