import typing

from .expressions import (Assign, Binary, Call, Get, Grouping, Expr, Literal, Logical,
                          Set, Super, This, Unary, Variable)
from .statements import (Block, Break, Class, Expression, Function, If, Print, Return,
                         Stmt, Var, While)
from .token import Token, TokenType


class ParseError(Exception):
    pass


class Parser:

    def __init__(self, tokens: list[Token],
                 error_reporter: typing.Callable[[Token, str], None]):
        self.tokens = tokens
        self.current = 0
        self.error_reporter = error_reporter

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def declaration(self) -> Stmt|None:
        try:
            if self.match(TokenType.FUN):
                return self.function('function')
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def function(self, kind: typing.Literal['function', 'method']) -> Function:
        name = self.consume(TokenType.IDENTIFIER, f'Expect {kind} name.')
        parameters: list[Token] = []
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        if not self.check(TokenType.RIGHT_PAREN):
            while not parameters or self.match(TokenType.COMMA):
                param = self.consume(TokenType.IDENTIFIER, 'Expect parameter name')
                parameters.append(param)
        if len(parameters) > 255:
            self.error(self.peek(), 'Cannot have more than 255 parameters.')
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        return Function(name, parameters, self.block(), kind)

    def class_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, 'Expect class name.')
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, 'Expect superclass name.')
            superclass = Variable(self.previous())
        else:
            superclass = None
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods: list[Function] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function('method'))
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return Class(name, superclass, methods)

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = self.expression() if self.match(TokenType.EQUAL) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def expression_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(value)

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        then_branch = self.statement()
        else_branch = self.statement() if self.match(TokenType.ELSE) else None
        return If(condition, then_branch, else_branch)

    def for_statement(self) -> Stmt:
        # Desugaring!
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        if self.check(TokenType.SEMICOLON):
            condition: Expr = Literal(True)
        else:
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        if self.check(TokenType.RIGHT_PAREN):
            increment = None
        else:
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        if increment is not None:
            body = Block([body, Expression(increment)])
        loop = While(condition, body)
        return loop if initializer is None else Block([initializer, loop])

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = self.expression() if not self.check(TokenType.SEMICOLON) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def break_statement(self) -> Stmt:
        keyword = self.previous()
        self.consume(TokenType.SEMICOLON, "Expect ';' after break.")
        return Break(keyword)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return While(condition, body)

    def block(self) -> list[Stmt]:
        statements = []
        while not (self.is_at_end() or self.check(TokenType.RIGHT_BRACE)):
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.or_()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)
            self.error(equals, 'Invalid assignment target.')
        return expr

    def or_(self) -> Expr:
        expr = self.and_()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)
        return expr

    def and_(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

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
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER,
                                    "Expect property name after '.'.")
                expr = Get(expr, name)
            else:
                break
        return expr

    def finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            while not arguments or self.match(TokenType.COMMA):
                arguments.append(self.expression())
        if len(arguments) > 255:
            self.error(self.peek(), 'Cannot have more than 255 arguments.')
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.THIS):
            return This(self.previous())
        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after super.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Super(keyword, method)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
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

    def check(self, expected: TokenType) -> bool:
        return self.peek().type == expected

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

    def consume(self, expected: TokenType, message: str):
        if self.check(expected):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        self.error_reporter(token, message)
        return ParseError()

    def synchronize(self):
        starts_new_stmt = {TokenType.CLASS, TokenType.FUN, TokenType.VAR,
                           TokenType.FOR, TokenType.IF, TokenType.WHILE,
                           TokenType.PRINT, TokenType.RETURN, TokenType.BREAK}
        while True:
            previous = self.advance()
            if (self.is_at_end()
                    or previous.type is TokenType.SEMICOLON
                    or self.peek().type in starts_new_stmt):
                return
