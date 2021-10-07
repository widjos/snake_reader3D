
class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.tempList = []

    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)

    def getCode(self) -> str:
        tempCode:str = 'package main\n\n'
        tempCode += "import \"fmt\"\n\n"

        tempCode += self.addPrintFalse()
        tempCode += self.addPrintTrue()

        #obtain the generated code
        if len(self.tempList) > 0 :
            tempCode = tempCode + "var " + self.getUsedTemps() +" float64"+ "\n\n"
        tempCode += 'func main(){\n\n'
        tempCode += '\n'.join(self.code)
        tempCode += '\nreturn\n\n}'

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

    #Add the label to the code 
    def addLabel(self, label:str):
        self.code.append(label + ":")           


    def addExpression(self, target:str , left: str, right: str, operator: str):
        self.code.append(f"{target} =  {left} {operator} {right} ;")

    #Println 
    def addPrintf(self , typePrint: str , value:str):
        self.code.append(f" fmt.Printf(\"%{typePrint}\", {value} );")

    def addIf(self, left:str , right:str , operator:str, label: str):
        self.code.append(f'if( {left}  {operator}  {right} ) {{ goto {label} }}')

    def addGoto(self, label:str):
        self.code.append(f' goto {label} ')

    #NewLine
    def addNewLine(self):
        self.code.append(f'fmt.Printf(\"%c\", 10)') 

    def callFunc(self, name:str):
        self.code.append(f' {name}()')     

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
   
       
