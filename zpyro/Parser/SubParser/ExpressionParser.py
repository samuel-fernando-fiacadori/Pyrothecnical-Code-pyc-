from zpyro.Parser.models.ModelParser import ModelParser
from zpyro.Parser.models.astnodes.BinaryNode import BinaryNode
from zpyro.Parser.models.astnodes.LiteralNode import LiteralNode
from zpyro.Parser.models.astnodes.VarAcessNode import VarAcessNode
from zpyro.Lexer.models.Token import Token


class ExpressionParser(ModelParser):
    def __init__(self, tokens: list[Token], index_ref: int):
        self.tokens = tokens
        self.start_index = index_ref
        self.index = index_ref  # usa o index real!
    
    def build(self):
        expr = self._parse_expression()
        consumed = self.index - self.start_index
        return expr, consumed

    def _parse_expression(self, min_precedence=0):
        left = self._parse_primary()

        while True:
            token = self._peek()
            if not token.type.startswith('EXPR'):
                break

            precedence = self._get_precedence(token)
            if precedence < min_precedence:
                break

            operator = self._advance().value  # consome operador
            right = self._parse_expression(precedence + 1)
            left = BinaryNode(left, operator, right)

        return left

    def _parse_primary(self):
        token = self._advance()
        

        if token.type.startswith('LITERAL'):
            return LiteralNode(token.value)

        elif token.type == 'IDENTIFIER':
            return VarAcessNode(token.value)

        raise Exception(f"Token inesperado em expressão: {token}")

    def _get_precedence(self, token: Token):
        if token.type in ('EXPR_MULTIPLICATION', 'EXPR_DIVISION'):
            return 2
        if token.type in ('EXPR_PLUS', 'EXPR_SUBTRACT'):
            return 1
        return 0
