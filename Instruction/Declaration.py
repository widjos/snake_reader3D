from Abstract.Instruction import Instruction
from Enum.typeExpression import  typeExpression
from Abstract.Expression import  Expression
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Environment.Value import Value

class Declaration(Instruction):

    def __init__(self, id: str , exp: Expression , type: typeExpression) -> None:
        self.id = id
        self.exp = exp
        self.type = type 


    def compile(self, environment: Environment) -> Value:

        self.exp.generator = self.generator
        newValue: Value = self.exp.compile(environment)
        self.type = newValue.type
        #tempVar:Symbol = environment.getVariable(self.id)

       
        tempVar = environment.saveVariable(self.id , newValue.type,
                  (newValue.type == typeExpression.STRING or 
                  newValue.type == typeExpression.ARRAY or
                  newValue.type == typeExpression.STRUCT), 
                  newValue.structType)          


        if self.type != typeExpression.BOOL: 
            self.generator.addSetStack(str(tempVar.position), newValue.getValue())
        else:
            newLabel = self.generator.newLabel()
            self.generator.addLabel(newValue.trueLabel)
            self.generator.addSetStack(str(tempVar.position), '1')
            self.generator.addGoto(newLabel)
            self.generator.addLabel(newValue.falseLabel)
            self.generator.addSetStack(str(tempVar.position), '0')
            self.generator.addLabel(newLabel)    

