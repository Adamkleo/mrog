class InvalidVariableError(Exception):
    """Raised when an invalid variable is encountered"""
    def __init__(self, variable, line, 
                 message="Invalid variable encountered"):
        self.variable = variable
        self.message = f"Error in line {line}: {message}: {variable}. Only x, y, z are allowed."
        super().__init__(self.message)

class InvalidIdentifierError(Exception):
    """Raised when an invalid identifier is encountered"""
    def __init__(self, identifier, line, 
                 message="Invalid identifier encountered"):
        self.identifier = identifier
        self.message = f"Error in line {line}: {message}: {identifier}."
        super().__init__(self.message)

class InvalidArgumentError(Exception):
    """Raised when an invalid variable is encountered"""
    def __init__(self, variable, line, 
                 message="Invalid argument encountered"):
        self.message = f"Error in line {line}: {message}: {variable}. Only x, y, z are allowed."
        super().__init__(self.message)

class InvalidExpressionVariableError(Exception):
    """Raised when an expression variable does not match its function variable."""
    def __init__(self, line, function, invalid_variable, function_variable, 
                 message="Invalid variable used in expression"):
        self.message = f"Error in line {line}: {message} [{invalid_variable}]\nVariable of function {function} is [{function_variable}]"
        super().__init__(self.message)

class InvalidSyntaxError(Exception):
    """Raised when an invalid syntax is encountered"""
    def __init__(self, line, received, expected,
                 message="Invalid syntax"):
        self.message = f"Error in line {line}: {message}. Expected {expected} but got {received}"
        super().__init__(self.message)

class UnknownSymbolError(Exception):
    """Raised when an unknown symbol is encountered"""
    def __init__(self, symbol):
        self.message = f"Unknown symbol encountered: {symbol}"
        super().__init__(self.message)

class UndefinedFunctionError(Exception):
    """Raised when an invalid function is encountered"""
    def __init__(self, line, function_name):
        self.message = f"Error in line {line}: Undefined function {function_name} used" 
        super().__init__(self.message)


class InvalidPrintArgumentError(Exception):
    """Raised when an invalid print statement is encountered"""
    def __init__(self, line, argument, arg_type, 
                 message="Invalid print statement argument:"):
        self.description = f"Expected a Function Call but got a {arg_type}."
        self.message = f"Error in line {line}: {message} {argument}\n{self.description}"
        super().__init__(self.message)






class TestError(Exception):
    """Raised when an invalid variable is encountered"""
    def __init__(self):
        self.message = f"Test error."
        super().__init__(self.message)