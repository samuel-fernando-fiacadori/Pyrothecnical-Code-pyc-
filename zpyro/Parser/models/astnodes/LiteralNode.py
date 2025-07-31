class LiteralNode:
    def __init__(self, value: any):
        self.value = value

    def __repr__(self):
        return f'LiteralNode <value: {self.value}>'