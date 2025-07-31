from zpyro.Parser.models.ModelParser import ModelParser
from zpyro.Parser.models.astnodes.FunctionNode import FunctionNode
from zpyro.Parser.models.astnodes.VarAssignNode import VarAssignNode
from zpyro.Parser.models.astnodes.VarAcessNode import VarAcessNode
from zpyro.Parser.models.astnodes.LiteralNode import LiteralNode
from zpyro.Parser.SubParser.ExpressionParser import ExpressionParser
from zpyro.Parser.models.astnodes.ConditionNode import ConditionNode
from zpyro.Parser.models.astnodes.ConditionStructureNode import ConditionStructureNode
from zpyro.Parser.error.ExpectingNode import ExpectingNode
from zpyro.Lexer.models.Token import Token



class IfParser(ModelParser):
    def __init__(self, tokens: list[Token], index_ref: int):
        self.tokens: list[Token] = tokens[index_ref:]
        self.index = 0

    def _get_tokens(self):
        tokens: list[Token] = []

        self._consume('CONDITION_SINAL')

        while not self._is_at_end():
                if self._match('RIGHT_BRACE'):
                     break
                
                tokens.append(self._peek())
                self._advance()

        return tokens

    def _get_body_tokens(self):
        tokens = []
        open_braces = 1

        while open_braces > 0 and not self._is_at_end():
            token = self._advance()
            if token.type == 'LEFT_BRACE':
                open_braces += 1
            elif token.type == 'RIGHT_BRACE':
                open_braces -= 1
            tokens.append(token)

        return tokens[:-1]  # remove o último RIGHT_BRACE

    
    def _parse_condition(self):
        self._consume('CONDITION_SINAL')
        self._consume('LEFT_PAREN')

        left_token = self._advance()
        operator = self._advance()
        right_token = self._advance()

        self._consume('RIGHT_PAREN')

        left, right = self._handle_condition_node_creation(left_token, right_token)
        condition = ConditionNode(left, operator.value, right)

        self._consume('LEFT_BRACE')

        from zpyro.Parser.Parser import Parser
        body_tokens = self._get_body_tokens()
        body = Parser(body_tokens).read()

        else_body = None
        if self._match('ELSE_SINAL'):
            self._consume('ELSE_SINAL')
            self._consume('LEFT_BRACE')
            else_tokens = self._get_body_tokens()
            else_body = Parser(else_tokens).read()

        return ConditionStructureNode(condition, body, else_body)

                

    def _handle_condition_node_creation(self, left_token, right_token):
        from zpyro.Parser.Parser import Parser

        def convert(token: Token):
            if token.type.startswith("LITERAL"):
                return LiteralNode(token.value)
            elif token.type == "IDENTIFIER":
                return VarAcessNode(token.value)
            else:
                raise ExpectingNode(f"Unexpected token in condition: {token}")

        left = convert(left_token)
        right = convert(right_token)

        return left, right

               
