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
        elif tempValue.type == typeExpression.CHAR:
           self.generator.addPrintf("c",f' {tempValue.getValue()}')           
        elif tempValue.type == typeExpression.FLOAT:
            self.generator.addPrintf("f",f'float64({tempValue.getValue()})')
        elif tempValue.type == typeExpression.BOOL:
            newLabel = self.generator.newLabel()
            self.generator.addLabel(tempValue.trueLabel)
            self.generator.callFunc('widPrintTrue')
            #Instruccion
            self.generator.addGoto(newLabel)
            self.generator.addLabel(tempValue.falseLabel)
            self.generator.callFunc('widPrintFalse')
            self.generator.addLabel(newLabel)
        elif tempValue.type == typeExpression.STRING:
            self.generator.fnPrintString()
            paramTemp = self.generator.newTemp()
            self.generator.addExpression(paramTemp,'P', environment.size, '+')
            self.generator.addExpression(paramTemp,paramTemp, '1','+')
            self.generator.addSetStack(paramTemp, tempValue.value)
            self.generator.addNextStack(environment.size)
            self.generator.callFunc('printString')
            temp = self.generator.newTemp()
            self.generator.addGetStack(temp,'P')
            self.generator.addBackStack(environment.size)
        elif tempValue.type == typeExpression.ARRAY:
            self.generator.addExpression('P','P', environment.size, '+')
            self.generator.fnPrinArray()
            self.generator.addExpression('P','P',environment.size,'-')
            paramTemp =  self.generator.newTemp()
            self.generator.addExpression(paramTemp,'P', environment.size, '+')
            self.generator.addExpression(paramTemp,paramTemp, '1', '+')
            self.generator.addSetStack(paramTemp, tempValue.value)
            self.generator.addNextStack(environment.size)
            self.generator.callFunc('printArray')
            temp = self.generator.newTemp()
            self.generator.addGetStack(temp,'P')
            self.generator.addBackStack(environment.size)            
        else:
            print("Error en el print")


        self.generator.addNewLine()
        self.generator.addSpaceInCode()        

