from enum import Enum, auto

class TokenType(Enum):
    # Binary perators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    
    # Comparison operators
    EQUAL = auto()

    # Standard math Functions
    MATH_FUNCTION = auto()
    TRIG_FUNCTION = auto()

    # Built-in functions
    PRINT = auto()

    # Unary operators
    FACTORIAL = auto()
    PRIME = auto()

    # Function/Variable names and numbers
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Symbols
    LPAREN = auto()  # Left Parenthesis '('
    RPAREN = auto()  # Right Parenthesis ')'
    COMMA = auto()   # Comma ','
    LBRACKET = auto()  # Left Bracket '['
    RBRACKET = auto()  # Right Bracket ']'

    # End of File
    EOF = auto()     # End of File

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

