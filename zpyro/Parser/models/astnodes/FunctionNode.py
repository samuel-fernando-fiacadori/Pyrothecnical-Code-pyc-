class FunctionNode:
    def __init__(self, name: str, arguments: list, body: list): #body is a list of nodes
          self.name = name
          self.arguments = arguments # VarAssignNodes
          self.body = body

    def __repr__(self):
         return f'FunctionNode: <name: {self.name}> <arguments: {self.arguments}> <body: {self.body}>'