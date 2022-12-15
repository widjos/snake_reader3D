# ------------------------------ SCANNER ------------------------------

reservadas = {
    'println' : 'PRINTLN',
    'print' : 'PRINT',
    'while' : 'WHILE',
    'for'   : 'FOR',
    "if"    : "IF",
    "in"    : "IN",
    "elif"  : "ELIF",
    "else"  : "ELSE",
    "None"  : "NONE",
    "int"   : "INT",
    "float" : "FLOAT",
    "bool"  : "BOOL",
    "str"   : "STR",
    "upper" : "UPPER",
    "lower" : "LOWER",
    "len"   : "LEN",
    "def"   : "DEF",
    "break" : "BREAK",
    "continue"  : "CONTINUE",
    "return"    : "RETURN",
    "end"       : "END",
    "true"      : "TRUE",
    "false"     : "FALSE"
}

tokens = [
    'LINEANUEVA',
    'DOSPT',
    'PUNTO',
    'COMA',
    'LLAVIZQ',
    'LLAVDER',
    'CORCHETEIZQ',
    'CORCHETEDER',
    'PARIZQ',
    'PARDER',
    #operators
    'ASIG',
    'MAS',
    'MENOS',
    'DIV',
    'MULT',
    'POTENCIA',
    'MODULO',
    #RELACIONALES
    'MENQUE',
    'MENIGUALQUE',
    'MAYQUE',
    'MAYIGUALQUE',
    'OR',
    'AND',
    'NOT',
    'IGUAL',
    'NIGUAL',
    #DATOS
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
] + list(reservadas.values())

t_LINEANUEVA = r'\n'
t_DOSPT  = r':'
t_PUNTO = r'\.'
t_COMA = r','
t_LLAVIZQ = r'{'
t_LLAVDER = r'}'
t_CORCHETEIZQ = r'\['
t_CORCHETEDER = r']' 
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS    = r'\+'
t_MENOS  = r'-'
t_DIV  = r'/'
t_MULT  = r'\*'
t_POTENCIA = r'\^'
t_MODULO = r'%'
t_MENQUE = r'<'
t_MENIGUALQUE = r'<='
t_MAYQUE = r'>'
t_MAYIGUALQUE = r'>='
t_OR = r'or'
t_AND = r'and'
t_NOT = r'not'
t_IGUAL = r'=='
t_NIGUAL = r'!='
t_ASIG = r'='

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

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # remuevo las comillas
    return t

def t_COMENTARIO_MULTILINEA(t):  # Comentario de múltiples líneas #= .. =#
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_SIMPLE(t):  # Comentario simple # ...
    r'\#.*\n'
    t.lexer.lineno += 1     
# Character ignored
t_ignore = " \t"

#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += t.value.count("\n")

# Lexical Error 
def t_error(t):
    print("Illegal character '%s'" % t.value[0] ,  t.lexer.lineno)
    t.lexer.skip(1)

from Environment.Value import Value
from Expression.Arithmetic.Module import Module
from Expression.Arithmetic.Power import Power
from Expression.Primitive.VariableCall import VariableCall
from Expression.Relational.GEThan import GEqualThan
from Expression.Relational.GThan import GThan
from Expression.Relational.LEThan import LEqualThan
from Expression.Relational.LThan import LThan
from Expression.Relational.NotEqual import NotEqual
from Generator.Generator import Generator
from Enum.typeExpression import typeExpression
from Expression.Primitive.NumberVal import NumberVal
from Instruction.Cycles.While import While
from Instruction.Declaration import Declaration
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
    ('left','OR'),
    ('left','AND'),
    ('left','IGUAL', 'NIGUAL'),
    ('left','MAYQUE', 'MENQUE', 'MAYIGUALQUE', 'MENIGUALQUE'),
    ('left','MAS','MENOS'),
    ('left','MULT','DIV', 'MODULO'),
    ('left','POTENCIA'),
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

  
#                    | asignacion_instr LINEANUEVA
#                    | asignacion_arreglo_instr LINEANUEVA
#                    | definicion_asignacion_instr LINEANUEVA
#                    | call_function LINEANUEVA
#                    | declare_function LINEANUEVA
#                    | return LINEANUEVA
#                    | break LINEANUEVA
#                    | continue LINEANUEVA
#                    | if LINEANUEVA 
#                    | for LINEANUEVA

