class BinaryNode:
    def __init__(self, left_node, operator: str=None, right_node=None):
        self.left = left_node
        self.operator = operator
        self.right = right_node


    def __repr__(self):
        if self.operator and self.right_node:
            return f"BinaryNode({self.left_node} {self.operator} {self.right_node})"
        return f"BinaryNode({self.left_node})"