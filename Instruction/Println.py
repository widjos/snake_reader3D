from Enum.typeExpression import typeExpression
from Environment.Value import Value
from Abstract.Instruction import Instruction
from Abstract.Expression import Expression
from Environment.Environment import Environment

class Println(Instruction):

    def __init__(self, exp: Expression) -> None:
        super().__init__()
        self.exp = exp

    def compile(self, environment: Environment) -> Value:
        self.exp.generator = self.generator

        tempValue: Value = self.exp.compile(environment)
        if tempValue.type == typeExpression.INT:
           self.generator.addPrintf("d",f' int64({tempValue.getValue()})')
        elif tempValue.type == typeExpression.FLOAT:
            self.generator.addPrintf("f",f'float64({tempValue.getValue()})')
        else:
            print("Error en el print")


        self.generator.addNewLine()        

