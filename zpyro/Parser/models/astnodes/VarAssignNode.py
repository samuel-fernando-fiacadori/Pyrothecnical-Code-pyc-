class VarAssignNode:
    def __init__(self, name: str, value: any):
        self.name: str = name
        self.value: any = value

    def __repr__(self):
        return f'VarAssignNode: <name: {self.name}> <value: {self.value}>'