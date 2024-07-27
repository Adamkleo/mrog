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
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        return self.parse_function_definition()

    def parse_function_definition(self):
        function_name = self.current_token.value
        self.eat(TokenType.FUNCTION)
        self.eat(TokenType.LPAREN)
        function_variable = self.current_token.value
        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.EQUAL)
        expression = self.parse_expression()
        return {'type': 'FunctionDefinition', 'name': function_name, 'variable': function_variable, 'expression': expression}

    def parse_expression(self):
        term = self.parse_term()
        return self.parse_rest_expression(term)

    def parse_rest_expression(self, initial_term):
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token
            if operator.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            next_term = self.parse_term()
            initial_term = {'type': 'BinaryExpression', 'left': initial_term, 'operator': operator.value, 'right': next_term}
        return initial_term

    def parse_term(self):
        factor = self.parse_factor()
        return self.parse_rest_term(factor)

    def parse_rest_term(self, initial_factor):
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            operator = self.current_token
            if operator.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            else:
                self.eat(TokenType.DIV)
            next_factor = self.parse_factor()
            initial_factor = {'type': 'BinaryExpression', 'left': initial_factor, 'operator': operator.value, 'right': next_factor}
        return initial_factor

    def parse_factor(self):
        primary = self.parse_primary()
        return self.parse_rest_factor(primary)

    def parse_rest_factor(self, initial_primary):
        if self.current_token.type == TokenType.POW:
            operator = self.current_token
            self.eat(TokenType.POW)
            next_primary = self.parse_primary()
            initial_primary = {'type': 'BinaryExpression', 'left': initial_primary, 'operator': operator.value, 'right': next_primary}
        return initial_primary

    def parse_primary(self):
        token = self.current_token
        if token.type == TokenType.TRIG_FUNCTION:
            self.eat(TokenType.TRIG_FUNCTION)
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return {'type': 'TrigFunction', 'function': token.value, 'expression': expr}
        elif token.type == TokenType.EXPONENTIAL:
            self.eat(TokenType.EXPONENTIAL)
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return {'type': 'ExpFunction', 'expression': expr}
        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return {'type': 'Number', 'value': token.value}
        elif token.type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
            return {'type': 'Variable', 'value': token.value}
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            self.error("Invalid primary expression")
