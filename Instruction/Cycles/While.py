from Abstract.Expression import Expression
from  Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList



class While(Instruction):

    def __init__(self, condition: Expression , block: Instruction) -> None:
        self.condition = condition ; 
        self.block = block;
        

    def compile(self, environment: Environment) -> Value:
        
        self.condition.generator = self.generator
        self.block.generator = self.generator

   
        continueLbl = self.generator.newLabel()
        self.generator.addLabel(continueLbl)
        valueCondition = self.condition.compile(environment)
        newEnv = Environment(environment)
        if(valueCondition.type == typeExpression.BOOL):
            newEnv.breakLbl = valueCondition.falseLabel
            newEnv.continueLbl = continueLbl
            self.generator.addLabel(valueCondition.trueLabel)
            self.block.compile(newEnv)
            self.generator.addGoto(continueLbl)
            self.generator.addLabel(valueCondition.falseLabel)
        else:
            print("SEMANTIC ERROR  not a booleand type inside a  if condition")   
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'Condicion del While no es booleana' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
