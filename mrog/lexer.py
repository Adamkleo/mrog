import re

from .symbols import TRIG_FUNCTIONS
from .token import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.symbols = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MUL,
            '/': TokenType.DIV,
            '^': TokenType.POW,
            '=': TokenType.EQUAL,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN
        }

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
    
    def variable(self):
        token_type = TokenType.VARIABLE
        char = self.current_char
        self.advance()
        return Token(token_type, char)
    
    def symbol(self):
        token_type = self.symbols[self.current_char]
        char = self.current_char
        self.advance()
        return Token(token_type, char)

    def alpha(self):
        """Handle identifiers, trigonometric functions, and variables."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        
        if result in TRIG_FUNCTIONS:
            return Token(TokenType.TRIG_FUNCTION, result)
        elif result == 'exp':
            return Token(TokenType.EXPONENTIAL, result)
        else:
            return Token(TokenType.IDENTIFIER, result)
        
        


    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.alpha()

            if self.current_char in self.symbols:
                return self.symbol()
            
            if self.current_char == '#':
                self.advance()
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            self.error()

        return Token(TokenType.EOF, None)

