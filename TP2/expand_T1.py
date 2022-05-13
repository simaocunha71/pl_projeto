from io import TextIOWrapper
import re
import sys
import os
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
  if dic_contains(condition,dictionary):
    compile_template(tuple_stack,dictionary,file,condition,1)
  else:
    valid = False
    i = 0
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
        if dic_contains(tuple[1],dictionary,condition):
          compile_template(instructions,dictionary,file,tuple[1])
      else:
        i+=1


#funcao auxiliar do compilador, que permite o ciclo de uma instrucao for
def compile_for(tuple_stack, dictionary, file, condition = True):
  iterate = 1
  if dic_contains(condition,dictionary):
    var = dic_get_var(condition,dictionary)
    if isinstance(var,list):
      iterate = len(var)
  j = 0
  while j<iterate: 
    compile_template(tuple_stack,dictionary,file,condition,2,j)
    j+=1


#funcao utilizada para compilar partials (subtemplates)
# as subtemplates podem ser utilizadas sozinhas, ou a variaveis dicionarios
def compile_partial(partial,dictionary,file,condition,type,j):
  partial = remove_dolars(partial)
  splits = partial.split(':')
  #caso de parcial aplicado a uma variavel
  if(len(splits) == 2):
    var = dic_get_var(splits[0],dictionary,condition,type,j)
    partial = remove_parentheses(splits[1])
    if os.path.isfile(partial):
      if var:
        #caso da variavel ser uma lista
        if isinstance(var,list):
          for i in var:
            if isinstance(var,dict):
              expand_T1(partial,var,file)
        #variavel simples
        else:
          if isinstance(var,dict):
            expand_T1(partial,var,file)
    else:
      print(f"template \"{partial}\" not found")
  #partial simples
  elif(len(splits) == 1):
    partial = remove_parentheses(partial)
    if os.path.isfile(partial):
      expand_T1(partial,{},file)
    else:
      print(f"template \"{partial}\" not found")
        
#funcao utilizada para compilar o pipe com 1 ou multpilos metodos
def compile_pipe(pipe,dictionary,file,condition,type,j):
  pipe = remove_dolars(pipe)
  splits = pipe.split('/')
  var_name = splits[0]
  var = dic_get_var(var_name,dictionary,condition,type,j)
  valid = True
  i = 0
  methods =splits[1:] 
  #verificar se todos os metodos sao validos
  while valid and i < len(methods):
    valid = valid_method(methods[i])
    i += 1

  if valid:
    if var:
      apply_methods(var,methods,file)
  else:
    print(f"Unknown method {methods[i-1]}")



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

    #caso partial
    if tuple[0] == "PARTIAL":
      compile_partial(tuple[1],dictionary,file,condition,type,j)

    #caso pipe
    if tuple[0] == "PIPE":
      compile_pipe(tuple[1],dictionary,file,condition,type,j)

    #caso variavel
    # necessario verificar se existe, tipo de variavel, se esta dentro de um ciclo...
    if(tuple[0] == "VAR"):
        variable = remove_dolars(tuple[1])
        contains = dic_contains(variable,dictionary,condition,type,j)
        if contains:
          dic_write_var(variable,dictionary,file,condition,type,j)

    #caso ciclo IF
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
  #booleano que indica se o ficheiro ja esta aberto (caso de partial)
  opened = False

  if os.path.isfile(template):
    f = open(template, "r",encoding='utf8',errors="surrogateescape")

    lines = f.read()
    f.close()


    #Parsing do template para verificar integridade lexica e gramatical
    stack = parser.parse(lines)

    if not error:

      #Expressao regular para separar os diferentes tuplos na string stack
      reg_exp_tuples = r'\((\w+)(,([^(),"]+|"([^"]*|")*"))?\)'
      compile = re.compile(reg_exp_tuples)
      matches = compile.finditer(stack)

      #transforma os diferentes tuplos do tipo string para tuplos
      tuple_stack = matches_to_tuples(matches)

      file = sys.stdout
      if output:
        if isinstance(output,str):
          file = open(output,'w+',encoding='utf8',errors="surrogateescape")
        #caso de subtemplates, o ficheiro ja estara antes aberto
        elif isinstance(output,TextIOWrapper):
          file = output
          opened = True
  
      compile_template(tuple_stack, dictionary, file)  
      if opened == False:
        file.close()
    else:
      print("Syntax Error")
  else:
    print(f"Template {template} not found")




 