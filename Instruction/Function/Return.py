from Abstract.Expression import Expression
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList


class Return(Expression):
    def __init__(self, exp:Expression,line,column) -> None:
        super().__init__()
        self.exp = exp
        self.row = line
        self.column = column

    def compile(self,environemnt:Environment):
        if environemnt.returnLbl == '':
            print("Error return fuera de funcion")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'Return fuera de funcion' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
            return
        self.exp.generator = self.generator
        value = self.exp.compile(environemnt)
        if value.type == typeExpression.BOOL:
            tempLbl = self.generator.newLabel()
            self.generator.addLabel(value.trueLabel)
            self.generator.addSetStack('P','1')
            self.generator.addGoto(tempLbl)
            self.generator.addLabel(value.falseLabel)
            self.generator.addSetStack('P','0')
            self.generator.addLabel(tempLbl)
        else:
            self.generator.addSetStack('P',value.value)
        self.generator.addGoto(environemnt.returnLbl)