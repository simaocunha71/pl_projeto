import re
import sys
from utilities import *
from lexer import *
from syntax import *

error = False

for_regex = r'^(FOR)(\d+)$'
comp_for = re.compile(for_regex)

if_regex = r'^(IF)(\d+)$'
comp_if = re.compile(if_regex)

endif_regex = r'^(ENDIF)(\d+)$'
comp_endif = re.compile(endif_regex)

""" 
TODO : 
  pipes
  sub-templates
 """

def get_nest_tuples(tuple_stack,i,instruction):
  end = False
  search = ""
  instructions = []
  if comp_for.search(instruction):
    search = f"ENDFOR{comp_for.search(instruction).group(2)}"
  elif comp_if.search(instruction):
    search = f"ENDIF{comp_if.search(instruction).group(2)}"
  elif instruction == "ELIF":
    i = 0
    level = 0
    while(i<len(tuple_stack) and not end):
      tuple = tuple_stack[i]
      print(str(tuple) + " " + level)
      if (comp_endif(tuple[0]) or tuple[0] == "ELSE" or tuple[0] == "ELSEIF") and level == 0:
        end = True
      elif comp_endif(tuple[0]):
        level -= 1
      elif comp_if.search(instruction):
        level += 1
        instructions.append(tuple)
      else:
        instructions.append(tuple)
      i+=1
  else:
    end = True

  while(i<len(tuple_stack) and not end):
    if(tuple_stack[i][0] == search):
      end = True
    else:
      instructions.append(tuple_stack[i])
    i+=1
  return instructions


#funcao auxiliar do compilador, que permite tratar de if
def compile_if(tuple_stack, dictionary, file,instruction, condition = True):
  #print(condition)
  if dictionary.__contains__(condition):
    compile_template(tuple_stack,dictionary,file,condition,1)
  else:
    valid = False
    i = 0
    level = 0
    while(not valid and i < len(tuple_stack)):
      tuple = tuple_stack[i]
      if(tuple[0] == "ELSE"):
        valid = True
        instructions = get_nest_tuples(tuple_stack,i,instruction)
        compile_template(instructions, dictionary, file)
      elif(tuple[0] == "ELSEIF"):
        i+=1
        instructions = get_nest_tuples(tuple_stack,i,tuple[0])
        i += len(instructions)
        if dictionary.__contains__(tuple[1]):
          compile_template(instructions,dictionary,file,tuple[1])
      
      i+=1


#funcao auxiliar do compilador, que permite o ciclo de uma instrucao for
def compile_for(tuple_stack, dictionary, file, condition = True):
  iterate = 1
  if dictionary.__contains__(condition):
    if isinstance(dictionary[condition],list):
      iterate = len(dictionary[condition])
  j = 0
  while j<iterate: 
    compile_template(tuple_stack,dictionary,file,condition,2,j)
    j+=1



        



#funcao principal de compilacao das instrucoes parsed
# tuple_stack: pode ser usado para correr listas de instrucoes
# dictionary : recebe um dicionario com informacao sobre as variaveis
# file       : ficheiro onde escreve o texto final
# condition  : argumento opcional da condicao de um for ou if
# type       : argumento opcional indicando tipo de nest (if == 1 ou for == 2)
# j          : argumento opcional no caso de for, utilizado para 
def compile_template(tuple_stack, dictionary, file, condition = True, type = 0,j=0):
  i = 0 
  #corre todas as instrucoes passadas
  while i<len(tuple_stack):
    tuple = tuple_stack[i]
    #caso constante, simplesmente escreve no ficheiro
    if tuple[0] == "CONS":
      file.write(tuple[1])

    #caso variavel
    # necessario verificar se existe, tipo de variavel, se esta dentro de um ciclo...
    if(tuple[0] == "VAR"):
        variable = remove_dolars(tuple[1])
        contains = dic_contains(variable,dictionary,condition,type,j)
        if contains:
          dic_write_var(variable,dictionary,file,condition,type,j)
    elif(comp_if.search(tuple[0])):
      variable = tuple[1]
      i+=1
      instructions = get_nest_tuples(tuple_stack,i,tuple[0])
      i += len(instructions)
      compile_if(instructions,dictionary,file,tuple[0],variable)
    #caso ciclo FOR
    elif(comp_for.search(tuple[0])):
      variable = tuple[1]
      i+=1
      cicle = get_nest_tuples(tuple_stack,i,tuple[0])
      i += len(cicle)
      contains = dic_contains(variable,dictionary,condition,type,j)
      if contains:
        compile_for(cicle,dictionary,file,variable)
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




 