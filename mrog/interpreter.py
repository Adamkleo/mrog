import math

class Interpreter:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        self.functions = {}
        self.function_strings = {}

    def interpret(self):
        for node in self.semantic_analyzer.analyze():
            if node['type'] == 'FunctionDefinition':
                self.handle_function_definition(node)
            elif node['type'] == 'PrintStatement':
                self.handle_print_statement(node)

    def handle_function_definition(self, node):
        function_name = node['name']
        function_variable = node['function_variable']
        expression = node['expression']
        self.functions[function_name] = (function_variable, expression)

    def handle_print_statement(self, node):
        argument = node['argument']
        if argument['type'] == 'FunctionCall':
            function_name = argument['name']
            arg = self.evaluate_expression(argument['argument'])
            if isinstance(arg, (int, float)):
                arg_to_print = int(arg) if arg % 1 == 0 else arg
                result = self.evaluate_expression(argument)
                print(f"{function_name}({arg_to_print}) = {result}")
            else:
                function_str = self.get_function_string(function_name, arg)
                self.function_strings[function_name] = function_str
                print(f"{function_name}({arg}) = {function_str}")
        else:
            result = self.evaluate_expression(argument)
            print(result)

    def evaluate_expression(self, node, variable_values={}):
        if node['type'] == 'Number':
            return node['value']
        elif node['type'] == 'Variable':
            return variable_values.get(node['value'], node['value'])
        elif node['type'] == 'BinaryExpression':
            left = self.evaluate_expression(node['left'], variable_values)
            right = self.evaluate_expression(node['right'], variable_values)
            if node['operator'] == '+':
                return left + right
            elif node['operator'] == '-':
                return left - right
            elif node['operator'] == '*':
                return left * right
            elif node['operator'] == '/':
                return left / right
            elif node['operator'] == '^':
                return left ** right
        elif node['type'] == 'MathFunction':
            argument = self.evaluate_expression(node['argument'], variable_values)
            if node['function'] == 'log':
                base = self.evaluate_expression(node['base'], variable_values)
                return math.log(argument, base)
            elif node['function'] == 'abs':
                return abs(argument)
            elif node['function'] == 'ln':
                return math.log(argument)
        elif node['type'] == 'FunctionCall':
            function_name = node['name']
            argument = self.evaluate_expression(node['argument'], variable_values)
            function_variable, expression = self.functions[function_name]
            return self.evaluate_expression(expression, {function_variable: argument})

    def get_function_string(self, function_name, argument):
        function_variable, expression = self.functions[function_name]
        if argument == function_variable:
            return self.expression_to_string(expression)
        else:
            return self.expression_to_string(expression, {function_variable: argument})

    def expression_to_string(self, expression, variable_values={}):
        if expression['type'] == 'Number':
            if expression['value'] % 1 == 0:
                return str(int(expression['value']))
            return str(expression['value'])
        elif expression['type'] == 'Variable':
            return str(variable_values.get(expression['value'], expression['value']))
        elif expression['type'] == 'BinaryExpression':
            left = self.expression_to_string(expression['left'], variable_values)
            right = self.expression_to_string(expression['right'], variable_values)
            return f"{left} {expression['operator']} {right}"
        elif expression['type'] == 'MathFunction':
            if expression['function'] == 'log':
                base = self.expression_to_string(expression['base'], variable_values)
                arg = self.expression_to_string(expression['argument'], variable_values)
                return f"log({base}, {arg})"
            elif expression['function'] == 'abs':
                arg = self.expression_to_string(expression['argument'], variable_values)
                return f"abs({arg})"
            elif expression['function'] == 'ln':
                arg = self.expression_to_string(expression['argument'], variable_values)
                return f"ln({arg})"
            elif expression['function'] == 'sqrt':
                arg = self.expression_to_string(expression['argument'], variable_values)
                return f"sqrt({arg})"
        elif expression['type'] == 'Derivative':
            function = expression['function']
            arg = self.expression_to_string(expression['argument'], variable_values)
            return f"{function}'({arg})"
        elif expression['type'] == 'FunctionCall':
            arg = self.expression_to_string(expression['argument'], variable_values)
            return f"{expression['name']}({arg})"

