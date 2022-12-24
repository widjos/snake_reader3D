from Abstract.Instruction import Instruction
from Environment.Value import Value
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList

class Len(Instruction):

    def __init__(self, value:Expression,line, column) -> None:
        super().__init__()
        self.line = line
        self.column = column
        self.value = value

    def compile(self, environment):
        self.value.generator = self.generator
        val = self.value.compile(environment)

        #if val.type == typeExpression.STRING or val.type == typeExpression.ARRAY:
            
        paramTemp = self.generator.newTemp()
        tempAux = self.generator.newTemp()
        self.generator.addExpression(paramTemp,val.value,'','')
        self.generator.addMod(tempAux,paramTemp,'1')
        self.generator.addExpression(paramTemp,paramTemp,tempAux,'-')
        return Value(paramTemp,True,typeExpression.INT)

    