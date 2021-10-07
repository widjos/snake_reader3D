from os import write
from Analisys.gramatica import parser



def main():
    f = open("./entrada.txt", "r")
    input = f.read()
    f.close()
    result = parser.parse(input)
    fOut = open("./cd3.go","w")
    fOut.write(result)
    fOut.close()  



if __name__ == "__main__":
    main()
