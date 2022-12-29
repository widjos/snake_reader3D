from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Generator.Generator import Generator
from Environment.Value import Value


class AccesArray(Expression):
    def __init__(self, id, indexs,line,column) -> None:
        super().__init__()
        self.id = id
        self.indexs = indexs

    
    def compile(self,env):
        self.generator.addComment('Compilacion de acceso')
        array = env.getVariable(self.id)
        if array is None:
            print("no existe el arreglo")
            return

        temp  = self.generator.newTemp()
        tempPos = array.position
        self.generator.addGetStack(temp,tempPos)
        tipo = typeExpression.BOOL
        for element in self.indexs:
            element.generator = self.generator
            elemento = element.compile(env)
            sumado = self.generator.newTemp()
            lenght = self.generator.newTemp()
            self.generator.addGetHeap(lenght,temp)
            self.generator.addExpression(sumado,elemento.value, temp , '+')
            #Error
            self.agregarError(lenght,elemento.value)
            self.generator.addGetHeap(temp,sumado)

            if(Generator.dict_temp[temp] % 1 != 0):
                if Generator.dict_temp[temp] % 1 == 0.12837:
                    if Generator.heap[int(Generator.dict_temp[temp])] == 0 :
                        tipo = typeExpression.STRING
                    else:
                        tipo = typeExpression.ARRAY
                else:
                    tipo = typeExpression.STRING
            else:
                tipo = typeExpression.INT

        return Value(temp,True,tipo)
    
    def agregarError(self,posicion, index):
        label1 = self.generator.newLabel()
        label2 = self.generator.newLabel()
        self.generator.addIf(posicion,index,'<', label1)

        self.generator.addGoto(label2)
        self.generator.addGoto(label1)
        self.generator.addPrintf('c', 105)  # i
        self.generator.addPrintf('c', 110)  # n
        self.generator.addPrintf('c', 100)  # d
        self.generator.addPrintf('c', 101)  # e
        self.generator.addPrintf('c', 120)  # x
        self.generator.addPrintf('c', 32)
        self.generator.addPrintf('c', 111)  # o
        self.generator.addPrintf('c', 117)  # u
        self.generator.addPrintf('c', 116)  # t
        self.generator.addPrintf('c', 32)
        self.generator.addPrintf('c', 111)  # o
        self.generator.addPrintf('c', 102)  # f
        self.generator.addPrintf('c', 32)
        self.generator.addPrintf('c', 114)  # r
        self.generator.addPrintf('c', 97)   # a
        self.generator.addPrintf('c', 110)  # n
        self.generator.addPrintf('c', 103)  # g
        self.generator.addPrintf('c', 101)  # e
        self.generator.writeCode("return;")

        self.generator.addLabel(label2)

                        
