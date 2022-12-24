from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList


class If(Instruction):
    def __init__(self,condition:Expression, instructions, line, column , elseSt =None):
        self.condition = condition
        self.instructions = instructions
        self.elseSt = elseSt

    
    def compile(self,env):
        self.condition.generator = self.generator
        self.instructions.generator = self.generator
        condition = self.condition.compile(env)
        if condition.type != typeExpression.BOOL:
            print('->Error no booleano')
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {condition.type} no es booleano' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
            return
        self.generator.addLabel(condition.trueLabel)
        self.instructions.compile(env)
        if self.elseSt is not None:
            exitIf = self.generator.newLabel()
            self.generator.addGoto(exitIf)
        self.generator.addLabel(condition.falseLabel)
        if self.elseSt is not None:
            self.elseSt.generator = self.generator
            self.elseSt.compile(env)
            self.generator.addLabel(exitIf)

            