class Token:
    def __init__(self, _type: str, _value: any):
        self._type: str = _type
        self._value: any = _value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value
    
    def __eq__(self, __o: object):
        if not isinstance(__o, Token):
            return False
        return self._type == __o.type

    def __repr__(self):
        return f'TOKEN <type: {self._type}> <value: {self.value}>'