from Abstract.Instruction import Instruction
from Environment.Environment import Environment

class AssignAccess(Instruction):

    def __init__(self, id, access, expression,line, column) -> None:
        super().__init__()
        self.id = id 
        self.access = access
        self.expression = expression

    
    def compile(self,env:Environment):

        self.expression.generator = self.generator

        val = self.expression.compile(env)
        var = env.getVariable(self.id)
        temp = self.generator.newTemp()

        tempPos = var.position

        self.generator.addGetStack(temp,tempPos)
        struct = var.structType

        if struct != '':
            struct = env.getStruct(struct)
            finalAtt = None
            finalAttPos = 0
            for att in struct:
                if att.id == self.access:
                    finalAtt = att
                    break
                finalAttPos = finalAttPos+1

            tempAux = self.generator.newTemp()
            self.generator.addExpression(tempAux,temp,finalAttPos,'+')
            self.generator.addSetHeap(tempAux,val.value)    
