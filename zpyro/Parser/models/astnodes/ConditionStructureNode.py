class ConditionStructureNode:
    def __init__(self, condition, body: list, else_body: list):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f'''
        ConditionStructureNode: 
        <Condition: {self.condition}>
        <body> {self.body}
        <else_body: {self.else_body}>
'''