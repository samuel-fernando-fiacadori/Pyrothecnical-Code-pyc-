import re

class TokenDefinition:
    def __init__(self, pattern: str, type: str, converter= lambda x: x):
        self.pattern: str = re.compile(pattern)
        self.token_type: str = type
        self.converter = converter