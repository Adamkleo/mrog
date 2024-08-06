import math

class Function:
    def __init__(self, name, variable, expression):
        self.name = name
        self.variable = variable
        self.expression = expression


    def evaluate(self, argument):
        return self._evaluate_expression(self.expression, argument)

    def _evaluate_expression(self, expr, argument):
        if expr['type'] == 'Number':
            return expr['value']
        elif expr['type'] == 'Variable':
            if expr['value'] == self.variable:
                return argument
            else:
                raise Exception(f'Unknown variable {expr["value"]}')
        elif expr['type'] == 'BinaryExpression':
            left = self._evaluate_expression(expr['left'], argument)
            right = self._evaluate_expression(expr['right'], argument)
            operator = expr['operator']
            return self._evaluate_binary_expression(left, operator, right)
        
        elif expr['type'] == 'MathFunction':
            function_name = expr['function']
            if function_name == 'sin':
                return math.sin(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'cos':
                return math.cos(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'tan':
                return math.tan(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'sqrt':
                return math.sqrt(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'ln':
                return math.log(self._evaluate_expression(expr['argument'], argument), math.e)
            elif function_name == 'abs':
                return abs(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'exp':
                return math.exp(self._evaluate_expression(expr['argument'], argument))
            elif function_name == 'log':
                return math.log(self._evaluate_expression(expr['argument'], argument), self._evaluate_expression(expr['base'], argument))


        else:
            raise Exception(f'Unknown expression type {expr["type"]}')
        

    def _evaluate_binary_expression(self, left, operator, right):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '^':
            return left ** right


        