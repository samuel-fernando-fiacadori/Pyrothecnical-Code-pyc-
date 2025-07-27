import re
from PyC.Lexer.TokenDefinition import TokenDefinition
from PyC.Lexer.Token import Token

class SintaxError(Exception):
    pass


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.index = 0
        self.automato = self._build_automaton()

    def _build_automaton(self):
        return {
            'q0': {
                r'"': 'q1',
                r"'": 'q2',
                r'[0-9]': 'q3',
                r'[a-zA-Z_]': 'q5',
                r'f': 'q7',
                r'=': TokenDefinition(r'=', 'ASSIGNMENT'),
                r'\+': TokenDefinition(r'\+', 'PLUS_SIGN'),
                r'\-': TokenDefinition(r'\-', 'SUB_SIGN'),
                r'\*': TokenDefinition(r'\*', 'MULTI_SIGN'),
                r'/': TokenDefinition(r'\/', 'DIV_SIGN'),
                r'\(': TokenDefinition(r'\(', 'LPAREN'),
                r'\)': TokenDefinition(r'\)', 'RPAREN'),
                r'\{': TokenDefinition(r'\{', 'LBRACE'),
                r'\}': TokenDefinition(r'\}', 'RBRACE'),
                r'\,': TokenDefinition(r'\,', 'COMMA'),
                r'\;': TokenDefinition(r'\;', 'NEWLINE'),
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
                r'let': TokenDefinition(r'let', 'VARIABLE_SINAL'),
                r'fun': TokenDefinition(r'fun', 'FUNCTION_KEYWORD'),
                r'(true|false)': TokenDefinition(r'(true|false)', 'LITERAL_BOOL', lambda s: s == 'true'),
                r'[a-zA-Z_][a-zA-Z0-9_]*': TokenDefinition(r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            },
        }

    def tokenize(self):
        tokens = []
        while self.index < len(self.code):
            if self.code[self.index].isspace():
                self.index += 1
                continue

            token, new_index = self._run_automaton()
            if token:
                tokens.append(token)
                self.index = new_index
            else:
                raise SintaxError(f"Erro léxico próximo a: '{self.code[self.index:]}'")
        return tokens

    def _run_automaton(self): # essa merda me levou 1 mês inteiro para mim fazer
        state = 'q0'
        lexema = ''
        start = self.index
        i = start
        last_token = None
        last_index = i

        while i < len(self.code):
            char = self.code[i]
            transitioned = False

            for pattern, next_state in self.automato[state].items():
                if re.fullmatch(pattern, char):
                    lexema += char
                    i += 1
                    transitioned = True

                    if isinstance(next_state, TokenDefinition):
                        value = next_state.converter(lexema) if next_state.converter else lexema
                        last_token = Token(next_state.token_type, value)
                        last_index = i
                        return last_token, last_index
                    else:
                        state = next_state
                    break

            if not transitioned:
                break

        # Verificação de estados com END (como q3 e q5)
        if 'END' in self.automato[state]:
            end_def = self.automato[state]['END']
            if isinstance(end_def, TokenDefinition):
                match = re.fullmatch(end_def.pattern, lexema)
                if match:
                    value = end_def.converter(lexema) if end_def.converter else lexema
                    return Token(end_def.token_type, value), i
            elif isinstance(end_def, str):  # vai para estado q6 para verificação
                for pat, defn in self.automato[end_def].items():
                    if re.fullmatch(pat, lexema):
                        value = defn.converter(lexema) if defn.converter else lexema
                        return Token(defn.token_type, value), i

        return last_token, i

