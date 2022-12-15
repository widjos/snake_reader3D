
from  Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol

class Environment:

    variables = {}
    functions = {}
    structs = {}
    errores = []
    entrada = []
    heapS = []
    heapA = []

    def __init__(self, father) -> None:
        self.father = father
        self.variable = {}
        self.size = 0

        if father != None:
            self.size = father.size


    def saveVariable(self , id: str , type: typeExpression):
        if self.variable.get(id) != None:
            print(f'La variable {id}  ya existe')
            return

        tempVar = Symbol(id, type , self.size) 
        self.size +=  1
        self.variable[id] = tempVar
        return tempVar

    def getVariable(self, id:str) -> Symbol:
        tempEnv = self
        while(tempEnv != None):
            if  tempEnv.variable.get(id) != None:
                return tempEnv.variable.get(id)
            tempEnv = tempEnv.father
        print(f'error la variable {id} no existe')
        return None 


