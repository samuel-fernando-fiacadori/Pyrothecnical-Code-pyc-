
import sys
from zpyro.Interpretador.model.Environment import Environment
from zpyro.Interpretador.signal.ReturnSignal import ReturnSignal
from zpyro.Lexer.Lexer import Lexer
from zpyro.Parser.Parser import Parser
from zpyro.Parser.models.astnodes.LiteralNode import LiteralNode
from zpyro.Parser.models.astnodes.VarAssignNode import VarAssignNode
from zpyro.Parser.models.astnodes.VarAcessNode import VarAcessNode
from zpyro.Parser.models.astnodes.BinaryNode import BinaryNode
from zpyro.Parser.models.astnodes.FunctionNode import FunctionNode
from zpyro.Parser.models.astnodes.ReturnNode import ReturnNode
from zpyro.Parser.models.astnodes.ExitNode import ExitNode
from zpyro.Parser.models.astnodes.ConditionNode import ConditionNode
from zpyro.Parser.models.astnodes.CallNode import CallNode
from zpyro.Parser.models.astnodes.ConditionStructureNode import ConditionStructureNode


class Interpreter:
    """
    Interpreter for the Zpyro language.
    This version is more organized and includes support for function calls and nested scopes.
    """
    def __init__(self):
        # The environment is now a stack-based structure to handle nested scopes
        self.env_stack = [Environment()]
        self.functions = {}

        # Use a dispatch table to handle different node types, which is cleaner than a long if/elif chain
        self.node_handlers = {
            LiteralNode: self._eval_literal,
            ExitNode: self._eval_exit,
            VarAssignNode: self._eval_var_assign,
            VarAcessNode: self._eval_var_access,
            BinaryNode: self._eval_binary,
            FunctionNode: self._eval_function_definition,
            ReturnNode: self._eval_return,
            CallNode: self._eval_function_call,
            ConditionStructureNode: self._eval_condition_structure
        }

        # A dispatch table for operators is also more scalable
        self.operators = {
            '+': lambda left, right: left + right,
            '-': lambda left, right: left - right,
            '*': lambda left, right: left * right,
            '/': lambda left, right: left / right,
            '==': lambda left, right: left == right,
            '!=': lambda left, right: left != right,
            '<': lambda left, right: left < right,
            '>': lambda left, right: left > right,
        }

    def _current_env(self):
        """Helper to get the current environment on the stack."""
        return self.env_stack[-1]

    def _push_env(self):
        """Pushes a new environment onto the stack for a new scope."""
        new_env = Environment(parent=self._current_env())
        self.env_stack.append(new_env)

    def _pop_env(self):
        """Removes the current environment from the stack when a scope ends."""
        if len(self.env_stack) > 1:
            self.env_stack.pop()
        else:
            raise Exception("Cannot pop the global environment.")

    def run(self, nodes):
        """Main entry point to execute a list of nodes."""
        for node in nodes:
            result = self.eval_node(node)
            # Check for a ReturnSignal to handle function returns
            if isinstance(result, ReturnSignal):
                return result.value
        return None

    def eval_node(self, node):
        """
        Dispatches node evaluation to the appropriate handler method.
        This is much cleaner than the previous if/elif chain.
        """
        node_type = type(node)
        if node_type in self.node_handlers:
            return self.node_handlers[node_type](node)
        else:
            raise Exception(f"[Interpreter] Unknown node type: {node_type}")

    # --- Node Handler Methods ---

    def _eval_literal(self, node):
        return node.value
    
    def _eval_exit(self, node):
        print(self.eval_node(node.value))


    def _eval_var_assign(self, node):
        value = self.eval_node(node.value)
        self._current_env().set(node.name, value)

    def _eval_var_access(self, node):
        return self._current_env().Get(node.name).value

    def _eval_binary(self, node):
        left = self.eval_node(node.left)
        right = self.eval_node(node.right)
        op_func = self.operators.get(node.operator)
        if not op_func:
            raise Exception(f"Unsupported operator: {node.operator}")
        return op_func(left, right)

    def _eval_function_definition(self, node):
        self.functions[node.name] = node

    def _eval_function_call(self, node):
        # 1. Look up the function
        func_node = self.functions.get(node.name)
        if not func_node:
            raise Exception(f"Function '{node.name}' not defined.")

        # 2. Push a new environment for the function's scope
        self._push_env()

        # 3. Evaluate arguments and bind them to parameters
        if len(node.args) != len(func_node.params):
            raise Exception(f"Function '{node.name}' expects {len(func_node.params)} arguments, but got {len(node.args)}.")
        
        for param_name, arg_node in zip(func_node.params, node.args):
            arg_value = self.eval_node(arg_node)
            self._current_env().set(param_name, arg_value)

        result = self.run(func_node.body)

        # 5. Pop the environment to return to the previous scope
        self._pop_env()
        
        # Return the result of the function call
        return result

    def _eval_return(self, node):
        value = self.eval_node(node.value)
        return ReturnSignal(value)

    def _eval_condition_structure(self, node):
        if self._eval_condition(node.condition):
            return self.run(node.body)
        elif node.else_body:
            return self.run(node.else_body)

    def _eval_condition(self, cond_node: ConditionNode):
        left = self.eval_node(cond_node.left)
        right = self.eval_node(cond_node.right)
        op_func = self.operators.get(cond_node.operator)
        if not op_func:
            raise Exception(f"Unsupported operator: {cond_node.operator}")
        return op_func(left, right)


if __name__ == "__main__":
    
    # sys.argv é a lista de argumentos de linha de comando.
    # sys.argv[0] é o nome do script (interpreter.py)
    # sys.argv[1] será o nome do arquivo que queremos interpretar.
    
    if len(sys.argv) < 2:
        print("Uso: python interpreter.py <nome_do_arquivo>")
        sys.exit(1)

    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as file:
            content = file.read()

            tokens = Lexer(content).tokenize()
            nodes = Parser(tokens).read()

            Interpreter().run(nodes)


            
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        sys.exit(1)