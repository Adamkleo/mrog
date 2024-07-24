# mrog/mrog.py
import argparse

from mrog.lexer import Lexer
from mrog.parser import Parser



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



    lexer = Lexer(input_text)
    parser = Parser(lexer)
    ast = parser.parse()
    print(ast)


            


