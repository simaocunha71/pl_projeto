import ply.lex as lex


tokens = ["VARIABLE","COMMENTBEGIN","COMMENTEND","COMMENT","PIPE",
          "PARTIAL","WORD","CONST","IF","ENDIF","ELSEIF","ELSE",
          "FOR","ENDFOR","ENDCONDITION"]
literals = ["$", "(", ")", "{", "}", "-", ".", "=",":"]

t_ANY_ignore = "\r"

states = [
  ("condition","inclusive"),
  ("conditionAlt","inclusive"),
  ("comment","exclusive")
]

# LEXICO

def t_COMMENTBEGIN(t):
    r'\$--'
    t.lexer.push_state("comment")
    return t

def t_comment_COMMENTEND(t):
    r'\n|.$'
    t.lexer.pop_state()
    return t

def t_comment_COMMENT(t):
    r'[^\n]'
    return t


def t_IF(t):
    r'(\$if\()|(\$\{if\()'
    if t.value == '$if(':
        t.lexer.push_state("condition")
    else:
        t.lexer.push_state("conditionAlt")
    return t


def t_ENDIF(t):
    r'(\$endif\$(\n)?)|(\$\{endif\}(\n)?)'
    return t

def t_ELSEIF(t):
    r'(\$elseif\()|(\$\{elseif\()'
    if t.value == '$elseif(':
        t.lexer.push_state("condition")
    else:
        t.lexer.push_state("conditionAlt")
    return t

def t_ELSE(t):
    r'(\$else\$(\n)?)|(\$\{else\}(\n)?)'
    return t

def t_FOR(t):
    r'(\$for\()|(\$\{for\()'
    if t.value == '$for(':
        t.lexer.push_state("condition")
    else:
        t.lexer.push_state("conditionAlt")
    return t

def t_ENDFOR(t):
    r'(\$endfor\$(\n)?)|(\$\{endfor\}(\n)?)'
    return t


def t_condition_ENDCONDITION(t):
  r'\)\$(\n)?'
  t.lexer.pop_state()
  return t

def t_conditionAlt_ENDCONDITION(t):
  r'\)\}(\n)?'
  t.lexer.pop_state()
  return t

def t_VARIABLE(t):
    r'(\$[\w]([._\-]?[\w\d]+)*\$)|(\$\{[\w]([._\-]?[\w\d]+)*\})'
    return t

def t_PARTIAL(t):
    r'(\$([\w]([._\-]?[\w\d]+)*:)?[\w]([_\-\\]?[\w\d]+)*\(\)\$)|(\$\{([\w]([._\-\\]?[\w\d]+)*:)?[\w]([_\-]?[\w\d]+)*\(\)\})'
    return t

def t_PIPE(t):
    r'(\$([\w]([._\-]?[\w\d]+)*)(\/[\w][_\-]?[\w\d]+)*\$)|(\$\{([\w]([._\-\\]?[\w\d]+)*)(\/[\w][_\-]?[\w\d]+)*\})'
    return t

def t_WORD(t):
    r'[\w]([._\-]?[\w\d]+)*'
    return t

def t_CONST(t):
    r'[^$]|\$\$'
    return t

def t_ANY_error(t):
    print("Lex error - >" + str(t))
