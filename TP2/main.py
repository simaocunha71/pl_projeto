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

t_ignore = " \n\t\r"

def t_IF(t):
    r'IF'
    return t

def t_endif(t):
    r'endif'
    return t

def t_elseif(t):
    r'elseif'
    return t

def t_else(t):
    r'else'
    return t

def t_for(t):
    r'for'
    return t

def t_endfor(t):
    r'endfor'
    return t

def t_VAR(t):
    r'\w+'
    return t

def t_CONST(t):
    r'.+'
    return t

def t_error(t):
    print("Ta Mal", t.value[0])

def p_grammar(p):
  """
prog : comandos

comandos : 
         | comandos terminator
         | '$' IF '(' VAR ')' '$' terminator condition  '$' ENDIF '$' 
         | '$' FOR '(' VAR ')' '$'  condition  '$' ENDFOR '$' 

condition :
          | comandos condition
          | condition_sing
          | condition_rec
         

condition_sing :  '$' ELSE '$'  comandos

condition_rec :
              | '$' ELSEIF '('  VAR  ')' '$'  comandos condition_rec

terminator :
           | comando terminator

comando :
        | '$' VAR '$' 
        | CONST
  """

def p_error(p):
    print(f"Syntax error! -> {p.value}")

lexer = lex.lex()
parser = yacc.yacc()

import sys
"""
for lines in sys.stdin:
  lexer.input(lines)
  for tok in lexer:
    print("\n \u001B[33m" + str(tok) + "\u001B[0m")
"""

f = open("templates_teste/template_md.txt", "r")
parser.parse(f.read())
f.close()
