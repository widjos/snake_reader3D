from os import write

from flask.json import jsonify
from flask import Flask,request
from flask_cors import CORS
import json
from Analisys.gramatica import parser
from Environment.Contexto import errorList
from Environment.Contexto import simbolos
from Environment.Environment import Environment

app = Flask(__name__)
CORS(app)

cors = CORS(app,resources={
    r'/*':{
        "origins":"*"
    }
})

@app.route('/compile',methods=['POST'])
def compile():
    try:
        codePyToPy = request.get_json()["jolc"]
        result = parser.parse(codePyToPy)

        print(simbolos)
        return jsonify({
            'resultado' : result,
            'errores' : errorList,
            'Lobjetos' : simbolos
                 
        })

    except:
        print("Error interno")


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
    #app.run(port=8000,debug=True)