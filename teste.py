from PyC.Lexer.Lexer import Lexer
from PyC.Lexer.Token import Token
from PyC.Parser.Parser import Parser



def getcode():
    code: str = ''
    with open('code.txt', 'r') as arch:
        for line in arch:
            code += line

    return code

code: str = getcode()
lexer: Lexer = Lexer(code)


tokens: list[Token] = lexer.tokenize()
parser: Parser = Parser(tokens)

parser.read()