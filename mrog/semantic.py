from .symbols import VARIABLES
from .exceptions import *


class SemanticAnalyzer:
    def __init__(self, parser):
        self.parser = parser
        self.functions = {}
        self.current_line = 1

    def analyze(self):
        ast = self.parser.parse()
        for statement in ast:
            self.analyze_statement(statement)
            self.current_line += 1

        return ast

    def analyze_statement(self, statement):
        statement_type = statement['type']
        method_name = 'analyze_' + statement_type
        analyzer = getattr(self, method_name, self.generic_analyze)
        return analyzer(statement)
    
    def generic_analyze(self, statement):
        raise Exception(f'No analyze method defined for statement type {statement["type"]}')
    
    def analyze_FunctionDefinition(self, statement):
        # Get function details
        function_name = statement['name']
        function_variable = statement['function_variable']
        expression = statement['expression']

        # Check if the function variable is valid
        if function_variable not in VARIABLES:
            raise InvalidVariableError(function_variable, self.current_line)

        # Check if the function expression varriable matches the function variable
        non_function_variables = VARIABLES.difference(set(function_variable))
        for var in non_function_variables:
            if var in self.parser.used_variables[self.current_line]:
                raise InvalidExpressionVariableError(self.current_line, function_name, var, function_variable)
            
        # Check if any of the functions that are called in the current function expressions dont exist
        for function in self.parser.functions_called[self.current_line]:
            if function not in self.functions.keys():
                raise UndefinedFunctionError(self.current_line, function)

        # Add function to functions dictionary
        function = (function_variable, expression)
        self.functions[function_name] = function


    def analyze_PrintStatement(self, statement):
        # Extract the argument of the print call
        print_arg = statement['argument']

        # Check if the argument is a function call
        if print_arg['type'] == 'FunctionCall':
            # Get the function name
            function_name = print_arg['name']
            # Check if the function is defined
            if function_name not in self.functions.keys():
                raise UndefinedFunctionError(self.current_line, function_name)
            
        # Check if the argument is a function call by function name only. ie. print(f)
        if print_arg['type'] == 'Variable':
            if print_arg['value'] not in self.functions.keys():
                raise UndefinedFunctionError(self.current_line, print_arg['value'])


