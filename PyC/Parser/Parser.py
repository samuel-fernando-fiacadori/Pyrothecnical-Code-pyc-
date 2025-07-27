from PyC.Lexer.Lexer import Lexer
from PyC.Parser.SubParser.ParserCore import ParserCore
from PyC.Parser.SubParser.ExpressionParser import ExpressionParser
from PyC.Parser.SubParser.VariableParser import VariableParser
from PyC.Parser.SubParser.FunctionParser import FunctionParser

class Parser(ParserCore):
    def __init__(self, tokens, variable_env=None, function_env=None):
        index_ref = {'index': 0}
        super().__init__(tokens, variable_env, function_env, index_ref=index_ref)

        self.function_parser = FunctionParser(tokens, self.variable_env, self.function_env, index_ref)
        self.variable_parser = VariableParser(tokens, self.variable_env, self.function_env, index_ref)

        self.handlers = {
            'FUNCTION_KEYWORD': self._handle_function_declaration,
            'VARIABLE_SINAL': self._handle_variable_declaration,
            'IDENTIFIER': self._handle_identifier,
        }

    def read(self):
        while not self._is_at_end():
            token = self._peek()

            handler = self.handlers.get(token.type, self._default_handler)
            handler()

    # ================================
    # Handlers
    # ================================

    def _handle_function_declaration(self):
        self.function_parser.read()

    def _handle_variable_declaration(self):
        self.variable_parser.read()

    def _handle_identifier(self):
        kind = self._discover_identifier_type()

        if kind is None and self._peek().type == 'VARIABLE_SINAL':
            self.variable_parser.read()
        elif kind == 'VAR' and self._peek(1).type == 'ASSIGNMENT':
            self.variable_parser.read()
        elif kind == 'FUN' and self._peek(1).type == 'LPAREN' and self._peek(3).type == 'NEWLINE':
            self._call_function(self._peek().value)
        else:
            print(f"[WARN] Identificador desconhecido ou mal usado: {self._peek().value}")
            self._advance()

    def _default_handler(self):
        self._advance()

    # ================================
    # Auxiliares
    # ================================

    def _discover_identifier_type(self):
        token = self._peek()
        if token.value in self.function_env._object_dict:
            return 'FUN'
        elif token.value in self.variable_env._object_dict:
            return 'VAR'
        return None

    def _call_function(self, name):
        from PyC.Parser.Functions.FunctionCaller import FunctionCaller
        caller = FunctionCaller(self.function_env, self.variable_env)
        caller.call(name)




codigo = '''
let x = 20;
x = x + 30 / 90
'''


tokens = Lexer(codigo).tokenize()
Par = Parser(tokens)
Par.read()        
