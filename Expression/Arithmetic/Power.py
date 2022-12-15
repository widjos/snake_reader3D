from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import Value
from Environment.Contexto import errorList


class  Power(Expression):

    def __init__(self, left: Expression , right: Expression , row , column) -> None:
        super().__init__()
        self.leftExp = left
        self.rightExp = right
        self.row = row
        self.column = column


    def compile(self, environement: Environment) -> Value:
        
        self.leftExp.generator = self.generator
        self.rightExp.generator = self.generator

        leftValue: Value = self.leftExp.compile(environement)
        rightValue: Value = self.rightExp.compile(environement)

        newTemp = self.generator.newTemp()

        if leftValue.type == typeExpression.INT:
            if rightValue.type == typeExpression.INT or rightValue.type == typeExpression.FLOAT:
                self.generator.addPowerOperation(newTemp, leftValue.getValue() , rightValue.getValue())
                return Value(newTemp, True, rightValue.type)
            else:
                print("Error en suma")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido para realizar la potencia' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    }) 
                return Value("0",False,typeExpression.INT)
        elif leftValue.type == typeExpression.FLOAT:
            if rightValue.type == typeExpression.INT or rightValue.type == typeExpression.FLOAT:
                self.generator.addPowerOperation(newTemp,leftValue.getValue(),rightValue.getValue())
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en resta")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido para realizar la potencia' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })                
                return Value("0",False,typeExpression.INT)
        else:
            print("Error suma")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {leftValue.type} no es valido para realizar la potencia' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
            return Value("0",False,typeExpression.INT)
