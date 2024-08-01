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
    

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise InvalidSyntaxError(self.current_line)


    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            self.current_line += 1
            statements.append((self.parse_statement()))
        return statements
    

    def parse_statement(self):
        """Parse a statement"""

        # Check if the statement is a function definition
        if self.current_token.type == TokenType.IDENTIFIER:
            # Create a new function object for the function being defined
            self.current_statement = Function()
            # Parse the function definition
            return self.parse_function_definition()
        
        # Check if the statement is a print statement
        if self.current_token.type == TokenType.PRINT:
            # Set the current statement type to 'print'
            self.current_statement = 'print'
            # Parse the print statement
            return self.parse_print_statement()
        
        raise InvalidSyntaxError(self.current_line)
        
    def parse_print_statement(self):
        # Allow print(f) or print(f(x)) or print(f(expression))
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)

        expression = self.parse_expression()

        self.eat(TokenType.RPAREN)
        
        return {'type': 'PrintStatement', 'expression': expression}

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
            next_primary = self.parse_rest_factor(next_primary)  # Recursively handle right-associative power
            initial_primary = {'type': 'BinaryExpression', 'left': initial_primary, 'operator': operator.value, 'right': next_primary}
        return initial_primary


    def parse_primary(self):
        token = self.current_token

        if token.type in (TokenType.EXPONENTIAL, TokenType.SQRT, TokenType.LN, TokenType.ABS, TokenType.TRIG_FUNCTION):
            return self.parse_math_function(token)
        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return self.parse_postfix({'type': 'Number', 'value': token.value})
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_identifier()
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return self.parse_postfix(expr)
        else:
            raise InvalidSyntaxError(self.current_line)

    def parse_postfix(self, node):
        if self.current_token.type == TokenType.FACTORIAL:
            self.eat(TokenType.FACTORIAL)
            node = {'type': 'Factorial', 'operand': node}
        return node


    def parse_identifier(self):
        """Parse an identifier, which can be a variable or a function call."""
        
        # Get identifier
        identifier = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        derivative = False
        if self.current_token.type == TokenType.PRIME:
            derivative = True
            self.eat(TokenType.PRIME)

        # Check if it is a function call or a variable
        if self.current_token.type == TokenType.LPAREN:

            # Parse opening parenthesis of function call
            self.eat(TokenType.LPAREN)
            # Get function call argument
            arg = self.parse_expression()
            
            # Check if argument contains any variables that are not in the function definition, only if not in print statement
            if self.current_statement != 'print':
                non_function_variables = VARIABLES.difference(set(self.current_statement.variable))
                for var in non_function_variables:
                    if var in arg:
                        raise InvalidVariableError(var, self.current_line)
                    
            # Parse closing parenthesis of function call
            self.eat(TokenType.RPAREN)

            if derivative:
                return {'type': 'Derivative', 'function': identifier, 'argument': arg}

            # Return function call node
            return {'type': 'FunctionCall', 'name': identifier, 'argument': arg}
        else:

            # Check if variable is valid (x, y, z)
            if identifier not in VARIABLES:
                raise InvalidVariableError(identifier, self.current_line)
            
            # Check if variable is the same as the function variable in which it is used, only if not in print statement
            if self.current_statement != 'print' and identifier != self.current_statement.variable:
                raise InvalidExpressionVariableError(identifier, self.current_line)
            
            if self.current_token.type == TokenType.FACTORIAL:
                self.parse_postfix(identifier)

            # Return variable node
            return {'type': 'Variable', 'value': identifier}

        

    def parse_math_function(self, token):
        self.eat(token.type)
        self.eat(TokenType.LPAREN)
        expr = self.parse_expression()
        self.eat(TokenType.RPAREN)
        return {'type': token.value, 'expression': expr}
