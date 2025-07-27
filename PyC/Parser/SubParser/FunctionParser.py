from PyC.Parser.Enviryoment.FunctionEnv import FunctionEnv
from PyC.Parser.Functions.Function import Function
from PyC.Parser.SubParser.ParserCore import ParserCore

class FunctionParser(ParserCore):
    def __init__(self, tokens, variable_env=None, function_env=None, index_ref=None):
        super().__init__(tokens, variable_env, function_env, index_ref)

    def read(self):
        while not self._is_at_end():
            print('FUNCTION_PARSER')
            if self._match('NEWLINE'):
                break
            if self._match('FUNCTION_KEYWORD'):
                self._parse_function()
            else:
                self._advance()


    def _parse_function(self):
        self._consume('FUNCTION_KEYWORD')
        identifier = self._consume('IDENTIFIER')
        self._consume('LPAREN')

        params = []
        if not self._match('RPAREN'):
            while True:
                param = self._consume('IDENTIFIER')
                params.append(param.value)
                if self._match('COMMA'):
                    self._advance()
                else:
                    break
        self._consume('RPAREN')
        self._consume('LBRACE')

        body = []
        depth = 1
        while not self._is_at_end() and depth > 0:
            token = self._advance()
            if token.type == 'LBRACE':
                depth += 1
            elif token.type == 'RBRACE':
                depth -= 1
            if depth > 0:
                body.append(token)

        function = Function(identifier.value, params, body)
        self.function_env.define(function)
        print(f"FUNÇÃO REGISTRADA: {function.identifier} com {len(body)} tokens.")
