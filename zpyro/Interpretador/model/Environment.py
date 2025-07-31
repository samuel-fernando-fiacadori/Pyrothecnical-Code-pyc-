from zpyro.Interpretador.model.Variable import Variable
from zpyro.Interpretador.error.AlreadyInEnv import AlreadyInEnv

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def InEnv(self, identifier):
        return identifier in self.variables
    
    def Get(self, identifier):
        if self.InEnv(identifier):
            return self.variables.get(identifier)

    def set(self, name: str, value: any):
        if self.InEnv(name):
            raise AlreadyInEnv(f'The variable "{name}" is already in env. Maybe try to "Assign" a nem value to it')
        var: Variable = Variable(None, None, None)

        var.name = name
        var.type = type(value)
        var.value = value

        self.variables[name] = var

    def assign(self, name, value: any):
        if not self.InEnv(name):
            raise AlreadyInEnv(f'The variable "{name}" is not in env. Maybe try to "Set" a value to it')
        var: Variable = self.Get(name)

        var.type = type(value)
        var.value = value