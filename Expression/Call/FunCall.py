
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Value import  Value
from Environment.Contexto import errorList

class FunCall(Expression):

    def __init__(self, id ,  params, row, column) -> None:
        super().__init__()
        self.id = id
        self.params = params

    
    def compile(self,env:Environment):
        try:
            func = env.getFunc(self.id)
            if func is not None:
                paramValues = []
                size = env.size
                for param in self.params:
                    param.generator = self.generator
                    paramValues.append(param.compile(env))
                temp = self.generator.newTemp()
                self.generator.addExpression(temp,'P',size+1,'+')
                aux = 0
                for param in paramValues:
                    aux = aux + 1
                    self.generator.addSetStack(temp,param.value)
                    if aux != len(paramValues):
                        self.generator.addExpression(temp,temp,'1','+')
                self.generator.addNextStack(size)
                self.generator.callFunc(self.id)
                self.generator.addGetStack(temp,'P')
                self.generator.addBackStack(size)
                return Value(temp, True, func.type)
            else:
                struct = env.getStruct(self.id)
                if struct  is not None:
                    self.strucType = self.id
                    returnTemp = self.generator.newTemp()
                    self.generator.addExpression(returnTemp, 'H','','')
                    aux = self.generator.newTemp()
                    self.generator.addExpression(aux, returnTemp,'','')
                    self.generator.addExpression('H','H',len(struct),'+')
                    for att in self.params:
                        att.generator = self.generator
                        value = att.comile(env)
                        if value.type != typeExpression.BOOL:
                            self.generator.addSetHeap(aux,value.value)
                        else:
                            returnLbl = self.generator.newLabel()
                            self.generator.addLabel(value.trueLbl)
                            self.generator.addSetHeap(aux,'1')
                            self.generator.addGoto(returnLbl)
                            self.generator.addLabel(value.falseLbl)
                            self.generator.addSetHeap(aux,'0')
                            self.generator.addLabel(returnLbl)
                        self.generator.addExpression(aux,aux,'1','+')
                    return Value(returnTemp,True,typeExpression.STRUCT, self.strucType)
            
        except Exception as e:
            print("no se puede llamarla funcion",e)   
            errorList.append(
                    {
                        "tipo":"Error Interno", 
                        "descripcion" : f'Error de llamada de funcion' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })

        