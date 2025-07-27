class Function:
    def __init__(self, identifier: str, params: list[str], inside_code: list): #inside_code: list, decidi por não importa o token no lexer
        self._identifier: str = identifier
        self._params: list[str] = params
        self._body: list = inside_code

    @property
    def identifier(self):
        return self._identifier
    
    @property
    def params(self):
        return self._params
    
    @property
    def body(self):
        return self._body
    
    def __str__(self):
        return f'FUNCTION <Identifier: {self._identifier}> <BodySize: {len(self._body)} tokens>'