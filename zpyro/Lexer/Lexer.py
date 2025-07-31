import re
from zpyro.Lexer.models.Token import Token
from zpyro.Lexer.models.TokenDefinition import TokenDefinition
from zpyro.Lexer.error.SintaxError import SintaxError

class Lexer:
    def __init__(self, _code: str):
        self._code: str = _code
        self._index: int = 0
        self._automato: dict[str:dict] = self._build_automaton()

    def _build_automaton(self):
        return {
            'q0': {
                r'\"': 'q1',
                r"\'": 'q2',
                r'[0-9]': 'q3',
                r'[a-zA-Z_]': 'q5',

                # Comparation signals
                r'\=': 'q7',
                r'\>': TokenDefinition(r'\>', 'HIGHER_THAN'),
                r'\<': TokenDefinition(r'\<', 'LESSER_THAN'),

                # Math
                r'\+': TokenDefinition(r'\+', 'EXPR_PLUS'),
                r'\-': TokenDefinition(r'\-', 'EXPR_SUBTRACT'),
                r'\*': TokenDefinition(r'\*', 'EXPR_MULTIPLICATION'),
                r'\/': TokenDefinition(r'\/', 'EXPR_DIVISION'),

                #Reserved for function, while and if steatment 
                r'\(': TokenDefinition(r'\(', 'LEFT_PAREN'),
                r'\)': TokenDefinition(r'\)', 'RIGHT_PAREN'),
                r'\{': TokenDefinition(r'\{', 'LEFT_BRACE'),
                r'\}': TokenDefinition(r'\}', 'RIGHT_BRACE'),
                r'\,': TokenDefinition(r'\,', 'COMMA'),

                # End of the line
                r'\;': TokenDefinition(r'\;', 'NEW_LINE'),
            },
            'q1': {
                r'"': TokenDefinition(r'"[^"]+"', 'LITERAL_STRING', lambda s: s[1:-1]),
                r'[^"]': 'q1',
            },
            'q2': {
                r"'": TokenDefinition(r"'[^']+'", 'LITERAL_STRING', lambda s: s[1:-1]),
                r"[^']": 'q2',
            },
            'q3': {
                r'[0-9]': 'q3',
                r'\.': 'q4',
                'END': TokenDefinition(r'[0-9]+', 'LITERAL_INTEGER', lambda s: int(s)),
            },
            'q4': {
                r'[0-9]': 'q4',
                'END': TokenDefinition(r'[0-9]+\.[0-9]+', 'LITERAL_FLOAT', lambda s: float(s)),
            },
            'q5': {
                r'[a-zA-Z0-9_]': 'q5',
                'END': 'q6',
            },
            'q6': {
                r'return': TokenDefinition(r'return', 'RETURN_SINAL'),
                r'if': TokenDefinition(r'if', 'CONDITION_SINAL'),
                r'let': TokenDefinition(r'let', 'VARIABLE_SINAL'),
                r'def': TokenDefinition(r'def', 'FUNCTION_KEYWORD'),
                r'exit': TokenDefinition(r'exit', 'EXIT_KEYWORD'),
                r'(true|false)': TokenDefinition(r'(true|false)', 'LITERAL_BOOL', lambda s: s == 'true'),
                r'[a-zA-Z_][a-zA-Z0-9_]*': TokenDefinition(r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            },
            'q7': {
                r'\=': TokenDefinition(r'==', 'EQUALS'),
                'END': TokenDefinition(r'=', 'ASSIGNMENT')
            }
        }
    

    def tokenize(self):
        tokens = []
        while self._index < len(self._code):
            if self._code[self._index].isspace():
                self._index += 1
                continue

            token, new_index = self._run_automaton()
            if token:
                tokens.append(token)
                self._index = new_index
            else:
                raise SintaxError(f"Erro léxico próximo a: '{self.code[self.index:]}'")
        return tokens

    def _run_automaton(self):
        state = 'q0'
        lexema = ''

        start = self._index
        i = start

        last_token = None
        last_index = i

        while i < len(self._code):
            char = self._code[i]
            transitioned = False

            for pattern, next_state in self._automato[state].items():
                if re.fullmatch(pattern, char):
                    lexema += char
                    i += 1
                    transitioned = True

                    if isinstance(next_state, TokenDefinition):
                        value = next_state.converter(lexema) if next_state.converter else lexema
                        last_token = Token(next_state.type, value)
                        last_index = i
                        return last_token, last_index
                    else:
                        state = next_state
                    break

            if not transitioned:
                break

        # Verificação de estados com END (como q3 e q5)
        if 'END' in self._automato[state]:
            end_def = self._automato[state]['END']
            if isinstance(end_def, TokenDefinition):
                match = re.fullmatch(end_def.pattern, lexema)
                if match:
                    value = end_def.converter(lexema) if end_def.converter else lexema
                    return Token(end_def.type, value), i
            elif isinstance(end_def, str):  # vai para estado q6 para verificação
                for pat, defn in self._automato[end_def].items():
                    if re.fullmatch(pat, lexema):
                        value = defn.converter(lexema) if defn.converter else lexema
                        return Token(defn.type, value), i

        return last_token, i