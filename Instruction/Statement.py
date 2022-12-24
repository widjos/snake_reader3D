from Abstract.Instruction import Instruction

class Statement(Instruction):
    def __init__(self, instruct, line, column):
        super().__init__()
        self.instruction = instruct
        self.line = line
        self.column = column

    def compile(self,env):
        for ins in self.instruction:
            ins.generator = self.generator
            ret = ins.compile(env)
            if ret is not None:
                return ret