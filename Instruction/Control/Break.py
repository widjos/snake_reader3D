from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Contexto import errorList


class Break(Instruction):
    def __init__(self, line,column) -> None:
        super().__init__()
        self.row = line
        self.column = column

    def compile(self,environemnt:Environment):
        if environemnt.breakLbl == '':
            print("")
            errorList.append(
                    {
                        "tipo":"Error Semantico", 
                        "descripcion" : f'Break fuera de ciclo' , 
                        "fila":  self.row , 
                        "columna": self.column 
                    })
        self.generator.addGoto(environemnt.breakLbl) 
