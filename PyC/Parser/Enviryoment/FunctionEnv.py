from PyC.Parser.Functions.Function import Function
from PyC.Parser.Enviryoment.Env import Env

class FunctionEnv(Env):
    def __init__(self):
        super().__init__(Function)

    def define(self, function: Function):
        if self.OnEnv(function.identifier):
            raise ValueError(f'A função "{function.identifier}" já está definida.')
        self._object_dict[function.identifier] = function

    def get(self, identifier: str) -> Function:
        if not self.OnEnv(identifier):
            raise NameError(f'A função "{identifier}" não foi encontrada.')
        return self._object_dict[identifier]

    def __contains__(self, identifier: str):
        return self.OnEnv(identifier)

    def __getitem__(self, identifier: str) -> Function:
        return self.get(identifier)

    def all(self):
        return list(self._object_dict.keys())
    