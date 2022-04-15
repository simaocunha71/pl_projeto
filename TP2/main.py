"""
Tokens:
   > VAR (variavel)
   > CONST (conteudo a colocar diretamente)
   > if/endif
   > elseif
   > else
   > for
   > endfor

Literals:
   > $
   > (
   > )
   > {
   > }
   > -
   > .

Gramática:

prog : comandos

comandos : 
         |comandos comando
         |$if '(' $VAR$ ')'$ terminator condition $endif$
         |$for '(' $VAR$ ')'$ condition $endfor$

condition:
         | comandos condition
         | condition_sing
         | condition_rec
         

condition_sing: $else$ comandos

condition_rec: $elseif '(' $VAR$ ')'$ comandos condition_rec

terminator:
          | comando terminator

comando :
        | $VAR$
        | $CONST$

"""
import ply.lex as lex
import ply.yacc as yacc

tokens = ["VAR","CONST","IF","ENDIF","ELSEIF","ELSE","FOR","ENDFOR"]
literals = ["$", "(", ")", "{", "}", "-", "."]

t_ignore = "\n\t\r "


# LEXICO

def t_IF(t):
    r'\$if\('
    return t

def t_ENDIF(t):
    r'\$endif\$'
    return t

def t_ELSEIF(t):
    r'\$elseif\('
    return t

def t_ELSE(t):
    r'\$else\$'
    return t

def t_FOR(t):
    r'\$for\('
    return t

def t_ENDFOR(t):
    r'\$endfor\$'
    return t

def t_VAR(t):
    r'[\w\-.]+'
    return t

def t_CONST(t):
    r'[^$(){}]+'
    return t

def t_error(t):
    print("Ta Mal", t)



# SINTAX
""" 
def p_prog(p):
    "prog : comandos"
    print("p0")

def p_comandos_vazios(p):
  "comandos : "
  print("p1")

def p_comandos_terminator(p):
  "comandos : comandos terminator"
  print("p2")

def p_comandos_if(p):
  "comandos : '$' IF '(' VAR ')' '$' terminator condition  '$' ENDIF '$'"
  print("p3")

def p_comandos_for(p):
  "comandos : '$' FOR '(' VAR ')' '$'  condition  '$' ENDFOR '$'"
  print("p4")

def p_condition_vazio(p):
  "condition :"
  print("p5")

def p_condition_cond_sing(p):
  "condition : condition_sing"
  print("p6")

def p_condition_cond_rec(p):
  "condition : condition_rec"
  print("p7")

def p_condition_sing(p):
  "condition_sing : '$' ELSE '$'  comandos"
  print("p8")

def p_condition_rec_vazio(p):
  "condition_rec : "
  print("p9")

def p_condition_rec(p):
  "condition_rec : '$' ELSEIF '('  VAR  ')' '$'  comandos condition_rec"
  print("p10")


def p_terminator_vazio(p):
  "terminator : "
  print("pa")

def p_terminator_var(p):
  "terminator : '$' VAR '$'"
  print("p11")

def p_terminator_const(p):
  "terminator : CONST"
  print("p12")

 """
    
def p_grammar(p):
      """
    prog : comandos

    comandos : 
            | CONST comandos
            | '$' VAR '$' comandos
            | IF VAR ')' '$' comandos alternative ENDIF comandos
            | FOR VAR ')' '$' comandos ENDFOR comandos

    alternative :
            | condition_sing
            | condition_rec

    condition_sing : ELSE comandos

    condition_rec :
                  | ELSEIF VAR  ')' '$'  comandos condition_rec
           
    
               
      """

def p_error(p):
    print(f"Syntax error! -> {p}")


lexer = lex.lex()
parser = yacc.yacc()

import sys


#print("$if(titleblock)$\n$titleblock$\n\n$endif$")
f = open("templates_teste/template_md.txt", "r")

lines = f.read()

line ="""  $if(titleblock)$
$titleblock$

$endif$
$for(header-includes)$
$header-includes$

$endfor$ """

lexer.input(lines)
#for tok in lexer:
#    print("\n \u001B[33m" + str(tok) + "\u001B[0m")



#parser.parse(lines)

parser.parse(lines)

f.close()
