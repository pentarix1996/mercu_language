#!/usr/bin/env python3

import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 2:
        print("Uso: mercu archivo.mer")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.mer'):
        print("Error: La extensión del archivo debe ser .mer")
        sys.exit(1)

    with open(filename, 'r', encoding="utf-8") as file:
        code = file.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    interpreter.interpret()


if __name__ == '__main__':
    main()
