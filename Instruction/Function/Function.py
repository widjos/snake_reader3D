from Abstract.Instruction import Instruction
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment

class Function(Instruction):
    def __init__(self,id, params, type, instructions,row,column) -> None:
        super().__init__()

        self.id = id
        self.params = params
        self.type = type
        self.instruct  = instructions

    
    def compile(self,env):
        env.saveFunc(self.id,self)
        newEnv = Environment(env)
        returnLbl = self.generator.newLabel()
        newEnv.returnLbl = returnLbl
        newEnv.size = 1
        for param in self.params:
            newEnv.saveVariable(param.id+'#',param.type, 
                (param.type == typeExpression.STRING or param.type == typeExpression.STRUCT),param.structType
            )
        self.generator.addBeginFunction(self.id)

        try:
            self.instruct.generator = self.generator
            self.instruct.compile(newEnv)
        except Exception as e:
            print("Error al compilar", e)
        if self.type != typeExpression.NULL:
            self.generator.addLabel(returnLbl)
        self.generator.addEndFunction()