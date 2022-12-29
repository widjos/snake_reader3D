from Abstract.Instruction import Instruction
from Environment.Environment import Environment

class CreateStruct(Instruction):

    def __init__(self, id, attributes,line,column) -> None:
        super().__init__()
        self.id = id
        self.atributes = attributes
        self.line = line
        self.column = column

    def compile(self,env:Environment):
        env.saveStruct(self.id,self.atributes)
