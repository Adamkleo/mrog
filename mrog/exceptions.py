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
        self.variable = variable
        self.message = f"Error in line {line}: {message}: {variable}. Only x, y, z are allowed."
        super().__init__(self.message)

class InvalidExpressionVariableError(Exception):
    """Raised when an expression variable does not match its function variable."""
    def __init__(self, character, line, 
                 message="Expression variable does not match function variable"):
        self.character = character
        self.message = f"Error in line {line}: {message}: {character}."
        super().__init__(self.message)

class InvalidSyntaxError(Exception):
    """Raised when an invalid syntax is encountered"""
    def __init__(self, line, 
                 message="Invalid syntax"):
        self.message = f"Error in line {line}: {message}."
        super().__init__(self.message)

class UnknownSymbolError(Exception):
    """Raised when an unknown symbol is encountered"""
    def __init__(self, symbol):
        self.message = f"Unknown symbol encountered: {symbol}"
        super().__init__(self.message)

class UndefinedFunctionError(Exception):
    """Raised when an invalid function is encountered"""
    def __init__(self, function_name):
        self.message = f"Undefined function {function_name}" 
        super().__init__(self.message)