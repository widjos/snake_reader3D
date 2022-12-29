from Abstract.Instruction import Instruction

class DeclareStruct(Instruction):
    def __init__(self,id,type,line,column) -> None:
        super().__init__()
        self.id = id
        self.type = type
        self.line = line
        self.column = column