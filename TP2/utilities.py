import re
import roman
import ast

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

def remove_parentheses(string):
  reg_exp = r'(.+)\(\)'
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


def file_to_dict(file):
  result = None
  try:
    f_open = open(file,'r')
    result = ast.literal_eval(f_open.read())
    f_open.close()
  except Exception:
    pass
  return result


#verifica se o metodo dado pertence aos metodos disponiveis
def valid_method(method):
  methods = ['uppercase','lowercase','pairs','length','reverse','first','last','rest','allbutlast','chomp','nowrap','alpha','roman']
  return method in methods

#aplica o metodo a var
def apply_method(var,method):
  result = var
  if method == 'uppercase':
    if isinstance(var,str):
      result = var.upper()
    elif isinstance(var,list):
      i=0
      for v in var:
        if isinstance(v,str):
          result[i] = v.upper()
        i+=1
    elif isinstance(var,dict):
      for key in var.keys():
        value = var[key]
        if isinstance(value,str):
          result[key] = value.upper()
        elif isinstance(value,list):
          result[key] = apply_method(value,method)

  elif method == 'lowercase':
    if isinstance(var,str):
      result = var.lower()
    elif isinstance(var,list):
      i=0
      for v in var:
        if isinstance(v,str):
          result[i] = v.lower()
        i+=1
    elif isinstance(var,dict):
      for key in var.keys():
        value = var[key]
        if isinstance(value,str):
          result[key] = value.lower()
        elif isinstance(value,list):
          result[key] = apply_method(value,method)
          
  elif method == 'pairs':
    map = []
    if isinstance(var,list):
      i = 1
      for v in var:
        map.append((i,v))
        i+=1
      result = map
    elif isinstance(var,dict):
      result = list(var.items())

  elif method == 'length':
    if isinstance(var,list) or isinstance(var,dict) or isinstance(var,str):
      result = len(var)

  elif method == 'reverse':
    if isinstance(var,list):
      result.reverse()
    elif isinstance(var,str):
      result = var[::-1]

  elif method == 'first':
    if isinstance(var,list):
      if len(var) > 0:
        result = var[0]
      else:
        result = []
    elif isinstance(var,dict):
      values = list(var.values())
      if len(values) > 0:
        result = values[0]
      else:
        result = []

  elif method == 'last':
    if isinstance(var,list):
      if len(var) > 0:
        result = var[-1]
      else:
        result = []
    elif isinstance(var,dict):
      values = list(var.values())
      if len(values) > 0:
        result = values[-1]
      else:
        result = []

  elif method == 'rest':
    if isinstance(var,list):
      if len(var) > 1:
        result = var[1:]
      else:
        result = []
    elif isinstance(var,dict):
      values = list(var.values())
      if len(values) > 1:
        result = values[1:]
      else:
        result = []

  elif method == 'allbutlast':
    if isinstance(var,list):
      if len(var) > 1:
        result = var[:-1]
      else:
        result = []
    elif isinstance(var,dict):
      values = list(var.values())
      if len(values) > 1:
        result = values[:-1]
      else:
        result = []

  elif method == 'chomp':
    if isinstance(var,str):
      var = var.rstrip()
      result = re.sub(r'\n','',var)


  elif method == 'nowrap':
    if isinstance(var,str):
      result = var.rstrip(' ')

  elif method == 'alpha':
    if isinstance(var,str) or isinstance(var,list):
      i=0
      for v in var:
        result[i] = chr(97 + ord(str(v))%26)
        i+=1

  elif method == 'roman':
    if isinstance(var,str) or isinstance(var,list):
      i=0
      for v in var:
        if isinstance(v,int):
          result[i] = roman.toRoman(v)
          i+=1
  return result
    

#recebendo uma variavel, aplica todos os metodos de uma lista nela
def apply_methods(var,methods,file):
  i = 0
  error = False
  while i < len(methods) and not error:
    var = apply_method(var,methods[i])
    i+= 1
  if isinstance(var,list):
    for v in var:
      file.write(f"{str(v)} ")
  else:
    file.write(str(var))
  


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


#funcao similar a anterior, mas devolve o valor encontrado
def dic_get_var(variable,dictionary,condition = True,type = 0,j = 0):
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
      #lista, se for dentro de um ciclo com a variavel igual a condicao
                                                    #fazer uma funcao para tratar desta condicao no caso de objetos ou variavel "it"
      if(isinstance(result,list) and variable == condition and type == 2):
          return result[j]
      #variavel simples
      else:
        return result
    else:
      return None

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

