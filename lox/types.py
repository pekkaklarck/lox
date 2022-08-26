from decimal import Decimal
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .functions import LoxFunction
    from .classes import LoxClass, LoxInstance


LoxType = Union[str, Decimal, bool, None, 'LoxFunction', 'LoxClass', 'LoxInstance']
