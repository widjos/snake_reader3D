from abc import  ABC , abstractclassmethod
from Environment.Environment import Environment
from Environment.Value import Value
from Generator.Generator import Generator

class Instruction(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.generator = Generator()

    @abstractclassmethod
    def compile(self, environment:Environment) -> Value:
        pass     