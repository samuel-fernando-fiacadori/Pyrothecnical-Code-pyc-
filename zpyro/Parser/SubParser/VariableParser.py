import time
from zpyro.Lexer.models.Token import Token
from zpyro.Lexer.Lexer import Lexer
from zpyro.Parser.models.astnodes.BinaryNode import BinaryNode
from zpyro.Parser.models.astnodes.VarAcessNode import VarAcessNode
from zpyro.Parser.models.astnodes.VarAssignNode import VarAssignNode
from zpyro.Parser.models.astnodes.LiteralNode import LiteralNode
from zpyro.Parser.models.astnodes.FunctionNode import FunctionNode
from zpyro.Parser.models.ModelParser import ModelParser
from zpyro.Parser.error.ExpressionError import ExpressionError
from zpyro.Parser.error.ExpectingNode import ExpectingNode

from zpyro.Parser.SubParser.ExpressionParser import ExpressionParser

class VariableParser(ModelParser):
    def __init__(self, tokens: list[Token], index_ref: int):
        self.tokens = tokens[index_ref:]
        self.index  = index_ref
    
    def variable_acess_creation(self):
        identifier = self._consume('IDENTIFIER')
        self._consume('ASSIGNMENT')
        return VarAcessNode(identifier.value), self.index

    def variable_node_creation(self):
        self._consume('VARIABLE_SINAL')
        identifier: Token = self._consume('IDENTIFIER')
        self._consume('ASSIGNMENT')
        value_node: BinaryNode|LiteralNode = self._handle_expression_node_creation()

        variable_node: VarAssignNode = VarAssignNode(
            name=identifier.value,
            value=value_node
        )

        return variable_node, self.index
    
    def _handle_expression_node_creation(self):
            if self._match('ASSIGNMENT'):
                self._consume('ASSIGNMENT')

                self._advance()

            if self._match('LITERAL_INTEGER', 'LITERAL_FLOAT', 'LITERAL_STRING', 'LITERAL_BOOL', 'IDENTIFIER'):
                expr_parser: ExpressionParser = ExpressionParser(self.tokens, self.index)

                node, consumed = expr_parser.build()
                self.index += consumed

                if  isinstance(node, LiteralNode) or  isinstance(node, BinaryNode):
                    return node
                else:
                    raise ExpressionError('The ExpressionParser was not returned a node')