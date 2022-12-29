from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import Value
from Environment.Contexto import errorList

class GThan(Expression):

    def __init__(self, left: Expression, right: Expression,row, column) -> None:
        super().__init__()
        self.leftExp = left
        self.rightExp = right
        self.row = row
        self.column = column


    def compile(self, environement: Environment) -> Value:
        self.leftExp.generator = self.generator
        self.rightExp.generator = self.generator

        leftVal: Value = self.leftExp.compile(environement)
        rightVal: Value = self.rightExp.compile(environement)

        if leftVal.type == typeExpression.INT or leftVal.type == typeExpression.FLOAT:

            if rightVal.type == typeExpression.INT or rightVal.type == typeExpression.FLOAT:
                newValue = Value("", False, typeExpression.BOOL)
                
                if self.trueLabel == "":
                    self.trueLabel = self.generator.newLabel()
                if self.falseLabel == "":
                    self.falseLabel = self.generator.newLabel()
                    
                self.generator.addComment("Greather Than expression")
                self.generator.addIf(leftVal.value, rightVal.value, ">" ,self.trueLabel)
                self.generator.addGoto(self.falseLabel)

                newValue.trueLabel = self.trueLabel
                newValue.falseLabel = self.falseLabel
                return newValue
            else:
                print("Error en resta")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {leftVal.type} no es valido para realizar >' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })                
                return Value("",False,typeExpression.INT)  
        else:
            print("Error en resta")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {leftVal.type} no es valido para realizar >' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })                
            return Value(False,False,typeExpression.INT)        
