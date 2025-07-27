class ObjectNotFounded(Exception):
    pass

class Env:
    def __init__(self, _object: object):
        self._object_type = _object
        self._object_dict: dict[str:_object] = {}

    def OnEnv(self, identifier: str):
        if identifier in self._object_dict:
            return True
        return False
    
    def Get(self, identifier: str):
        if self.OnEnv(identifier):
            return self._object_dict.get(identifier)
        else:
            raise ObjectNotFounded(f'Env was not fouded the object: {identifier} of type {self._object_type}')
    
    def All(self):
        return self._object_dict.copy()