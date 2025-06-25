import math

# Mapping of function names to their corresponding Python callables
TRIG_FUNCTIONS_MAP = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'csc': lambda x: 1 / math.sin(x),
    'sec': lambda x: 1 / math.cos(x),
    'cot': lambda x: 1 / math.tan(x),
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'csch': lambda x: 1 / math.sinh(x),
    'sech': lambda x: 1 / math.cosh(x),
    'coth': lambda x: 1 / math.tanh(x),
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'acsc': lambda x: math.asin(1 / x),
    'asec': lambda x: math.acos(1 / x),
    'acot': lambda x: math.atan(1 / x),
    'asinh': math.asinh,
    'acosh': math.acosh,
    'atanh': math.atanh,
    'acsch': lambda x: math.asinh(1 / x),
    'asech': lambda x: math.acosh(1 / x),
    'acoth': lambda x: math.atanh(1 / x),
}

MATH_FUNCTIONS_MAP = {
    'exp': math.exp,
    'sqrt': math.sqrt,
    'ln': math.log,
    'abs': abs,
}

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
            func_name = node['function']
            if func_name == 'log':
                base = self.evaluate_expression(node['base'], variable_values)
                return math.log(argument, base)
            if func_name in MATH_FUNCTIONS_MAP:
                return MATH_FUNCTIONS_MAP[func_name](argument)
            if func_name in TRIG_FUNCTIONS_MAP:
                return TRIG_FUNCTIONS_MAP[func_name](argument)
        elif node['type'] == 'FunctionCall':
            function_name = node['name']
            argument = self.evaluate_expression(node['argument'], variable_values)
            function_variable, expression = self.functions[function_name]
            return self.evaluate_expression(expression, {function_variable: argument})
        elif node['type'] == 'Factorial':
            operand = self.evaluate_expression(node['operand'], variable_values)
            if isinstance(operand, (int, float)):
                return math.factorial(int(operand))
            return f"{self.expression_to_string(node['operand'], variable_values)}!"
        elif node['type'] == 'Derivative':
            func_name = node['function']
            argument = self.evaluate_expression(node['argument'], variable_values)
            var, expr = self.functions[func_name]
            if isinstance(argument, (int, float)):
                h = 1e-6
                try:
                    plus = self.evaluate_expression(expr, {var: argument + h})
                    minus = self.evaluate_expression(expr, {var: argument - h})
                    return (plus - minus) / (2 * h)
                except Exception:
                    plus = self.evaluate_expression(expr, {var: argument + h})
                    minus = self.evaluate_expression(expr, {var: argument})
                    return (plus - minus) / h
            arg_str = self.expression_to_string(node['argument'], variable_values)
            return f"{func_name}'({arg_str})"

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
            elif expression['function'] in MATH_FUNCTIONS_MAP or expression['function'] in TRIG_FUNCTIONS_MAP:
                arg = self.expression_to_string(expression['argument'], variable_values)
                return f"{expression['function']}({arg})"
        elif expression['type'] == 'Derivative':
            function = expression['function']
            arg = self.expression_to_string(expression['argument'], variable_values)
            return f"{function}'({arg})"
        elif expression['type'] == 'FunctionCall':
            arg = self.expression_to_string(expression['argument'], variable_values)
            return f"{expression['name']}({arg})"
        elif expression['type'] == 'Factorial':
            operand = self.expression_to_string(expression['operand'], variable_values)
            return f"{operand}!"

