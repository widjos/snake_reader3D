class Symbol:

    def __init__(self, id:str, type, position, isGlobal=False, inHeap= False, structType='', posHeap= False ):
        self.id = id
        self.type = type 
        self.position = position
        self.isGlobal = isGlobal
        self.inHeap = inHeap
        self.structType = structType
        self.posHeap = posHeap
        self.value = None

    def getId(self):
        return self.id

    def getPosition(self):
        return self.position

    def getType(self):
        return self.type

        