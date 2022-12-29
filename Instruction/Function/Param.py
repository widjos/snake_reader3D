from Abstract.Instruction import Instruction

class Param(Instruction):

    def __init__(self, id, type, row,column,structType:str='') -> None:
        super().__init__()
        self.id = id
        self.type = type
        self.structType = structType

    def compile(self,env):
        return self