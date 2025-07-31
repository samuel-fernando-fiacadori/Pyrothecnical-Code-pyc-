class ConditionNode:
    '''
    A condição esquerda pode ser a única para o ConditionNode, o interpretador irá verificar se o valor exite
    como: 

    null -> False
    '' -> False
    false -> False
    0 -> False

    'String' -> True
    true -> True
    1 > + -> True
    -1 > - -> True #Este valor por mais que negativo existe, diferente do zero que é representante do nada ou null
    
    '''

    def __init__(self, left_condition, expression_condition=None, right_condition=None):
        self.left_condition = left_condition
        self.expression_condition = expression_condition
        self.right_condition = right_condition

    def __repr__(self):
        return f'ConditionNode <left value: {self.left_condition}> <expression: {self.expression_condition}> <right value: {self.right_condition}>'
        