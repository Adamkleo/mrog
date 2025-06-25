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
        function_variables = node['function_variables']
        expression = node['expression']
        self.functions[function_name] = (function_variables, expression)

    def handle_print_statement(self, node):
        argument = node['argument']
        if argument['type'] == 'FunctionCall':
            function_name = argument['name']
            args = [self.evaluate_expression(a) for a in argument['arguments']]
            if all(isinstance(a, (int, float)) for a in args):
                display_args = [int(a) if isinstance(a, float) and a % 1 == 0 else a for a in args]
                result = self.evaluate_expression(argument)
                args_str = ', '.join(str(a) for a in display_args)
                print(f"{function_name}({args_str}) = {result}")
            else:
                func_str = self.get_function_string(function_name, args)
                print(f"{function_name}({', '.join(str(a) for a in args)}) = {func_str}")
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
        elif node['type'] == 'Matrix':
            return [[self.evaluate_expression(elem, variable_values) for elem in row] for row in node['elements']]
        elif node['type'] == 'FunctionCall':
            function_name = node['name']
            arguments = [self.evaluate_expression(a, variable_values) for a in node['arguments']]
            vars_, expression = self.functions[function_name]
            env = {v: val for v, val in zip(vars_, arguments)}
            return self.evaluate_expression(expression, env)
        elif node['type'] == 'Factorial':
            operand = self.evaluate_expression(node['operand'], variable_values)
            if isinstance(operand, (int, float)):
                return math.factorial(int(operand))
            return f"{self.expression_to_string(node['operand'], variable_values)}!"
        elif node['type'] == 'Derivative':
            func_name = node['function']
            arguments = [self.evaluate_expression(a, variable_values) for a in node['arguments']]
            vars_, expr = self.functions[func_name]
            if all(isinstance(a, (int, float)) for a in arguments):
                h = 1e-6
                grads = []
                for i, var in enumerate(vars_):
                    plus_args = arguments.copy()
                    minus_args = arguments.copy()
                    plus_args[i] += h
                    minus_args[i] -= h
                    try:
                        plus = self.evaluate_expression(expr, {v: val for v, val in zip(vars_, plus_args)})
                        minus = self.evaluate_expression(expr, {v: val for v, val in zip(vars_, minus_args)})
                        diff = self.matrix_subtract(plus, minus)
                        grads.append(self.matrix_scalar_divide(diff, 2*h))
                    except Exception:
                        plus = self.evaluate_expression(expr, {v: val for v, val in zip(vars_, plus_args)})
                        base = self.evaluate_expression(expr, {v: val for v, val in zip(vars_, arguments)})
                        diff = self.matrix_subtract(plus, base)
                        grads.append(self.matrix_scalar_divide(diff, h))
                return grads[0] if len(grads) == 1 else grads
            arg_str = ', '.join(self.expression_to_string(a, variable_values) for a in node['arguments'])
            return f"{func_name}'({arg_str})"

    def get_function_string(self, function_name, arguments):
        vars_, expression = self.functions[function_name]
        if arguments == vars_:
            return self.expression_to_string(expression)
        else:
            env = {v: arg for v, arg in zip(vars_, arguments)}
            return self.expression_to_string(expression, env)

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
            args = ', '.join(self.expression_to_string(a, variable_values) for a in expression['arguments'])
            return f"{function}'({args})"
        elif expression['type'] == 'FunctionCall':
            args = ', '.join(self.expression_to_string(a, variable_values) for a in expression['arguments'])
            return f"{expression['name']}({args})"
        elif expression['type'] == 'Factorial':
            operand = self.expression_to_string(expression['operand'], variable_values)
            return f"{operand}!"
        elif expression['type'] == 'Matrix':
            rows = []
            for row in expression['elements']:
                row_str = ', '.join(self.expression_to_string(e, variable_values) for e in row)
                rows.append(f"[{row_str}]")
            return '[' + ', '.join(rows) + ']'

    def matrix_subtract(self, a, b):
        if isinstance(a, list):
            return [self.matrix_subtract(x, y) for x, y in zip(a, b)]
        return a - b

    def matrix_scalar_divide(self, a, scalar):
        if isinstance(a, list):
            return [self.matrix_scalar_divide(x, scalar) for x in a]
        return a / scalar

