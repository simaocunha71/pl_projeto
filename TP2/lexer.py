import ply.lex as lex


tokens = ["VARIABLE","WORD","CONST","IF","ENDIF","ELSEIF","ELSE","FOR","ENDFOR","ENDCONDITION"]
literals = ["$", "(", ")", "{", "}", "-", ".", "=",":"]

t_ignore = "\r"


# LEXICO

def t_IF(t):
    r'\$if\('
    return t

def t_ENDIF(t):
    r'\$endif\$(\n)?'
    return t

def t_ELSEIF(t):
    r'\$elseif\('
    return t

def t_ELSE(t):
    r'\$else\$(\n)?'
    return t

def t_FOR(t):
    r'\$for\('
    return t

def t_ENDFOR(t):
    r'\$endfor\$(\n)?'
    return t


def t_ENDCONDITION(t):
  r'\)\$(\n)?'
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
