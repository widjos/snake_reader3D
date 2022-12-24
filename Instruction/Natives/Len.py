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

        if val is None:
            print("var no existe")
            return

        elif val.type == typeExpression.STRING or val.type == typeExpression.ARRAY:
            
            paramTemp = self.generator.newTemp()
            self.generator.addExpression(paramTemp,val.value, '', '')
            self.generator.addGetHeap(paramTemp,paramTemp)
            return Value(paramTemp,True,typeExpression.INT)

        else:
            print("Error en nativa")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {val.type} no es valido para realizar la funcion len()' , 
                        "fila":  self.line , 
                        "columna": self.column 
                    }) 
            return Value("0",True,typeExpression.INT)  