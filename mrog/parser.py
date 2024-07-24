from .lexer import Lexer
from .token import TokenType, Token


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, message="Syntax error"):
        raise Exception(message)

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == TokenType.FUNCTION:
            return self.function_definition()
        else:
            self.error("Invalid statement")

    def function_definition(self):
        function_name = self.current_token
        self.eat(TokenType.FUNCTION)
        self.eat(TokenType.LPAREN)
        variable = self.current_token
        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.EQUAL)
        expr = self.expression()
        return ('FUNCTION_DEFINITION', function_name, variable, expr)

    def expression(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = ('BINARY_OP', token, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = ('BINARY_OP', token, node, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            node = ('NUMBER', token)
            self.eat(TokenType.NUMBER)
            node = self.handle_implicit_multiplication(node)
            return node
        elif token.type == TokenType.LPAREN:
            node = self.parenthesis_expression()
            node = self.handle_implicit_multiplication(node)
            return node
        elif token.type == TokenType.FUNCTION:
            node = self.function_call()
            node = self.handle_implicit_multiplication(node)
            return node
        elif token.type == TokenType.VARIABLE:
            node = ('VARIABLE', token)
            self.eat(TokenType.VARIABLE)
            node = self.handle_implicit_multiplication(node)
            return node
        elif token.type == TokenType.TRIG_FUNCTION:
            node = self.trig_function()
            node = self.handle_implicit_multiplication(node)
            return node
        elif token.type == TokenType.EXPONENTIAL:
            node = self.exponential()
            node = self.handle_implicit_multiplication(node)
            return node
        else:
            self.error()

    def handle_implicit_multiplication(self, node):
        while self.current_token.type in (TokenType.NUMBER, TokenType.VARIABLE, TokenType.LPAREN, TokenType.FUNCTION, TokenType.TRIG_FUNCTION, TokenType.EXPONENTIAL):
            if self.current_token.type == TokenType.NUMBER:
                next_node = ('NUMBER', self.current_token)
                self.eat(TokenType.NUMBER)
            elif self.current_token.type == TokenType.VARIABLE:
                next_node = ('VARIABLE', self.current_token)
                self.eat(TokenType.VARIABLE)
            elif self.current_token.type == TokenType.LPAREN:
                next_node = self.parenthesis_expression()
            elif self.current_token.type == TokenType.FUNCTION:
                next_node = self.function_call()
            elif self.current_token.type == TokenType.TRIG_FUNCTION:
                next_node = self.trig_function()
            elif self.current_token.type == TokenType.EXPONENTIAL:
                next_node = self.exponential()
            node = ('BINARY_OP', Token(TokenType.MUL, '*'), node, next_node)
        return node

    def function_call(self):
        func_name = self.current_token
        self.eat(TokenType.FUNCTION)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        return ('FUNCTION_CALL', func_name, expr)

    def trig_function(self):
        token = self.current_token
        self.eat(TokenType.TRIG_FUNCTION)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        return ('TRIG_FUNCTION', token, expr)

    def exponential(self):
        token = self.current_token
        self.eat(TokenType.EXPONENTIAL)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        return ('EXPONENTIAL', token, expr)

    def parenthesis_expression(self):
        self.eat(TokenType.LPAREN)
        node = self.expression()
        self.eat(TokenType.RPAREN)
        node = self.handle_implicit_multiplication(node)
        return node
