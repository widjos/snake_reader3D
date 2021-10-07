from Enum.typeExpression import typeExpression

class Value:
    def __init__(self,  value:str , isTemp: bool, type: typeExpression) -> None:
        self.value = value
        self.isTemp = isTemp
        self.type = type
        self.trueLabel = ""
        self.falseLabel = ""

    def getValue(self):
        return self.value    