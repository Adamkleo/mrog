from .lexer import Lexer
from .token import TokenType, Token
from .exceptions import *
from .symbols import VARIABLES
from .statement import Function

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
        self.current_line = 0
        self.current_statement = None

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
            self.current_line += 1
            statements.append((self.parse_statement()))
        return statements

    def parse_statement(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            self.current_statement = Function()
            return self.parse_function_definition()


    def parse_function_definition(self):
        function_name = self.current_token.value
        self.current_statement.name = function_name

        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        
        function_variable = self.current_token.value
        self.current_statement.variable = function_variable

        if function_variable not in VARIABLES:
            raise InvalidArgumentError(function_variable, self.current_line)
        
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.EQUAL)

        expression = self.parse_expression()
        self.current_statement.expression = expression

        return {'type': 'FunctionDefinition', 'name': function_name, 'function_variable': function_variable, 'expression': expression}

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
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_identifier()
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            self.error("Invalid primary expression")



    def parse_identifier(self):
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            arg = self.parse_expression()
            non_function_variables = VARIABLES.difference(set(self.current_statement.variable))
            for var in non_function_variables:
                if var in arg:
                    raise InvalidVariableError(var, self.current_line)
            self.eat(TokenType.RPAREN)
            return {'type': 'FunctionCall', 'name': identifier, 'argument': arg}
        else:
            if identifier not in VARIABLES:
                raise InvalidVariableError(identifier, self.current_line)
            if identifier != self.current_statement.variable:
                raise InvalidExpressionVariableError(identifier, self.current_line)
            
            return {'type': 'Variable', 'value': identifier}