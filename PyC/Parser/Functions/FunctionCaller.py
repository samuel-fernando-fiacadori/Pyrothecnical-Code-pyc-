from PyC.Parser.SubParser.ParserCore import ParserCore
from PyC.Parser.Parser import Parser  
from PyC.Parser.Enviryoment.FunctionEnv import FunctionEnv
from PyC.Parser.Enviryoment.VariableEnv import VariableEnv

class FunctionCaller:
    def __init__(self, function_env: FunctionEnv, variable_env: VariableEnv):
        self.function_env = function_env
        self.variable_env = variable_env

    def call(self, function_name: str, args: list = []):
        function = self.function_env.call(function_name)

        # ⚠️ Parâmetros ainda não estão sendo usados aqui. Se quiser, a gente implementa depois.
        print(f'Executando função: {function.identifier} com {len(function.body)} tokens')

        # Executa o corpo da função com os mesmos ambientes
        parser = Parser(function.body, self.variable_env, self.function_env)
        parser.read()
