from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import Value
from Environment.Contexto import errorList


class  Plus(Expression):

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
                self.generator.addExpression(newTemp, leftValue.getValue() , rightValue.getValue(), "+")
                return Value(newTemp, True, rightValue.type)
            else:
                print("Error en suma")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido para realizar una suma' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })                                                 
                return Value("0",False,typeExpression.INT)
        elif leftValue.type == typeExpression.FLOAT:
            if rightValue.type == typeExpression.INT or rightValue.type == typeExpression.FLOAT:
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"+")
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en suma")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido para realizar una suma' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })                  
                return Value("0",False,typeExpression.INT)
        elif leftValue.type == typeExpression.STRING:
            if rightValue.type == typeExpression.STRING:
                leftTemp = self.generator.newTemp()
                rightTemp = self.generator.newTemp()
                retTemp   = self.generator.newTemp()
                auxuliarTemp = self.generator.newTemp()

                self.generator.addExpression(retTemp,'H','','')
                self.generator.addExpression(leftTemp,leftValue.getValue(), '','')
                self.generator.addExpression(rightTemp,rightValue.getValue(), '','')
                self.generator.addExpression(auxuliarTemp,leftValue.getValue(), '','')

                #Second part for the right

                leftLabel = self.generator.newLabel()
                rightLabel = self.generator.newLabel()
                leftSwaper = self.generator.newTemp()
                rightSwaper = self.generator.newTemp()
                self.generator.addGetHeap(leftSwaper,leftTemp)
                self.generator.addGetHeap(rightSwaper,rightTemp)

                self.generator.addLabel(leftLabel)
                self.generator.addSetHeap('H',leftSwaper)
                self.generator.addNextHeap()
                self.generator.addExpression(leftTemp,leftTemp,'1','+')
                self.generator.addGetHeap(leftSwaper,leftTemp)
                self.generator.addIf(leftSwaper,'-1','!=',leftLabel)

                self.generator.addLabel(rightLabel)
                self.generator.addSetHeap('H',rightSwaper)
                self.generator.addNextHeap()
                self.generator.addExpression(rightTemp,rightTemp,'1','+')
                self.generator.addGetHeap(rightSwaper,rightTemp)
                self.generator.addIf(rightSwaper,'-1','!=',rightLabel)
                
                self.generator.addSetHeap('H','-1')
                self.generator.addNextHeap()

            else:
                print("Error suma")
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido para realizar concatenacion' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    }) 


            return Value(retTemp,True,typeExpression.STRING)   
        
        else:
            print("Error suma")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {leftValue.type} no es valido para realizar una suma' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })  
            return Value("0",False,typeExpression.INT)

 