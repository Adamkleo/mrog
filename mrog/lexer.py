import re

from .symbols import TRIG_FUNCTIONS
from .token import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the 'pos' pointer and set 'current_char'."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        """Peek at the next character without advancing the pointer."""
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a number token."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        return Token(TokenType.NUMBER, float(result))

    def identifier_or_function(self):
        """Handle identifiers, trigonometric functions, and variables."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result in TRIG_FUNCTIONS:
            return Token(TokenType.TRIG_FUNCTION, result)
        elif result == 'exp':
            return Token(TokenType.EXPONENTIAL, result)
        elif self.current_char == '(':
            return Token(TokenType.FUNCTION, result)
        else:
            return Token(TokenType.VARIABLE, result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier_or_function()
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/')
            
            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POW, '^')
            
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQUAL, '=')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            
            if self.current_char == '#':
                self.advance()
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            self.error()

        return Token(TokenType.EOF, None)

