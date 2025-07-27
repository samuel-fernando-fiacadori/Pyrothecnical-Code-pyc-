class Variable:
    def __init__(self, identifier: str, type: object, value: any):
        self.identifier = identifier
        self.type = type
        self.value = value

    def __eq__(self, __o: object):
        if isinstance(__o, int|float|bool|str):
            return self.value == __o
        elif isinstance(__o, Variable):
            return self.value == __o.value
        else:
            return False
        
    def __ne__(self, __o: object):
        if isinstance(__o, int|float|bool|str):
            return self.value != __o
        elif isinstance(__o, Variable):
            return self.value != __o.value
        else:
            return False
        
    def __lt__(self, __o: object):
        if isinstance(__o, int|float|bool|str):
            return self.value < __o
        elif isinstance(__o, Variable):
            return self.value < __o.value
        else:
            return False
        
    def __gt__(self, __o: object):
        if isinstance(__o, int|float|bool|str):
            return self.value > __o
        elif isinstance(__o, Variable):
            return self.value > __o.value
        else:
            return False

    def __str__(self):
        return F'VARIABLE <Identifier: {self.identifier}> <Type: {self.type}> <value: {self.value}>'
    