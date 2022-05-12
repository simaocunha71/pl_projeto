import ply.lex as lex


tokens = ["VARIABLE","WORD","CONST","IF","ENDIF","ELSEIF","ELSE","FOR","ENDFOR","ENDCONDITION"]
literals = ["$", "(", ")", "{", "}", "-", ".", "=",":"]

t_ignore = "\r"

states = [
  ("condition","inclusive")
]

# LEXICO

def t_IF(t):
    r'\$if\('
    t.lexer.push_state("condition")
    return t

def t_ENDIF(t):
    r'\$endif\$(\n)?'
    return t

def t_ELSEIF(t):
    r'\$elseif\('
    t.lexer.push_state("condition")
    return t

def t_ELSE(t):
    r'\$else\$(\n)?'
    return t

def t_FOR(t):
    r'\$for\('
    t.lexer.push_state("condition")
    return t

def t_ENDFOR(t):
    r'\$endfor\$(\n)?'
    return t


def t_condition_ENDCONDITION(t):
  r'\)\$(\n)?'
  t.lexer.pop_state()
  return t

def t_VARIABLE(t):
    r'\$[\w]([._-]?[\w\d]+)*\$'
    return t

def t_WORD(t):
    r'[\w]([._-]?[\w\d]+)*'
    return t

def t_CONST(t):
    r'[^$]|\$\$'
    return t

def t_error(t):
    print("Ta Mal", t)
