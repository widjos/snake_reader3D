from Abstract.Instruction import *

class StructAttribute(Instruction):

    def __init__(self, id, type, line,column) -> None:
        super().__init__()
        self.id = id
        self.type = type

    def compile(self,env):
        return self