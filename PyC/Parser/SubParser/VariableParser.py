from PyC.Parser.SubParser.ParserCore import ParserCore
from PyC.Parser.SubParser.ExpressionParser import ExpressionParser
from PyC.Lexer.Token import Token
from PyC.Lexer.Lexer import Lexer

# este lida com váriaveis
class VariableParser(ParserCore):
    def __init__(self, tokens, variable_env=None, function_env=None, index_ref=None):
        super().__init__(tokens, variable_env, function_env, index_ref)
        

    def read(self):
        while not self._is_at_end():
            if self._match('NEWLINE'):
                break

            if self._match('VARIABLE_SINAL'):
                self._parse_declaration()
            elif self._match('IDENTIFIER') and self._peek(1).type == 'ASSIGNMENT':
                self._parse_assignment()
            else:
                self._advance()

    def _parse_declaration(self):
        self._consume('VARIABLE_SINAL')
        identifier = self._consume('IDENTIFIER')
        self._consume('ASSIGNMENT')


        value_token = self._resolve_expression()
        self.variable_env.set(identifier.value, value_token.type, value_token.value)

    def _parse_assignment(self):
        identifier = self._consume('IDENTIFIER')
        self._consume('ASSIGNMENT')

        value_token = self._resolve_expression()
        self.variable_env.assign(identifier.value, value_token.type, value_token.value)

    def _resolve_expression(self):
        expression_tokens = []

        while not self._peek().type in ['EOF', 'NEWLINE']:  # ou outro separador
            expression_tokens.append(self._advance())

        expr_parser = ExpressionParser(expression_tokens, self.variable_env)
        result: Token = expr_parser.parse_expression()
        return result
    