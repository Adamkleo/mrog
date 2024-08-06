import re

from .symbols import TRIG_FUNCTIONS, MATH_FUNCTIONS, BUILTIN_FUNCTIONS, SYMBOLS 
from .token import Token, TokenType
from .exceptions import UnknownSymbolError

class Lexer:
    """Lexer class for tokenizing input text."""
    def __init__(self, text):
        # Input text
        self.text = text
        # Current position in the input text
        self.pos = 0
        # Current character in the input text
        self.current_char = self.text[self.pos] if self.text else None


    def error(self):
        """Raise an error if an unknown character is encountered."""
        raise UnknownSymbolError(self.current_char)
    

    def advance(self):
        """Advance the 'pos' pointer and set 'current_char'."""
        self.pos += 1
        if self.pos < len(self.text):
            # Set the current character to the next character in the input text
            self.current_char = self.text[self.pos]
        else:
            # End of input text
            self.current_char = None

    """ UNUSED CODE
    def peek(self):
        # Peek at the next character without advancing the pointer
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            # Return the next character in the input text
            return self.text[peek_pos]
        else:
            return None
    """
    
    def skip_whitespace(self):
        """Skip whitespace characters in the input text."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a number token."""
        result = ''

        # Parse the integer part of the number
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # Check if the number has a fractional part
        if self.current_char == '.':
            result += self.current_char
            self.advance()

            # Parse the fractional part of the number
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # Return the number token
        return Token(TokenType.NUMBER, float(result))
    

    def variable(self):
        """Return a variable token."""
        token_type = TokenType.VARIABLE
        char = self.current_char
        self.advance()
        return Token(token_type, char)
    
    def symbol(self):
        """Return a symbol token."""
        
        # Map the current character to its corresponding symbol in the symbol table.
        token_type = SYMBOLS[self.current_char]
        char = self.current_char
        self.advance()
        return Token(token_type, char)

    def alpha(self):
        """Handle identifiers, trigonometric functions, and variables."""
        result = ''

        # Parse the identifiers
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        
        # Check the type of identifier and return the token from the respective table
        # a trigonometric function
        if result in TRIG_FUNCTIONS:
            return Token(TokenType.TRIG_FUNCTION, result)
        # a math function
        elif result in MATH_FUNCTIONS:
            return Token(TokenType.MATH_FUNCTION, result)
        # a built-in function
        elif result in BUILTIN_FUNCTIONS:
            return Token(BUILTIN_FUNCTIONS[result], result)
        # neither of the above, so it is an identifier
        else:
            return Token(TokenType.IDENTIFIER, result)
    

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)."""

        # Loop through the input text until the end is reached
        while self.current_char is not None:
            # Skip whitespace characters
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Check if the current character is a digit
            if self.current_char.isdigit():
                return self.number()
            
            # Check if the current character is a letter
            if self.current_char.isalpha():
                return self.alpha()
            
            # Check if the current character is a symbol (operator, parenthesis, etc.)
            if self.current_char in SYMBOLS:
                return self.symbol()
            
            # Check if the current character is a variable
            if self.current_char == '#':
                self.advance()
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            self.error()
        # End of file reached, return the EOF token
        return Token(TokenType.EOF, None)

