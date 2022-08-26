from typing import Any

from .exceptions import RunError
from .token import Token


class Environment:

    def __init__(self, enclosing: 'Environment|None' = None,
                 initial: dict[str, Any]|None = None):
        self.values: dict[str, Any] = initial or {}
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise RunError(f"Undefined variable '{name.lexeme}'.", name)

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise RunError(f"Undefined variable '{name.lexeme}'.", name)

    def get_at(self, distance: int, name: str) -> Any:
        environment = self.ancestor(distance)
        return environment.values[name]

    def assign_at(self, distance: int, name: str, value: Any):
        self.ancestor(distance).values[name] = value

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment
