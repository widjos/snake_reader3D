from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import  Value
from Enum.typeExpression import typeExpression
from Environment.Contexto import errorList

class Literal(Expression):

    def __init__(self, type:typeExpression , value, row, column) -> None:
        super().__init__()
        self.type = type
        self.value = value
        self.row = row
        self.column = column


    def compile(self, environement: Environment) -> Value:
        
        if self.type == typeExpression.BOOL:
            #              
            if self.trueLabel == "":
                self.trueLabel = self.generator.newLabel()
            if self.falseLabel == "":
                self.falseLabel = self.generator.newLabel()
            
            if self.value:
                self.generator.addGoto(self.trueLabel)
                self.generator.addComment("Para evitar Errores")
                self.generator.addGoto(self.falseLabel)
            else:
                self.generator.addGoto(self.falseLabel)
                self.generator.addComment("Para evitar Errores")
                self.generator.addGoto(self.trueLabel)
            newValue = Value(self.value, False, typeExpression.BOOL)    
            newValue.trueLabel = self.trueLabel
            newValue.falseLabel = self.falseLabel
            return newValue
        
        elif self.type == typeExpression.STRING:
            retTemp = self.generator.newTemp()
            self.generator.addExpression(retTemp, 'H', '', '')
            self.generator.addSetHeap('H',0)
            self.generator.addNextHeap()
            for char in str(self.value):
                self.generator.addSetHeap('H', ord(char))
                self.generator.addNextHeap()

            self.generator.addSetHeap('H','-1')
            self.generator.addNextHeap()
            self.generator.addExpression(retTemp,retTemp, '0.12837', '+')
            return Value(retTemp,True,typeExpression.STRING)
        elif self.type == typeExpression.ARRAY:
            elements = []
            
            for element in  self.value:
                print("---> Resultado: "+ str(element))
                element.generator = self.generator
                valor = element.compile(environement)
                elements.append(valor.value)
                if(valor.type == typeExpression.STRING):
                    tempAuxiliar = self.generator.newTemp()
                    self.generator.addExpression(tempAuxiliar,valor.value,'','')
                    Environment.heapS.append(tempAuxiliar)
                elif valor.type == typeExpression.ARRAY:
                    tempAuxiliar = self.generator.newTemp()
                    self.generator.addExpression(tempAuxiliar,valor.value,'','')
                    Environment.heapA.append(tempAuxiliar)
            retTemp = self.generator.newTemp()
            self.generator.addExpression(retTemp,'H','','')
            self.generator.addSetHeap('H',len(self.value))
            self.generator.addNextHeap()
            for element in elements:
                self.generator.addSetHeap('H',element)
                self.generator.addNextHeap()
            self.generator.addExpression(retTemp,retTemp,'0.12837','+')
            return Value(retTemp,True,typeExpression.ARRAY)
        else:
            print("Error no se reconoce el tipo")
            errorList.append(
                    {
                        "tipo":"Error array", 
                        "descripcion" : f'valor no valido para alamacenar' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    }) 
            return Value("0", False, typeExpression.INT)