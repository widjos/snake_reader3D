from Abstract.Expression import Expression
from  Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Expression.Primitive.Literal import Literal
from Expression.Primitive.NumberVal import NumberVal
from Instruction.Declaration import Declaration
from Environment.Contexto import errorList


class For(Instruction):
    def __init__(self, varTemp, val1:Expression, instruct:Instruction, row,column,  val2=None) -> None:
        super().__init__()
        self.varTemp = varTemp
        self.val1 = val1
        self.instruct = instruct
        self.val2 = val2
        self.row = row
        self.column = column

    def compile(self,env):
        self.val1.generator = self.generator
        leftVal = self.val1.compile(env)
        if self.val2 is not None:
           self.val2.generator = self.generator
           rightVal = self.val2.compile(env)
           temp1 = self.generator.newTemp()
           litTemp = Literal(typeExpression.INT, temp1, self.row, self.column)
           self.generator.addExpression(temp1,leftVal,'','')
           continueLbl = self.generator.newLabel()
           self.generator.addLabel(continueLbl)
           endLbl = self.generator.newLabel()
           self.generator.addIf(temp1,rightVal.value,">",endLbl)
           newEnv = Environment(env)
           newEnv.breakLbl = endLbl
           newEnv.continueLbl = continueLbl
           self.varTemp.generator = self.generator
           dec = Declaration(litTemp,self.varTemp, self.varTemp.type)
           dec.generator = self.generator
           dec.compile(newEnv)
           self.generator.addExpression(temp1,temp1,'1','+')
           self.instruct.generator = self.generator
           self.instruct.compile(newEnv)
           self.generator.addGoto(continueLbl)
           self.generator.addLabel(endLbl)
        else:
            if leftVal.type == typeExpression.STRING:
                moveTemp = self.generator.newTemp()
                puntero = self.generator.newTemp()
                continueLbl = self.generator.newLabel()
                endLbl = self.generator.newLabel()

                self.generator.addExpression(puntero,leftVal.value,'1','+')
                self.generator.addGetHeap(moveTemp,puntero)
                self.generator.addLabel(continueLbl)
                self.generator.addIf(moveTemp,'-1','==',endLbl)
                newEnv = Environment(env)
                newEnv.breakLbl = endLbl
                newEnv.continueLbl = continueLbl
                self.generator.addGetHeap(moveTemp,puntero)
                litTemp1 = Literal(typeExpression.CHAR,moveTemp,self.row,self.column)
                litTemp1.generator = self.generator
                declaration = Declaration(self.varTemp,litTemp1,litTemp1.type)
                declaration.generator = self.generator
                declaration.compile(newEnv)
                self.generator.addExpression(puntero,puntero,'1','+')
                self.instruct.generator = self.generator
                self.instruct.compile(newEnv)
                self.generator.addGoto(continueLbl)
                self.generator.addLabel(endLbl)
            elif leftVal.type == typeExpression.ARRAY:
                tipo = typeExpression.FLOAT

                moveTemp = self.generator.newTemp()
                puntero = self.generator.newTemp()
                contador = self.generator.newTemp()
                maximo = self.generator.newTemp()
                continueLbl = self.generator.newLabel()
                endLbl = self.generator.newLabel()

                self.generator.addGetHeap(maximo,leftVal.value)
                self.generator.addExpression(puntero,leftVal.value,'1','+')
                self.generator.addExpression(contador,contador,'1','+')
                self.generator.addLabel(continueLbl)
                self.generator.addIf(contador,maximo,'>',endLbl)
                newEnv = Environment(env)
                newEnv.breakLbl = endLbl
                newEnv.continueLbl = continueLbl
                self.generator.addGetHeap(moveTemp,puntero)
                litTemp1 = NumberVal(tipo,moveTemp,self.row,self.column)
                litTemp1.generator = self.generator
                declaration = Declaration(self.varTemp,litTemp1,litTemp1.type)
                declaration.generator = self.generator
                declaration.compile(newEnv)
                self.generator.addExpression(puntero,puntero,'1','+')
                self.generator.addExpression(contador,contador,'1','+')
                self.instruct.generator = self.generator
                self.instruct.compile(newEnv)
                declaration.compile(newEnv)

                self.generator.addGoto(continueLbl)
                self.generator.addLabel(endLbl)
                print(leftVal)
            else:
                print("no se puede iterar el obejto")   
                errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'Objeto no iterable en For ' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
                

