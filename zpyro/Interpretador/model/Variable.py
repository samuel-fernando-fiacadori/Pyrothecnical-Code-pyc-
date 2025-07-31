class Variable:
    def __init__(self, name: str, type: object ,value: any):
        self.name: str = name
        self.type: object = type
        self.value: any = value

    def __str__(self):
        return f'Variable: <name: {self.name}> <type: {self.type}> <value: {self.value}>'