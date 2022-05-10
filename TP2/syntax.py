import ply.yacc as yacc
import expand_T1

"""
    
def p_grammar(p):
      
    prog : comandos

    comandos : 
            | comandos VARIABLE
            | comandos WORD
            | comandos CONST
            | comandos IF WORD ENDCONDITION comandos alternative ENDIF 
            | comandos FOR WORD ENDCONDITION comandos ENDFOR 

    alternative : condition_sing
                | condition_rec

    condition_sing : ELSE comandos

    condition_rec :
                  | condition_rec ELSEIF WORD  ENDCONDITION  comandos 
           
"""

id = 1

def p_prog(p):
  "prog : comandos"
  p[0] = p[1]

def p_comandos_vazios(p):
  "comandos : "
  p[0] = ""

def p_comandos_VARIABLE(p):
  "comandos : comandos VARIABLE"
  p[0] = p[1] +  f'(VAR,"{p[2]}")' 

def p_comandos_WORD(p):
  "comandos : comandos WORD"
  p[0] = p[1] + f'(CONS,"{p[2]}")' 


def p_comandos_CONST(p):
  "comandos : comandos CONST"
  p[0] = p[1] + f'(CONS,"{p[2]}")'  

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
  "condition_rec : condition_rec ELSEIF WORD  ENDCONDITION  comandos"
  p[0] = f'(ELSEIF,"{p[3]}")' + p[4] + p[5]


def p_error(p):
    print(f"Syntax error! -> {p}")
    expand_T1.error = True