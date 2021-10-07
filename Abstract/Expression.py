from abc import ABC,  abstractclassmethod
from Generator.Generator import Generator
from Environment.Environment import Environment
from Environment.Value import Value 

class Expression(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.generator: Generator = None
        self.trueLabel = ""
        self.falseLabel = ""


    @abstractclassmethod
    def compile(self, environement: Environment) -> Value:
        pass    

