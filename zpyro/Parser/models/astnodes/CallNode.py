class CallNode:
    def __init__(self, name: str, args: list):
        self.name = name        # Nome da função
        self.args = args        # Lista de nós (argumentos)

    def __repr__(self):
        return f'CallNode: <name: {self.name}> <args: {self.args}>'