def p_instruccion(t):
    ''' instruccion : printl LINEANUEVA
                    | asignacion LINEANUEVA
                    | declaracion LINEANUEVA
                    | while LINEANUEVA
                    | nativas LINEANUEVA
    ''' 
    t[0] = t[1]

def p_println(t):
    '''printl : PRINTLN PARIZQ expression PARDER'''
    t[0] = Println(t[3])

def p_while(t):
    'while : WHILE expression l_instruccion'
    t[0] = While(t[2], t[3]);   

def p_expression(t):
    '''expression : expression MAS expression 
                 | expression MENOS expression
                 | expression MULT expression
                 | expression DIV expression
                 | expression IGUAL expression
                 | expression MODULO expression
                 | expression POTENCIA expression
                 | expression NIGUAL expression                 
                 | expression MAYQUE expression
                 | expression MENQUE expression
                 | expression MENIGUALQUE expression
                 | expression MAYIGUALQUE expression
                 | expression OR expression
                 | expression AND expression
    '''
    if   t[2] == '+' : t[0] = Plus(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '-' : t[0] = Minus(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '*' : t[0] = Mult(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '/' : t[0] = Div(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '==' : t[0] = Equal(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '%'  : t[0] = Module(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '^'  : t[0] = Power(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '!='  : t[0] = NotEqual(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '>'  : t[0] = GThan(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '<'  : t[0] = LThan(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '<='  : t[0] = LEqualThan(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))
    elif t[2] == '>='  : t[0] = GEqualThan(t[1],t[3], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))




def p_expression_decimal(t):
    'expression : DECIMAL'
    t[0] = NumberVal(typeExpression.FLOAT,t[1], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))

def p_expression_integer(t):
    'expression : ENTERO'
    t[0] = NumberVal(typeExpression.INT, t[1], t.lexer.lineno,find_column(t.lexer.lexdata,t.lexer))

def p_expression_id(t):
    'expression : ID'
    t[0] = VariableCall(t[1])     

def p_asignacion(t):
    '''asignacion : ID ASIG expression'''
    t[0] = Declaration(t[1],t[3], None )

def p_declaracion(t):
    '''declaracion : ID DOSPT tipo ASIG expression'''
    t[0] = Declaration(t[1],t[5],t[3] )                   


def p_nativas(t):
    '''nativas          : UPPER PARIZQ expression PARDER
                        | LOWER PARIZQ expression PARDER
                        | STR PARIZQ expression PARDER
                        | FLOAT PARIZQ expression PARDER
                        | LEN PARIZQ expression PARDER
                        '''

def p_tipo(t):
    '''tipo     : INT
                | FLOAT
                | BOOL
                | STR
                | NONE
    '''
    if   t[1] == 'int'   : Value('0', False, typeExpression.INT)
    elif t[1] == 'float' : Value('0',False, typeExpression.FLOAT)
    elif t[1] == 'bool'  : Value('0',False, typeExpression.BOOL)
    elif t[1] == 'str'   : Value('0',False, typeExpression.STRING)
    elif t[1] == 'None'  : Value('0',False, typeExpression.NULL)


def p_exp_list_instr(t):
    '''exp_list         : exp_list COMA expression
                        | expression'''
#------------------- Fin de ------------

def p_error(t):
    if not t:
        print("End of File!")
        return

    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()             # Get the next token
        #listaErrores.append({"tipo":"Error Sintactico", "descripcion" : "No se esperaba "+ str(t.value), "fila":  t.lexer.lineno , "columna": find_column(t.lexer.lexdata,t.lexer) })
        if not tok or tok.type == 'END':
            break
    parser.restart()    
    print("====> Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()