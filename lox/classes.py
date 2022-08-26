from typing import Any, TYPE_CHECKING

from .exceptions import RunError
from .functions import Callable, LoxFunction
from .token import Token

if TYPE_CHECKING:
    from .interpreter import Interpreter


class LoxClass(Callable):

    def __init__(self, name: str, superclass: 'LoxClass|None',
                 methods: dict[str, LoxFunction]):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    @property
    def arity(self) -> int:
        initializer = self.find_method('init')
        return initializer.arity if initializer is not None else 0

    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> Any:
        instance = LoxInstance(self)
        initializer = self.find_method('init')
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name: str):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.find_method(name)
        return None

    def __str__(self):
        return f'<cls {self.name}>'


class LoxInstance:

    def __init__(self, klass: LoxClass):
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        raise RunError(f"Undefined property '{name.lexeme}'.", name)

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f'<{self.klass.name} instance>'
