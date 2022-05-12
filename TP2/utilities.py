import re

def matches_to_tuples(matches):
  tuple_stack = []
  for match in matches:
      type = match.group(1)
      content = ""
      if match.group(3):
       content = remove_qotes(match.group(3))
      tuple = (type,content)
      tuple_stack.append(tuple)
  return tuple_stack

def remove_qotes(string):
  reg_exp = r'"(.+|\n+|\s+)"'
  compile = re.compile(reg_exp)
  match = compile.search(string)
  if match:
    return match.group(1)
  else:
    return string

def remove_dolars(string):
  reg_exp = r'\$(.+)\$'
  compile = re.compile(reg_exp)
  match = compile.search(string)
  if match:
    return match.group(1)
  else:
    reg_exp = r'\$\{(.+)\}'
    compile = re.compile(reg_exp)
    match = compile.search(string)
    if match:
      return match.group(1)
    else:
      return string


#funcao que procura uma dada variavel num dicionario e a escreve no ficheiro explicitado
# apresenta argumentos opcionais para procura da variavel no dicionario e escrita no ficheiro
def dic_write_var(variable,dictionary,file,condition = True,type = 0,j = 0):
  #caso especial da variavel "it"
  if variable.split('.')[0] == "it" and not isinstance(condition,bool):
    variable = re.sub(r'(it)(\.\w)*',condition +r'\2',variable)

  if dic_contains(variable,dictionary,condition,type,j):
    splits = variable.split('.')
    if isinstance(splits,list):
      iterations = len(splits)

    i = 0
    result = dictionary
    var_append = splits[0]
    error = False
    while(i<iterations and not error):
      if not isinstance(condition,bool):
        if i > 0:
          var_append = var_append + "." + splits[i] 
      #se a variavel for a da condicao e for pedida por um "for", pega apenas
      # na variavel correspondente a iteracao atual, dada por j
      if var_append == condition:
        condition = True
        result = result[splits[i]]
        if isinstance(result,list) and type == 2:
          if j < len(result):
            result = result[j]
          else:
            error = True
      else:
        result = result[splits[i]]
      i += 1

    if not error:
      #lista, se for fora de um ciclo ou for diferente da condicao deste, escreve-se todos os elementos
      if((isinstance(result,list) and variable != condition) or (isinstance(result,list) and type != 2)):
        for var in result:
          file.write(str(var)+" ")

      #lista, se for dentro de um ciclo com a variavel igual a condicao
                                                    #fazer uma funcao para tratar desta condicao no caso de objetos ou variavel "it"
      elif(isinstance(result,list) and variable == condition and type == 2):
          file.write(str(result[j]))
      #variavel simples
      else:
        file.write(str(result))




#funcao utiliada para verificar se uma variavel pertence ao dicionario
# tem argumentos opcionais para auxilio na procura, caso de "for"
# neste casos especial, e possivel escolher uma variavel de uma lista
def dic_contains(variable,dictionary,condition = True,type = 0,j = 0):
  contains = True
  error = False
  i = 0
  iterations = 1
  #caso especial da variavel "it"
  if variable.split('.')[0] == "it" and not isinstance(condition,bool):
    variable = re.sub(r'(it)(\.\w)*',condition.split('.')[0]+r'\2',variable)

  splits = variable.split('.')

  if isinstance(splits,list):
    iterations = len(splits)
  dic = dictionary
  var_append = splits[0]
  
  
  while(contains and i < iterations and not error):
    if not isinstance(condition,bool):
      if i > 0:
        var_append = var_append + "." + splits[i]

    if var_append == condition:
      condition = True
      if dic.__contains__(splits[i]):
        dic = dic[splits[i]]
        if isinstance(dic,list) and type == 2:
          if j < len(dic):
            dic = dic[j]
          else:
            error = True
            contains = False
      else:
        contains = False
    else:
      if not dic.__contains__(splits[i]):
        contains = False
      # possivel procurar em dicionarios dentro do dicionario
      else:
        contains = dic.__contains__(splits[i])
        dic = dic[splits[i]]
    i += 1

  return contains

