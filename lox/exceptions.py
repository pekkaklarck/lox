from .token import Token


class LoxError(Exception):

    def __init__(self, message: str, token: Token):
        super().__init__(message)
        self.token = token

    @property
    def message(self):
        return self.args[0]


class RunError(LoxError):
    pass


class BreakControl(LoxError):

    def __init__(self, keyword: Token):
        super().__init__("'break' outside loop.", keyword)


class ReturnControl(LoxError):

    def __init__(self, value, keyword: Token):
        super().__init__("'return' outside function.", keyword)
        self.value = value
