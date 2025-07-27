from PyC.Parser.Variables.Variable import Variable
from PyC.Parser.Enviryoment.Env import Env

class VariableEnv(Env):
    def __init__(self):
        super().__init__(Variable)

    def _get_type(self, type_string: str):
        type_dict: dict[str:object] = {
            'LITERAL_STRING':str,
            'LITERAL_INTEGER':int,
            'LITERAL_FLOAT':float,
            'LITERAL_BOOL':bool,
        }
        type: object = type_dict.get(type_string)
        if type is not None:
            return type
        else:
            raise NameError(f'The variable type is not what we was expecting: {type_string}')
        
    def set(self, identifier: str, type: str, value: str|int|float|bool):
        if self.OnEnv(identifier):
           raise ValueError(f'Variable "{identifier}" already exists. Use "assign" to change its value.')
        
        new_variable: Variable = Variable(identifier, self._get_type(type), value)
        self._object_dict[identifier] = new_variable
        print(new_variable)

    def assign(self, identifier: str, type: str , value: str|int|float|bool): 

        if self.OnEnv(identifier) == False:
            raise ValueError(f'Variable "{identifier}" not found in VariableEnv. Use "set" to declare it.')

        variable: Variable = self.Get(identifier)
        variable.type = self._get_type(type)
        variable.value = value

        print(f'Váriavel teve seu valor alterado: {variable}')

