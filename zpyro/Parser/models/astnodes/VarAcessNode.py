class VarAcessNode:
    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self):
        return f'VarAcessNode <name: {self.name}>'