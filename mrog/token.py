from enum import Enum, auto

class TokenType(Enum):
    FUNCTION = auto()
    TRIG_FUNCTION = auto()
    VARIABLE = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    OPERATOR = auto()
    EXPONENTIAL = auto()
    NUMBER = auto()
    EQUAL = auto()
    LPAREN = auto()  # Left Parenthesis '('
    RPAREN = auto()  # Right Parenthesis ')'
    EOF = auto()     # End of File

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"