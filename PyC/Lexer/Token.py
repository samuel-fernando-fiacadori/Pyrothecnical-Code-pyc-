class Token:
    '''
    Definição de um token:
    Um objeto que tem seu tipo e valor que o Parser irá utilizar para fazer instruções

    Formas de criação:
    Quando um Lexer detectar algum padrão, criará um token com seu tipo (Pré determinado) e seu valor (indefinido)
    '''
    def __init__(self, token_type: str, token_value: str|int|float|bool):
        self._type: str = token_type
        self._value: str|int|float|bool = token_value

    # Setter não será utilizado para manter a integridade das informações.
    @property
    def type(self):
        return self._type
    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return f'TOKEN <type: {self._type}> <value: {self._value}>'