from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from .environment import Environment
from .exceptions import ReturnControl
from .statements import Function

if TYPE_CHECKING:
    from .classes import LoxInstance
    from .interpreter import Interpreter


class Callable(ABC):

    @property
    @abstractmethod
    def arity(self) -> int:
        ...

    @abstractmethod
    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> Any:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...


class NativeFunction(Callable):

    def __init__(self, name, arity, func):
        self.name = name
        self._arity = arity
        self.func = func

    @property
    def arity(self) -> int:
        return self._arity

    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> Any:
        return self.func(*arguments)

    def __str__(self) -> str:
        return f'<fn {self.name}>'


class LoxFunction(Callable):

    def __init__(self, declaration: Function, closure: Environment,
                 is_method: bool = False):
        self.declaration = declaration
        self.closure = closure
        self.is_method = is_method

    @property
    def is_initializer(self):
        return self.is_method and self.declaration.name.lexeme == 'init'

    @property
    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> Any:
        params = [p.lexeme for p in self.declaration.params]
        environment = Environment(self.closure, dict(zip(params, arguments)))
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnControl as ret:
            return_value = ret.value
        else:
            return_value = None
        if self.is_initializer:
            return self.closure.get_at(0, 'this')
        return return_value

    def bind(self, instance: 'LoxInstance'):
        environment = Environment(self.closure, {'this': instance})
        return LoxFunction(self.declaration, environment, is_method=True)

    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'
