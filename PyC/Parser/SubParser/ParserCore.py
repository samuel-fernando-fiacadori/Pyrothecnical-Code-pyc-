from PyC.Lexer.Token import Token
from PyC.Parser.Variables.Variable import Variable
from PyC.Parser.Enviryoment.VariableEnv import VariableEnv
import time
from PyC.Parser.Enviryoment.VariableEnv import VariableEnv
from PyC.Parser.Enviryoment.FunctionEnv import FunctionEnv

SHARED_VARIABLE_ENV = VariableEnv()
SHARED_FUNCTION_ENV = FunctionEnv()

# Modelo de Parser
class ParserCore:
    def __init__(self, tokens, variable_env=None, function_env=None, index_ref=None):
        self.tokens = tokens
        self.index_ref = index_ref if index_ref is not None else {'index': 0}
        self.variable_env = variable_env or VariableEnv()
        self.function_env = function_env or FunctionEnv()


    @property
    def index(self):
        return self.index_ref['index']

    @index.setter
    def index(self, value):
        self.index_ref['index'] = value

    def _is_at_end(self):
        token = self._peek()
        if token.type == 'NEWLINE' or token.type == 'RBRACE':
            time.sleep(0.001)
            self._advance()
        return token.type == 'EOF'

    def _peek(self, offset=0):
        idx = self.index + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return Token('EOF', None)

    def _advance(self):
        token = self._peek()
        self.index += 1
        return token

    def _consume(self, *expected_types):
        token = self._peek()
        if token.type in expected_types:
            return self._advance()
        raise ValueError(f'Esperava {expected_types}, recebeu {token.type}')

    def _match(self, *expected_types):
        return self._peek().type in expected_types
