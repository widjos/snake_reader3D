
from  Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Contexto import simbolos 

class Environment:

    variable = {}
    functions = {}
    structs = {}
    errores = []
    entrada = []
    heapS = []
    heapA = []

    def __init__(self, father) -> None:
        self.father = father
        self.variable = {}
        self.structs = {}
        self.size = 0
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        if father is not None:
            self.size = self.father.size
            self.breakLbl = self.father.breakLbl
            self.continueLbl  = self.father.continueLbl
            self.returnLbl = self.father.returnLbl


  #  def saveVariable(self , id: str , type: typeExpression):
  #      if self.variable.get(id) != None:
  #          print(f'La variable {id}  ya existe')
  #          return
  #
  #      tempVar = Symbol(id, type , self.size, self.variable[id].pos ) 
  #      self.size +=  1
  #      self.variable[id] = tempVar
  #      return tempVar

    def saveVariable(self , id: str , type: typeExpression, inHeap, strucType=''):
        env = self
        #Entra aqui si la variable ya existe y solo queda remplazar de nuevo o sobre escribir
        while env is not None:
            if id in env.variable.keys():
                print(f'La variable {id}  ya existe')
                env.variable[id] = Symbol(id,type,env.variable[id].position, env.father == None , inHeap, strucType)
                simbolos.append({
                        "nombre": id,
                        "tipo": type.name, 
                        "position" : env.variable[id].position , 
                        "global":  True, 
                        "inHeap": inHeap
            })
                Environment.variable = env.variable
                return env.variable[id]
            env =env.father
        if(id[-1] == '#'):
            id = id[0:-1]
        tempVar = Symbol(id, type , self.size, self.father == None, inHeap, strucType ) 
        self.size +=  1
        self.variable[id] = tempVar
        simbolos.append({
                        "nombre": id,
                        "tipo": type.name, 
                        "position" : self.size , 
                        "global":  True, 
                        "inHeap": inHeap
        })
        Environment.variable = self.variable
        return self.variable[id]

    def getVariable(self, id:str) -> Symbol:
        tempEnv = self
        while(tempEnv is not None):
            if  id in tempEnv.variable.keys():
                return tempEnv.variable.get(id)
            tempEnv = tempEnv.father
        print(f'error la variable {id} no existe')
        return None 

    def saveFunc(self,idFunc,function):
        if idFunc in self.functions.keys():
            print(f'Error funcion repetida')
        else:
            self.functions[idFunc] = function
            Environment.functions = self.functions
         

    def saveStruct(self,idStruct, attributes):
        if idStruct in self.structs.keys():
            print(f'Struct repetido')
        else:
            self.structs[idStruct] = attributes
    
    def getFunc(self,idFunc):
        env = self
        while env is not None:
            if idFunc in env.functions.keys():
                return env.functions[idFunc]
            env = env.father
        return None

    def getStruct(self,idStruct):
        env = self
        while env is not None:
            if idStruct in env.structs.keys():
                return env.structs[idStruct]
            env = env.father
        
        return None

             
