import re
import sys
from utilities import *
from lexer import *
from syntax import *

error = False

for_regex = r'^(FOR)(\d+)$'
comp_for = re.compile(for_regex)

if_regex = r'^(IF)(\d+)$'
comp_if = re.compile(for_regex)



def get_nest_tuples(tuple_stack,i,instruction):
  end = False
  search = ""
  cicle = []

  if comp_for.search(instruction):
    search = f"ENDFOR{comp_for.search(instruction).group(2)}"
  elif comp_if.search(instruction):
    search = f"ENDIF{comp_for.search(instruction).group(2)}"
  else:
    end = True

  while(i<len(tuple_stack) and not end):
    if(tuple_stack[i][0] == search):
      end = True
    else:
      cicle.append(tuple_stack[i])
    i+=1
  return cicle


def compile_for(tuple_stack, dictionary, file, condition = True):
  iterate = 1
  if dictionary.__contains__(condition):
    if isinstance(dictionary[condition],list):
      iterate = len(dictionary[condition])
  
  j = 0
  while j<iterate: 
    print(str(j) + " " + condition)
    compile_template(tuple_stack,dictionary,file,condition,j)
    j+=1


def compile_template(tuple_stack, dictionary, file, condition = True,j=0):
  i = 0 
  while i<len(tuple_stack):
    tuple = tuple_stack[i]
    if tuple[0] == "CONS":
      file.write(tuple[1])
    if(tuple[0] == "VAR"):
        variable = remove_dolars(tuple[1])
        if dictionary.__contains__(variable):
          if(isinstance(dictionary[variable],list) and variable != condition):
            for var in dictionary[variable]:
              file.write(var)
          elif(isinstance(dictionary[variable],list) and variable == condition):
              file.write(dictionary[variable][j])
          else:
            file.write(dictionary[variable])
    elif(comp_for.search(tuple[0])):
      variable = tuple[1]
      i+=1
      cicle = get_nest_tuples(tuple_stack,i,tuple[0])
      i += len(cicle)
      if dictionary.__contains__(variable):
        compile_for(cicle,dictionary,file,tuple[1])
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

  if not error:
    print("No syntax error")

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
  else:
    print("Syntax Error")




 