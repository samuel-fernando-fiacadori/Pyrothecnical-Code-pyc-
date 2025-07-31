
import re

class TokenDefinition:
    def __init__(self, _pattern: str, _type: str, _converter=lambda s: s):
        self._pattern: str = _pattern
        self._type: str = _type
        self._converter: function = _converter

    @property
    def pattern(self):
        return self._pattern
    
    @property
    def type(self):
        return self._type

    @property
    def converter(self):
        return self._converter