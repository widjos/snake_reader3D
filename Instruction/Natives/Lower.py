from Abstract.Instruction import Instruction
from Environment.Value import Value
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList

class Lower(Instruction):

    def __init__(self, value:Expression,line, column) -> None:
        super().__init__()
        self.line = line
        self.column = column
        self.value = value

    def compile(self, environment):
        self.value.generator = self.generator
        val = self.value.compile(environment)

        if val.type == typeExpression.STRING:
            
            self.generator.fToLower()
            paramTemp = self.generator.newTemp()
            self.generator.addExpression(paramTemp,'P', environment.size, '+')
            self.generator.addExpression(paramTemp, paramTemp, '1','+')
            self.generator.addSetStack(paramTemp,val.value)
            self.generator.addNextStack(environment.size)
            self.generator.callFunc("toLower")
            temp1 = self.generator.newTemp()
            temp2 = self.generator.newTemp()

            self.generator.addExpression(temp2,'P',1,'+')
            self.generator.addGetStack(temp1,temp2)
            return Value(temp1,True,typeExpression.STRING)

        else:
            print("Error en nativa")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {val.type} no es valido para realizar la funcion nativa' , 
                        "fila":  self.line , 
                        "columna": self.column 
                    }) 
            return    
