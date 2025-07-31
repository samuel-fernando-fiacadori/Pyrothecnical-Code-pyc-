import time
from zpyro.Lexer.models.Token import Token
from zpyro.Lexer.Lexer import Lexer
from zpyro.Parser.models.astnodes.CallNode import CallNode
from zpyro.Parser.models.astnodes.BinaryNode import BinaryNode
from zpyro.Parser.models.astnodes.VarAcessNode import VarAcessNode
from zpyro.Parser.models.astnodes.VarAssignNode import VarAssignNode
from zpyro.Parser.models.astnodes.ExitNode import ExitNode
from zpyro.Parser.models.astnodes.LiteralNode import LiteralNode
from zpyro.Parser.models.astnodes.FunctionNode import FunctionNode
from zpyro.Parser.models.ModelParser import ModelParser
from zpyro.Parser.error.ExpressionError import ExpressionError
from zpyro.Parser.error.ExpectingNode import ExpectingNode
from zpyro.Parser.models.astnodes.ReturnNode import ReturnNode
from zpyro.Parser.SubParser.ExpressionParser import ExpressionParser
from zpyro.Parser.SubParser.VariableParser import VariableParser

class Parser(ModelParser):
    def __init__(self, tokens: list):
        self.tokens: list = tokens
        self.index: int = 0
    
    def read(self):
        nodes = []
        while not self._is_at_end():
            current_index = self.index  # ← salva índice antes
            node = self._make_nodes()
            if self.index == current_index:
                self._advance()
            if node:
                nodes.append(node)
        return nodes
    
    def read_function(self):
        nodes = []
        while not self._is_at_end():
            current_index = self.index  # ← salva índice antes
            node = self._make_function_node()
            if self.index == current_index:
                self._advance()
            if node:
                nodes.append(node)
        return nodes 
            
    def _make_nodes(self):
        Node = None
        if self._match('VARIABLE_SINAL'):
            Node = self._handle_variable_node_creation()
        elif self._match('IDENTIFIER') and self._match('ASSIGNMENT', offset=1):
            Node = self._handle_variable_acess_creation()
        elif self._match('IDENTIFIER') and self._match('LEFT_PAREN', offset=1):
            ...
        elif self._match('FUNCTION_KEYWORD'):
            Node = self._handle_function_node_creation()
        elif self._match('LITERAL_INTEGER', 'LITERAL_FLOAT', 'LITERAL_STRING', 'LITERAL_BOOL'):
            Node = self._handle_expression_node_creation()
        elif self._match('EXIT_KEYWORD'):
            Node = self._handle_exit_node_creation()
        else:
            return None
        return Node
    
    def _make_function_node(self):
        if self._match('VARIABLE_SINAL'):
            return self._handle_variable_node_creation()
        elif self._match('IDENTIFIER') and self._match('ASSIGNMENT', offset=1):
            return self._handle_variable_acess_creation()
        elif self._match('RETURN_SINAL'):
            return self._handle_return_node_creation()
        elif self._match('LITERAL_INTEGER', 'LITERAL_FLOAT', 'LITERAL_STRING', 'LITERAL_BOOL'):
            return self._handle_expression_node_creation()
        else:
            return None
        
    def _handle_call_node_creation(self):
        identifer = self._consume('IDENTIFER')
        self._consume('LEFT_PAREN')
        
        return CallNode(identifer, [])
    
    
        
    def _handle_exit_node_creation(self):
        self._consume('EXIT_KEYWORD')
        expr_par = ExpressionParser(self.tokens, self.index)
        value, consumed = expr_par.build()
        self.index += consumed
        return ExitNode(value)

    def _handle_condition_structure_node_creatio(self):
        from zpyro.Parser.SubParser.ConditionParser import IfParser
        if_parser = IfParser(self.tokens, self.index)
        if_node = if_parser._parse_condition()
        self.index += if_parser.index  

        print(if_node)
        return if_node
    
    def _handle_return_node_creation(self):
        self._consume('RETURN_SINAL')
        value_to_return, consumed = ExpressionParser(self.tokens, self.index).build()
        self.index += consumed

        return ReturnNode(value_to_return)

    def _handle_variable_acess_creation(self): 
        var_parser: VariableParser = VariableParser(self.tokens, self.index)
        var_node, consumed = var_parser.variable_acess_creation()

        self.index += consumed
        return var_node 

    def _handle_variable_node_creation(self):
        var_parser: VariableParser = VariableParser(self.tokens, self.index)
        var_node, consumed = var_parser.variable_node_creation()

        self.index += consumed
        return var_node 
    
    def _handle_function_node_creation(self):
        from zpyro.Parser.SubParser.FunctionParser import FunctionParser


        fun_parser = FunctionParser(self.tokens, self.index)
        fun_node, consumed = fun_parser.build()
        

        self.index += consumed

        if not isinstance(fun_node, FunctionNode):
            raise ExpectingNode(f'Expected FunctionNode, got {type(fun_node)}')
        return fun_node


        

    def _handle_expression_node_creation(self):
        if self._match('ASSIGNMENT'):
            self._consume('ASSIGNMENT')

            self._advance()
        
        if self._match('LITERAL_INTEGER', 'LITERAL_FLOAT', 'LITERAL_STRING', 'LITERAL_BOOL', 'IDENTIFIER'):
            expr_parser: ExpressionParser = ExpressionParser(self.tokens, self.index)
            
            node, consumed = expr_parser.build()
            self.index += consumed

            if  isinstance(node, LiteralNode) or  isinstance(node, BinaryNode):
                return node
            else:
                raise ExpressionError('The ExpressionParser was not returned a node')
            

print()