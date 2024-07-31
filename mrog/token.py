from enum import Enum, auto

class TokenType(Enum):
    TRIG_FUNCTION = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    EQUAL = auto()

    SQRT = auto()
    ABS = auto()
    LOG = auto()
    LN = auto()
    EXPONENTIAL = auto()

    FACTORIAL = auto()

    IDENTIFIER = auto()
    NUMBER = auto()
    
    LPAREN = auto()  # Left Parenthesis '('
    RPAREN = auto()  # Right Parenthesis ')'
    
    EOF = auto()     # End of File

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

