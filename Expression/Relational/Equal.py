from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import Value

class Equal(Expression):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.leftExp = left
        self.rightExp = right


    def compile(self, environement: Environment) -> Value:
        pass    

