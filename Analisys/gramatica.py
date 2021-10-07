# ------------------------------ SCANNER ------------------------------

reservadas = {
    'println' : 'PRINTLN'
}

tokens = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    #operators
    'MAS',
    'MENOS',
    'DIV',
    'MULT',
    'IGUAL',
    #DATOS
    'DECIMAL',
    'ENTERO',
    'ID',
] + list(reservadas.values())

t_PTCOMA = r';'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS    = r'\+'
t_MENOS  = r'-'
t_DIV  = r'/'
t_MULT  = r'\*'
t_IGUAL = r'=='

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')    # Check for reserved words
     return t
# Character ignored
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Lexical Error 
def t_error(t):
    print("Illegal character '%s'" % t.value[0] ,  t.lexer.lineno)
    t.lexer.skip(1)

from Generator.Generator import Generator
from Enum.typeExpression import typeExpression
from Expression.Primitive.NumberVal import NumberVal
from Instruction.Println import Println
from Environment.Environment import Environment
from Expression.Arithmetic.Plus import Plus
from Expression.Arithmetic.Minus import Minus
from Expression.Arithmetic.Mult import Mult
from Expression.Arithmetic.Div import Div
from Expression.Relational.Equal import Equal

import ply.lex as lex
lexer = lex.lex()

# ---------------------------------------- PARSER ------------------------

precedence = (
    ('left','MAS','MENOS'),
    ('left','MULT','DIV'),
    ('left','IGUAL')
)



def p_inicio(t):
    ''' inicio : l_instruccion
    '''
    generator : Generator = Generator()
    globalEnv = Environment(None)
    for ins in t[1]:
        ins.generator = generator
        ins.compile(globalEnv)

    t[0] = generator.getCode()     

def p_lista_instruccion(t):
    ''' l_instruccion : l_instruccion instruccion
                      | instruccion
    '''
    if(len(t) == 3):
        t[1].append(t[2])
        t[0] = t[1]
    elif(len(t) == 2):
        t[0] = [t[1]]

def p_instruccion(t):
    ''' instruccion : printl PTCOMA
    ''' 
    t[0] = t[1]

def p_println(t):
    '''printl : PRINTLN PARIZQ expresion PARDER'''
    t[0] = Println(t[3])


def p_expresion(t):
    '''expresion : expresion MAS expresion 
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion IGUAL expresion
    '''
    if   t[2] == '+' : t[0] = Plus(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '-' : t[0] = Minus(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '*' : t[0] = Mult(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '/' : t[0] = Div(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '==' : t[0] = Equal(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))



def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = NumberVal(typeExpression.FLOAT,t[1], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))

def p_expresion_integer(t):
    'expresion : ENTERO'
    t[0] = NumberVal(typeExpression.INT, t[1], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))


#------------------- Fin de ------------

def p_error(t):
    if not t:
        print("End of File!")
        return

    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()             # Get the next token
        #listaErrores.append({"tipo":"Error Sintactico", "descripcion" : "No se esperaba "+ str(t.value), "fila":  t.lexer.lineno , "columna": find_column(t.lexer.lexdata,t.lexer) })
        if not tok or tok.type == 'PTCOMA':
            break
    parser.restart()    
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()