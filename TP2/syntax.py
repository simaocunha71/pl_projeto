import ply.yacc as yacc
import expand_T1

"""
    
def p_grammar(p):
      
    prog : comandos                                                       # terminador

    comandos :                                                            # comando vazio
            | comandos VARIABLE                                           # variavel
            | comandos PARTIAL                                            # partial (subtemplate)
            | comandos PIPE                                               # pipe (metodos aplicados a variavel)
            | comandos WORD                                               # texto que se escreve diretamente no ficheiro
            | comandos COMMENTBEGIN comentarios COMMENTEND                # linha de comentario
            | comandos CONST                                              # texto que se escreve diretamente no ficheiro
            | comandos IF WORD ENDCONDITION comandos alternative ENDIF    # condiçao if, formato if('variavel') ... endif
            | comandos FOR WORD ENDCONDITION comandos ENDFOR              # condiçao for, formato for('variavel') ... endfor

    comentarios :                                                         # comentario vazio
                | comentarios COMMENT                                     # comentario (recursivo por se ler char a char)


    alternative : condition_sing                                          # regra de else
                | condition_rec                                           # regra de elif

    condition_sing : ELSE comandos                                        # else

    condition_rec :                                                       # vazio (no caso de nao ter condicional else)
                  | ELSEIF WORD  ENDCONDITION  comandos condition_rec     # condicionais elif recursivamente
                  | ELSEIF WORD  ENDCONDITION  comandos condition_sing    # elif seguido de else
           
"""

id = 1
tabs = 0

def p_prog(p):
  "prog : comandos"
  p[0] = p[1]

def p_comandos_vazios(p):
  "comandos : "
  p[0] = ""

def p_comandos_VARIABLE(p):
  "comandos : comandos VARIABLE"
  p[0] = p[1] +  f'(VAR,"{p[2]}")' 

def p_comandos_PARTIAL(p):
  "comandos : comandos PARTIAL"
  p[0] = p[1] +  f'(PARTIAL,"{p[2]}")' 

def p_comandos_PIPE(p):
  "comandos : comandos PIPE"
  p[0] = p[1] +  f'(PIPE,"{p[2]}")' 

def p_comandos_WORD(p):
  "comandos : comandos WORD"
  p[0] = p[1] + f'(CONS,"{p[2]}")' 

def p_comandos_comentarios(p):
  "comandos : comandos COMMENTBEGIN comentarios COMMENTEND"
  p[0] = p[1]


def p_comandos_CONST(p):
  "comandos : comandos CONST"
  cons = p[2]
  if cons == '$$':
    cons = '$'
  p[0] = p[1] + f'(CONS,"{cons}")' 


def p_comandos_if(p):
  "comandos : comandos IF WORD ENDCONDITION comandos alternative ENDIF"
  global id
  p[0] = p[1] + f'(IF{id},"{p[3]}")' + p[5] + p[6] + f"(ENDIF{id})"
  id+=1


def p_comandos_for(p):
  "comandos : comandos FOR WORD ENDCONDITION comandos ENDFOR "
  global id
  p[0] = p[1] + f'(FOR{id},"{p[3]}")' + p[5] + p[6] + f"(ENDFOR{id})"
  id+=1


def p_comentarios_EMPTY(p):
  "comentarios : "

def p_comentarios_mult(p):
  "comentarios : comentarios COMMENT"


def p_alternative_cond_sing(p):
  "alternative : condition_sing"
  p[0] = p[1]

def p_alternative_cond_rec(p):
  "alternative : condition_rec"
  p[0] = p[1]
  

def p_condition_sing(p):
  "condition_sing : ELSE comandos"
  p[0] = "(ELSE)" + p[2]

def p_condition_rec_vazio(p):
  "condition_rec : "
  p[0] = ""

def p_condition_rec(p):
  "condition_rec : ELSEIF WORD  ENDCONDITION  comandos condition_rec"
  p[0] = f'(ELSEIF,"{p[3]}")' + p[4] + p[5]

def p_condition_rec_sing(p):
  "condition_rec : ELSEIF WORD  ENDCONDITION  comandos condition_sing"
  p[0] = f'(ELSEIF,"{p[3]}")' + p[4] + p[5]


def p_error(p):
    print(f"Syntax error! -> {p}")
    expand_T1.error = True