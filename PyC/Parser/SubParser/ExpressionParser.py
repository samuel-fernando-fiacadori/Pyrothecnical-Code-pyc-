from PyC.Parser.SubParser.ParserCore import ParserCore
from PyC.Lexer.Token import Token
from PyC.Parser.Enviryoment.VariableEnv import VariableEnv

# Esse aqui é de matemática (a + b) (a - b), etc...
class ExpressionParser(ParserCore):
    def __init__(self, tokens, variable_env=None, function_env=None):
        super().__init__(tokens, variable_env, function_env)

    def parse_expression(self):
        output = []
        operator_stack = []

        precedence = {
            'PLUS_SIGN': 1,
            'SUB_SIGN': 1,
            'MULTI_SIGN': 2,
            'DIV_SIGN': 2,
        }

        while not self._is_at_end():
            token = self._peek()


            if token.type.startswith('LITERAL'):
                output.append(self._advance())

            elif token.type == 'IDENTIFIER':
                var = self.variable_env.Get(token.value)
                output.append(Token(f'LITERAL_{var.type.__name__.upper()}', var.value))
                self._advance()

            elif token.type in precedence:
                while operator_stack and precedence.get(operator_stack[-1].type, 0) >= precedence[token.type]:
                    output.append(operator_stack.pop())
                operator_stack.append(self._advance())

            else:
                break
            

        while operator_stack:
            output.append(operator_stack.pop())

        result = self._evaluate_postfix(output)
        return result
    
    def _token_type(self, token):
        if isinstance(token, str):
            return 'LITERAL_STRING'
        elif isinstance(token, int):
            return 'LITERAL_INTEGER'
        elif isinstance(token, float):
            return 'LITERAL_FLOAT'
        elif isinstance(token, bool):
            return 'LITERAL_BOOL'
        else:
            raise ValueError('Variable type not founded')
    
    def _Oper_string(self, a, b):
        if isinstance(a, str) and isinstance(b, str):
            return a + b
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + b
        else:
            raise TypeError(f"Operação '+' inválida entre {type(a)} e {type(b)}")
        
    def _Err_string(self, a, b, oper):
        operations = {
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }
        if isinstance(a, str) or isinstance(b, str):
            raise TypeError(f'{oper} não suporta operação com {type(a)} e {type(b)}')
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return operations.get(oper)(a, b)
    
    def _evaluate_postfix(self, tokens: list[Token]):
        stack = []

        
        for token in tokens:
            if token.type.startswith('LITERAL'):
                stack.append(token.value)
            elif token.type in ['PLUS_SIGN', 'SUB_SIGN', 'MULTI_SIGN', 'DIV_SIGN']:
                b = stack.pop()
                a = stack.pop()
                if token.type == 'PLUS_SIGN':
                    stack.append(self._Oper_string(a, b))
                elif token.type == 'SUB_SIGN':
                    stack.append(self._Err_string(a, b, '-'))
                elif token.type == 'MULTI_SIGN':
                    stack.append(self._Err_string(a, b, '*'))
                elif token.type == 'DIV_SIGN':
                    stack.append(self._Err_string(a, b, '/'))
        
        result = stack[0]
        token_type = self._token_type(result)
        return Token(token_type, result)
