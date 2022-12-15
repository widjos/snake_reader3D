from Abstract.Expression import Expression
from  Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression



class While(Instruction):

    def __init__(self, condition: Expression , block: Instruction) -> None:
        self.condition = condition ; 
        self.block = block;
        

    def compile(self, environment: Environment) -> Value:
        
        self.condition.generator = self.generator
        self.block.generator = self.generator

        #Label que engloba el codigo  del while 
        newLabel = self.generator.newLabel()
        self.generator.addLabel(newLabel)

        valueCondition = self.condition.compile(environment)

        if(valueCondition.type == typeExpression.BOOL):
            self.generator.addLabel(valueCondition.trueLabel)
            self.block.compile(environment)
            self.generator.addGoto(newLabel)
            self.generator.addLabel(valueCondition.falseLabel)
        else:
            print("SEMANTIC ERROR  not a booleand type inside a  if condition")   

