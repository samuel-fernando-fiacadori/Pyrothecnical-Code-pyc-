from zpyro.Parser.error.ExpectingToken import ExpectingToken
from zpyro.Parser.error.OffsetOutOfRange import OffsetOutOfRange
from zpyro.Lexer.models.Token import Token



class ModelParser:
    def __init__(self, tokens: list):
        self.tokens: list = tokens
        self.index: int = 0

    def _advance(self):
        token = self._peek()
        if not self._match('EOF'):
            self.index += 1
        return token

    def _peek(self, offset: int=0):
        
        token_lenght: int = len(self.tokens)
        idx: int = self.index + offset
        if idx < token_lenght:
            return self.tokens[idx]
        else:
            return Token('EOF', None)
        
    def _consume(self, *expected_type):
        
        if self._match(*expected_type):
            return self._advance()
        else:
            raise ExpectingToken(f'Expecting: {expected_type} received: {self._peek().type}')

    def _match(self, *expected_type, offset: int=0):
        actual_token: Token = self._peek(offset)
        if actual_token.type in expected_type:
            return True
        elif not actual_token.type in expected_type:
            return False
        
    def _is_at_end(self):
        if self._match('NEW_LINE'):
            self._advance()
        return self._match('EOF')