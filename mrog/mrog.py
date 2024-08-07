# mrog/mrog.py
import argparse

from mrog.lexer import Lexer
from mrog.parser import Parser
from mrog.semantic import SemanticAnalyzer
from mrog.interpreter import Interpreter
from mrog.exceptions import *

def main():
    parser = argparse.ArgumentParser(description="Process .mg files with the mrog lexer.")
    parser.add_argument("filename", help="The .mg file to process")
    
    args = parser.parse_args()
    
    try:
        with open(args.filename, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File {args.filename} not found.")
        return


    functions = {}
    ast = None
    try:
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        semantic_analyzer = SemanticAnalyzer(parser)
        interpreter = Interpreter(semantic_analyzer)
        result = interpreter.interpret()
        print(result)


    except (InvalidVariableError, InvalidIdentifierError, \
            InvalidExpressionVariableError, InvalidArgumentError, \
            InvalidSyntaxError, UnknownSymbolError, UndefinedFunctionError, \
            InvalidPrintArgumentError, 
            
            ) as e:
        print(e)
        
    if ast:
        print(ast)




            


