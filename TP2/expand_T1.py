import re
import sys
from utilities import *
from lexer import *
from syntax import *


def get_for(tuple_stack,i):
  endfor = False
  cicle = []
  while(i<len(tuple_stack) and not endfor):
    if(tuple_stack[i][0] == "ENDFOR"):
      endfor = True
    else:
      cicle.append(tuple_stack[i])
    i+=1
  return cicle



def compile_template(tuple_stack, dictionary, file, condition = True):
  if(isinstance(condition,bool)):
    validation = True
  elif(isinstance(condition,list)):
    if(len(condition) > 0):
      validation = True
    else:
      validation = False
  else:
    validation = True
  i = 0 
  j = 0
  while(i<len(tuple_stack) and validation):
    tuple = tuple_stack[i]
    if(tuple[0] == "CONS"):
      file.write(tuple[1])
    if(tuple[0] == "VAR"):
      variable = remove_dolars(tuple[1])
      if(dictionary[variable]):
        if(isinstance(dictionary[variable],list)):
          file.write(dictionary[variable][j])
          j+=1
        else:
          file.write(dictionary[variable])
    elif(tuple[0] == "FOR"):
      if dictionary[tuple[1]]:
        i+=1
        cicle = get_for(tuple_stack,i)
        i += len(cicle)
        compile_template(cicle,dictionary,file,dictionary[tuple[1]])
    print(condition)
    if(isinstance(condition,bool)):
      pass
    elif(isinstance(condition,list)):
      if(len(condition) > j):
        validation = condition[j]  
      else:
        validation = False
    else:
      validation = False
    i+=1


def expand_T1(template,dictionary,output=False):
  lexer = lex.lex()
  parser = yacc.yacc()

  #print("$if(titleblock)$\n$titleblock$\n\n$endif$")
  f = open(template, "r",encoding='utf8',errors="surrogateescape")

  lines = f.read()
  f.close()

  #lexer.input(lines)
  #for tok in lexer:
  #    print("\u001B[33m" + str(tok) + "\u001B[0m")

  #Parsing do template para verificar integridade lexica e gramatical
  stack = parser.parse(lines)

  #print(stack)

  #Expressao regular para separar os diferentes tuplos na string stack
  reg_exp_tuples = r'\((\w+)(,([^(),"]+|"([^"]*|")*"))?\)'
  compile = re.compile(reg_exp_tuples)
  matches = compile.finditer(stack)

  #transforma os diferentes tuplos do tipo string para tuplos
  tuple_stack = matches_to_tuples(matches)

  

  #for i in tuple_stack:
  #  print(i)

  #variables = {}
  #for i in tuple_stack:
  #  if i[0] == "VAR" or i[0] == "IF" or i[0] == "ELSEIF" or i[0] == "FOR":
  #    variable = remove_dolars(i[1])
  #    variables[variable] = variable
  #for v in variables:
  #  print(v)

  file = sys.stdout
  if output:
    file = open(output,'w+',encoding='utf8',errors="surrogateescape")
  
  compile_template(tuple_stack, dictionary, file)  

  file.close()




 