from .token import TokenType

TRIG_FUNCTIONS = {
    'sin', 'cos', 'tan', 'csc', 'sec', 'cot',  # basic trigonometric functions
    'sinh', 'cosh', 'tanh', 'csch', 'sech', 'coth',  # hyperbolic functions
    'asin', 'acos', 'atan', 'acsc', 'asec', 'acot',  # inverse trigonometric functions
    'asinh', 'acosh', 'atanh', 'acsch', 'asech', 'acoth'  # inverse hyperbolic functions
}

VARIABLES = {'x', 'y', 'z'}


SYMBOLS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MUL,
    '/': TokenType.DIV,
    '^': TokenType.POW,
    '=': TokenType.EQUAL,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '!': TokenType.FACTORIAL,
    "'": TokenType.PRIME
}

MATH_FUNCTIONS = {
    'exp': TokenType.EXPONENTIAL,
    'sqrt': TokenType.SQRT,
    'log': TokenType.LOG,
    'ln': TokenType.LN,
    'abs': TokenType.ABS
}


BUILTIN_FUNCTIONS = {
    'print': TokenType.PRINT
}