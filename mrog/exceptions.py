class InvalidVariableError(Exception):
    """Raised when an invalid variable is encountered"""
    def __init__(self, variable, message="Invalid variable encountered"):
        self.variable = variable
        self.message = f"{message}: {variable}. Only x, y, z are allowed."
        super().__init__(self.message)

"""
# Example usage:
def validate_variable(variable):
    valid_variables = ['x', 'y', 'z']
    if variable not in valid_variables:
        raise InvalidVariableError(variable)
    # Proceed with processing if the variable is valid
    return variable

try:
    validate_variable('a')
except InvalidVariableError as e:
    print(f"Error: {e}")
"""