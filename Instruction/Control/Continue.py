from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Contexto import errorList


class Continue(Instruction):
    def __init__(self, line,column) -> None:
        super().__init__()
        self.row = line
        self.column = column

    def compile(self,environemnt:Environment):
        if environemnt.continueLbl == '':
            print("")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'Continue fuera de ciclo' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
        self.generator.addGoto(environemnt.continueLbl) 
