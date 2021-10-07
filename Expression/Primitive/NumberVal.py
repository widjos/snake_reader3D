from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import  Value
from Enum.typeExpression import typeExpression

class NumberVal(Expression):

    def __init__(self, type:typeExpression , value, row, column) -> None:
        super().__init__()
        self.type = type
        self.value = value
        self.row = row
        self.column = column


    def compile(self, environement: Environment) -> Value:

        if self.type == typeExpression.INT or self.type == typeExpression.FLOAT:
            return Value(str(self.value), False,self.type)

        print("Error no se reconoce el tipo")
        return Value("0", False, typeExpression.INT)
        
                

