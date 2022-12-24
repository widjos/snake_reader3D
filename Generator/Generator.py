
from Environment.Environment import Environment

class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.natives = []
        self.functions = []
        self.tempList = []
        self.printString = False
        self.printArray = False
        self.inNatives = False
        self.inFunction = False
        self.toUpper = False
        self.toLower = False


    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)

    def getCode(self) -> str:
        tempCode:str = 'package main\n\n'
        tempCode += "import (\n\t\"fmt\"\n\t\"math\"\n)\n\n"

        tempCode += self.addPrintFalse()
        tempCode += self.addPrintTrue()
        tempCode += self.addPointers()
        tempCode += self.addStack()
        tempCode += self.addHeap()

        #obtain the generated code
        if len(self.tempList) > 0 :
            tempCode = tempCode + "var " + self.getUsedTemps() +" float64"+ "\n\n"
        
        tempCode += '\n'.join(self.natives)    
        tempCode += 'func main(){\n\n'
        tempCode += '\n'.join(self.code)
        tempCode += '\t\t\nreturn\n\n}'
        return tempCode    

    def newTemp(self) -> str:
        temp = "t" + str(self.temporal)
        self.temporal += 1

        #save for declaration
        self.tempList.append(temp)
        return temp 

    def newLabel(self) -> str:
        temp = "L" + str(self.label)
        self.label += 1
        return  temp 

    #Add Stack
    def addStack(self):
        return "var STACK [3010199] float64\n"

    #Add Heap
    def addHeap(self):
        return "var HEAP [3010199] float64\n"
    
    #Add pointers
    def addPointers(self):
        return 'var H, P float64\n'

    def writeCode(self, code:str):                              #Metodo para decidir donde escribir el codigo
        if(self.inNatives):
            if(len(self.natives) == 0):
                self.natives.append('// -----NATIVES --------')
            self.natives.append(code)
        elif(self.inFunction):
            if(len(self.functions) == 0):
                self.functions.append('// ----- FUNCTIONS --------')
            self.functions.append(code)
        else:
            self.code.append(code);     


    #Add the label to the code 
    def addLabel(self, label:str):
        self.writeCode(label + ":")           

    #Power operation
    def addMod(self, target:str, left:str, right:str):
        self.writeCode(f'     {target} = math.Mod({left,right});')

    def addPowerOperation(self, target:str, left:str, right: str ):
        self.writeCode(f"     {target} =  math.Pow({left}, {right})")

    def addExpression(self, target:str , left: str, right: str, operator: str):
        self.writeCode(f"     {target} =  {left} {operator} {right} ;")

    #Println 
    def addPrintf(self , typePrint: str , value:str):
        self.writeCode(f"     fmt.Printf(\"%{typePrint}\", int64({value}) );")

    def addPrintFloat(self,value:str):
        self.writeCode(f"     fmt.Printf(\"%f\", {value});")

    def addIf(self, left:str , right:str , operator:str, label: str):
        self.writeCode(f'     if( {left}  {operator}  {right} ) {{ goto {label} }}')

    def addGoto(self, label:str):
        self.writeCode(f'     goto {label} ')

    def addComment(self, label:str):
        self.writeCode(f'     //{label}')

    #Agrega espacio al codigo
    def addSpaceInCode(self):
        self.writeCode('\n')

    #NewLine
    def addNewLine(self):
        self.writeCode(f'     fmt.Printf(\"%c\", 10)')

    def addGetHeap(self, tarjet:str ,  index: str):
        self.writeCode(f'     {tarjet} = HEAP[ int64({index})]')

    def addGetStack(self, tarjet:str , index:str):
        self.writeCode(f'     {tarjet} = STACK[int64({index})]')

    def addSetStack(self, index:str, value:str):
        self.writeCode(f'     STACK[int64({index})] = {value}')

    def addNextStack(self, index:str):
        self.writeCode(f'     P = P + {index}')

    def addBackStack(self, index:str):
        self.writeCode(f'     P = P - {index}')
                
    def addSetHeap(self, index:str, value:str):
        self.writeCode(f'     HEAP[int64({index})] = {value}')                 

    def addNextHeap(self):
        self.writeCode('      H = H + 1')

    def callFunc(self, name:str):
        self.writeCode(f'     {name}()')

    #Funciones para crear
    def addBeginFunction(self, id:str):
        if not self.inNatives:
            self.inFunction = True
        self.natives.append(f'func {id}(){{')

    def addEndFunction(self):
        self.natives.append(f'\t\treturn;\n}}\n\n')
        if not self.inNatives:
            self.inFunction = False        


    def fnPrintString(self):
        if self.printString:
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunction('printString')
        returnLbl = self.newLabel()              #Label para salir de la funcion
        compareLbl = self.newLabel()             # Label para comparacion para buscar un fin de cadena
        tempP = self.newTemp()                   # Temporal puntero para el stack
        tempH = self.newTemp()                   # Puntero temporal a Heap

        self.addExpression(tempP, 'P', '1', '+')

        self.addGetStack(tempH,tempP)

        tempC = self.newTemp()                  # Temporal para comparar
        self.addLabel(compareLbl)
        self.addGetHeap(tempC,tempH)
        self.addIf(tempC, '-1', '==', returnLbl)
        self.addPrintf('c', tempC)

        self.addExpression(tempH, tempH, '1', '+')
        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.addEndFunction()
        self.inNatives = False

    def fnPrinArray(self):
        trigger1 = False
        trigger2 = False
        self.fnPrintString()

        if(self.printArray):
            return
        
        self.printArray = True
        self.inNatives = True
        self.addBeginFunction('printArray')
        
        returnLbl = self.newLabel()             # Salir de la funcion
        compareLbl = self.newLabel()            # Comparar cuando termina el arrego
        printS     = self.newLabel()            #
        printA      = self.newLabel()           #Label para arreglos
        tempP       = self.newTemp()       
        tempH       = self.newTemp()
        
        self.addExpression(tempP,'P','1','+')
        self.addGetStack(tempH,tempP)

        contador = self.newTemp()
        size = self.newTemp()
        self.addGetHeap(size,tempH)

        punteroInicial = self.newTemp()
        self.addExpression(tempH,tempH,'1','+')
        tempC = self.newTemp()
        self.addPrintf('c',91)
        self.addLabel(compareLbl)
        self.addGetHeap(tempC,tempH)
        self.addExpression(punteroInicial,tempC,'','')
        self.addIf(contador,size, '>=', returnLbl)

        for element in Environment.heapA:
            self.addIf(element,punteroInicial,'==',printA)
            trigger1 = True
        for element in Environment.heapS:
            self.addIf(element, tempC, '==', printS)
            trigger2 = True
        self.addPrintFloat(tempC)
        self.addPrintf('c',44)
        self.addExpression(tempH,tempH,'1','+')
        self.addExpression(contador,contador,'1','+')
        self.addGoto(compareLbl)

        if(trigger1):
            self.addLabel(printA)

            tempAuxP = self.newTemp()
            tempAuxCont = self.newTemp()        
            tempAuxTam = self.newTemp()        
            tempAuxC = self.newTemp()        
            tempAuxPP = self.newTemp()        
            tempAuxH = self.newTemp()

            self.addExpression(tempAuxP,'P','','')        
            self.addExpression(tempAuxCont,contador,'','')        
            self.addExpression(tempAuxTam,size,'','')        
            self.addExpression(tempAuxC,tempC,'','')        
            self.addExpression(tempAuxPP,tempP,'','')        
            self.addExpression(tempAuxH,tempH,'','')        
            self.addExpression(contador,'0','','')
            
            self.addSetStack(tempP,tempC)
            self.callFunc("printArray")

            self.addExpression(contador,tempAuxCont,'1','+')        
            self.addExpression(size,tempAuxTam,'','')        
            self.addExpression(tempC,tempAuxC,'','')        
            self.addExpression(tempP,tempAuxPP,'','')        
            self.addExpression(tempH,tempAuxH,'1','+')

            self.addGoto(compareLbl)

        if(trigger2):
            self.addLabel(printS)

            tempAuxP = self.newTemp()
            tempAuxCont = self.newTemp()        
            tempAuxTam = self.newTemp()        
            tempAuxC = self.newTemp()        
            tempAuxPP = self.newTemp()        
            tempAuxH = self.newTemp()              

            self.addExpression(tempAuxP,'P','','')        
            self.addExpression(tempAuxCont,contador,'','')        
            self.addExpression(tempAuxTam,size,'','')        
            self.addExpression(tempAuxC,tempC,'','')        
            self.addExpression(tempAuxPP,tempP,'','')        
            self.addExpression(tempAuxH,tempH,'','')

            self.addSetStack(tempP,tempC)
            self.callFunc("printString")    

            self.addExpression('P',tempAuxP,'','')
            self.addExpression(contador,tempAuxCont,'1','+')        
            self.addExpression(size,tempAuxTam,'','')        
            self.addExpression(tempC,tempAuxC,'','')        
            self.addExpression(tempP,tempAuxPP,'','')        
            self.addExpression(tempH,tempAuxH,'1','+')
            self.addPrintf('c',44)

            self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.addPrintf('c',93)
        self.addExpression(contador,'0','','')
        self.addEndFunction()
        self.inNatives = False

    def fToUpper(self):
        if(self.toUpper):
            return
        self.toUpper = True
        self.inNatives = True

        self.addBeginFunction('toUpper')
        returnLbl = self.newLabel()
        compareLbl = self.newLabel()

        tempP = self.newTemp()
        tempH = self.newTemp()

        self.addExpression(tempP,'P','1','+')
        self.addGetStack(tempH,tempP)

        tempC = self.newTemp()

        self.addLabel(compareLbl)
        self.addGetHeap(tempC,tempH)
        self.addIf(tempC, '-1','==',returnLbl)

        temp = self.newTemp()
        passLabel = self.newLabel()
        self.addIf(tempC,'97','<',passLabel)   
        self.addIf(tempC,'122','>',passLabel)
        self.addSetHeap(passLabel)
        self.addLabel(passLabel)
        self.addExpression(tempH,tempH,'1','+')

        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.addEndFunction()
        self.inNatives =  False 

    def fToLower(self):
        if(self.toLower):
            return
        self.toLower = True
        self.inNatives = True

        self.addBeginFunction('toLower')

        returnLbl = self.newLabel()
        compareLbl = self.newLabel()

        tempP = self.newTemp()
        tempH = self.newTemp()
        self.addExpression(tempP,'P','1','+')

        self.addGetStack(tempH,tempP)
        tempC = self.newTemp()

        self.addLabel(compareLbl)
        self.addGetHeap(tempC,tempH)
        self.addIf(tempC,'-1','==',returnLbl)

        temp = self.newTemp()
        passLabel = self.newLabel()
        self.addIf(tempC,'65','<',passLabel)
        self.addIf(tempC,'90','>',passLabel)
        self.addExpression(temp,tempC,'32','+')

        self.addSetHeap(tempH,temp)
        self.addLabel(passLabel)
        self.addExpression(tempH,tempH,'1','+')

        self.addGoto(compareLbl)

        self.addLabel(returnLbl)
        self.addEndFunction()
        self.inNatives =False      
    

    def addPrintFalse(self):
        return '''
func widPrintFalse(){ 
    fmt.Printf("%c",102)
    fmt.Printf("%c",97)
    fmt.Printf("%c",108)
    fmt.Printf("%c",115)
    fmt.Printf("%c",101)
    return
}\n\n'''

    def addPrintTrue(self):
        return '''
func widPrintTrue(){ 
    fmt.Printf("%c",116)
    fmt.Printf("%c",114)
    fmt.Printf("%c",117)
    fmt.Printf("%c",101)
    return
}\n\n'''
   
       
