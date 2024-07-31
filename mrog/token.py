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

    # Standard ath Functions
    SQRT = auto()
    ABS = auto()
    LOG = auto()
    LN = auto()
    EXPONENTIAL = auto()
    TRIG_FUNCTION = auto()

    # Built-in functions
    PRINT = auto()

    # Unary operators
    FACTORIAL = auto()
    PRIME = auto()

    # Function/Variable names and numbers
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Parentheses
    LPAREN = auto()  # Left Parenthesis '('
    RPAREN = auto()  # Right Parenthesis ')'
    
    # End of File
    EOF = auto()     # End of File

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

