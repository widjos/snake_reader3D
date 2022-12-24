from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import Value
from Environment.Contexto import errorList


class Logic(Expression):

    def __init__(self, left: Expression, right: Expression, type:str  , row , column) -> None:
        super().__init__()
        self.leftExp = left
        self.rightExp = right
        self.row = row
        self.column = column
        self.type = type

    def compile(self, environement: Environment) -> Value:
        self.leftExp.generator = self.generator
        self.rightExp.generator = self.generator

        newTemp = self.generator.newTemp()
        
        if self.trueLabel == "":
            self.trueLabel = self.generator.newLabel()
        if self.falseLabel == "":
            self.falseLabel = self.generator.newLabel()
                    
        lblAndOr = ''

        if self.type == 'AND':
            lblAndOr = self.leftExp.trueLabel = self.generator.newLabel()
            self.rightExp.trueLabel = self.trueLabel
            self.leftExp.falseLabel = self.rightExp.falseLabel = self.falseLabel
        elif self.type == 'OR':
            self.leftExp.trueLabel = self.rightExp.trueLabel = self.trueLabel
            lblAndOr = self.leftExp.falseLabel = self.generator.newLabel()
            self.rightExp.falseLabel = self.falseLabel
        else:
            self.leftExp.trueLabel = self.rightExp.trueLabel = self.falseLabel
            self.leftExp.falseLabel = self.rightExp.falseLabel = self.trueLabel
        
        leftValue: Value = self.leftExp.compile(environement)
        if leftValue.type != typeExpression.BOOL:
            print("Error en Logico")
            errorList.append({
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {leftValue.type} no es valido' , 
                        "fila":  leftValue.row , 
                        "columna": leftValue.column 
            })
            return
        if(lblAndOr != ''):
            self.generator.addLabel(lblAndOr)
        rightValue: Value = self.rightExp.compile(environement)
        if rightValue.type != typeExpression.BOOL:
            print("Error en Logico")
            errorList.append({
                        "tipo":"Error Semantico", 
                        "descripcion" : f'El tipo de dato {rightValue.type} no es valido' , 
                        "fila":  rightValue.row , 
                        "columna": rightValue.column 
            })
            return
        self.generator.addComment('Finalizo la expresion logica')
        ret = Value(None, False, typeExpression.BOOL)
        ret.trueLabel = self.trueLabel
        ret.falseLabel = self.falseLabel
        return ret
