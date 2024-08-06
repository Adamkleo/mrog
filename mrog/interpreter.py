from .function import Function
from .exceptions import *

class Interpreter:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        self.global_scope = {}

    def interpret(self):
        ast = self.semantic_analyzer.analyze()
        for node in ast:
            print(node)
            self.visit(node)


    def visit(self, node):
        node_type = node['type']
        method_name = 'visit_' + node_type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit method defined for node type {node["type"]}')
    
    def visit_FunctionDefinition(self, node):
        function = Function(node['name'], node['function_variable'], node['expression'])
        self.global_scope[node['name']] = function

    def visit_PrintStatement(self, node):
        """Executing print statements of the form: print(f(expression))"""
        
        # f(2) // num
        # f(x) // id
        # f(x + 2) // Bexpr
        # f(2+3) // Bexpr


        # Extract the expression of the print statement
        print_arg = node['argument']

        # Check if the expression is a function call. ie. print(f(x))
        if print_arg['type'] == 'FunctionCall':
            # Get the function name
            function_name = print_arg['name']
            # Check if the function is defined
            function = self.global_scope.get(function_name)
            if not function:
                raise UndefinedFunctionError(function_name)
            
            # Get the argument of the function call
            function_arg = print_arg['argument']
            # If the function argument is a number, evaluate the function
            if function_arg['type'] == 'Number':
                # Evaluate the function with the number argument
                result = function.evaluate(function_arg['value'])
                # print the result
                print(f"{function_name}({function_arg['value']}) = {result}")

            # If the function argument is an expression
            if function_arg['type'] == 'BinaryExpression':
                # Evaluate the expression
                result = self.evaluate_expression(function_arg)
                # Evaluate the function with the expression argument
                result = function.evaluate(result)
                # print the result
                print(f"{function_name}({self.stringify_expression(function_arg)}) = {result}")