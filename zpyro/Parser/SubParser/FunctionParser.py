from zpyro.Parser.models.ModelParser import ModelParser
from zpyro.Parser.models.astnodes.FunctionNode import FunctionNode
from zpyro.Parser.models.astnodes.VarAssignNode import VarAssignNode
from zpyro.Parser.models.astnodes.ReturnNode import ReturnNode
from zpyro.Parser.SubParser.ExpressionParser import ExpressionParser
from zpyro.Lexer.models.Token import Token

class FunctionParser(ModelParser):
    def __init__(self, tokens, index_ref: int):
        self.tokens: list[Token] = tokens[index_ref:]
        self.start_index: int = index_ref
        self.index: int = index_ref

        self.fun_node: FunctionNode = FunctionNode(None, [], [])

    def build(self):
        self._parse_signature()
        self._parse_body()

        return self.fun_node, self.index

    def _parse_signature(self):
        self._consume('FUNCTION_KEYWORD')
        name_token = self._consume('IDENTIFIER')
        self.fun_node.name = name_token.value

        self._consume('LEFT_PAREN')

        while not self._match('RIGHT_PAREN'):
            arg_token = self._consume('IDENTIFIER')
            self.fun_node.arguments.append(VarAssignNode(arg_token.value, None))

            if self._match('COMMA'):
                self._advance()

        self._consume('RIGHT_PAREN')
        self._consume('LEFT_BRACE')

    def _parse_body(self):
        from zpyro.Parser.Parser import Parser
        tokens = self._get_tokens()

        body_parser = Parser(tokens)
        nodes = body_parser.read_function()

        self.fun_node.body = [
            ReturnNode(node.value) if isinstance(node, ReturnNode) else node
            for node in nodes
        ]



    def _get_tokens(self):
        tokens = []
        open_braces = 1

        while open_braces > 0 and not self._is_at_end():
            token = self._advance()
            tokens.append(token) 

            if token.type == 'LEFT_BRACE':
                open_braces += 1
            elif token.type == 'RIGHT_BRACE':
                open_braces -= 1

        return tokens  # ← já vem com o RIGHT_BRACE incluso

