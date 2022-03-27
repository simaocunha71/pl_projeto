import re
#ficheiro com funcoes para validacao das diferentes linhas e campos do csv



#Le linha do csv para descobrir os headers
#verifica tb a validade do header, caso seja invalido o csv sera invalido
def get_columns_names(string):
    columns = []
    #expressao regular do header
    #apanha:           nome do campo                  |numero de elementos da lista|     nome do metodo     | virgulas (no caso de ser uma lista)      
    reg_exp = r'((?P<nome>(\w|[^",{}\n]|(\"[^"]*\"))+)((?P<n_elementos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?)(?P<virgulas>(,+))?(,|$)'
    columns_pattern = re.compile(reg_exp)
    matches = columns_pattern.finditer(string)
    valid_header = True
    for match in matches: 
        #caso de match de uma lista
        if(match.group("n_elementos") != None):
            #verificaçao do nº de virgulas depois de uma lista
            str_virgulas = match.group("virgulas")
            n_virg = get_max_rep(match.group("n_elementos"))-1
            if(n_virg == len(str_virgulas)):
                #no caso de ter metodo tera de ser uma lista e tem de ter um nome de campo
                if(match.group("metodo") and match.group("n_elementos") and match.group("nome") ):
                    columns.append((match.group("nome"),match.group("n_elementos"), match.group("metodo")))
                #no caso de ser uma lista necessita ter um nome de campo
                elif(match.group("n_elementos") and match.group("nome") ):
                    columns.append((match.group("nome"), match.group("n_elementos")))
            else:
                valid_header = False
        #match de campo simples
        else:
            if(match.group("nome")):
                columns.append(match.group("nome"))
    if(valid_header == False):
        columns = []
    return columns

#Devolve o numero de colunas máximo dos headers
def get_num_columns_array(columns):
    count = 0
    #print("**************** \n Colunas: " + str(columns) + "\n****************\n")
    for col in columns:
        #caso de lista (o numero de virgulas e igual ao maximo numero de elementos)
        if(type(col) is tuple):
            max = get_max_rep(col[1])
            if(max > 0):
                count += max 
        else:
            count+=1
    return count

#Devolve o valor para o nº de colunas
"""
Por exemplo: 
    {3,5} -> devolve 5
    {3} -> devolve 3 (porque nao existe o limite máximo)
"""
def get_max_rep(reps):
    regExp = r'^{(?P<fst>\d+)(,(?P<sec>\d+))?}$'
    interv = re.compile(regExp)
    value = interv.match(reps)
    if(value.group("sec")):
        return int(value.group("sec"))
    elif(value.group("fst")):
        return int(value.group("fst"))
    else:
        return -1

#Devolve o valor minimo para o nº de colunas
def get_min_rep(reps):
    regExp = r'^{(?P<fst>\d+)(,(?P<sec>\d+))?}$'
    interv = re.compile(regExp)
    value = interv.match(reps)
    if(value.group("fst")):
        return int(value.group("fst"))
    else:
        return -1

#Devolve o numero de colunas de uma linha do csv
def get_num_columns (line):
    qmark_flag = False
    count = 0
    for c in line:
        if not qmark_flag:
            if(c == ","):
                count += 1
            elif (c == "\""):
                qmark_flag = True
        else:
            if (c == "\""):
                qmark_flag = False
    return count + 1 #ha sempre menos uma virgula do que o numero de colunas 

#Valida se uma lista está preenchida um numero minimo de vezes (tuplo com 2 elems)
def validate_rep(line, limits, index):
    min = get_min_rep(limits)
    max = get_max_rep(limits)

    if (min <= max):
        i = 0
        filled = 0
        size = len(line)
        while(i < max and index < size and filled < min):
            if(len(line[index].group("column")) > 0):
                filled += 1
            i+=1
            index += 1
        if(filled >= min):
            return True
    else:
        return False

#Verifica se uma string representa um numero (parte decimal inclusive)
def matchNumeric(string_num):
    reg_exp = r'^((\+|-)?\d+)(\.\d+)?$'
    p = re.compile(reg_exp)
    value = p.match(string_num)
    return value != None



#Valida se uma lista com metodo está preenchida um numero minimo de vezes (tuplo com 3 elems)
#todos os elementos da lista tem de ser do mesmo tipo para ser valida
def validate_rep_method(line, limits, method, index):
    if (validate_method(method)):
        min = get_min_rep(limits)
        max = get_max_rep(limits)
        if (min <= max):
            i = 0
            filled = 0
            flag = True
            size = len(line)
            while(i < max and index < size and flag):
                if(len(line[index].group("column")) > 0):
                    filled += 1
                    if (not matchNumeric(line[index].group("column"))):
                        flag = False
                i+=1
                index += 1
            
            if(filled >= min and flag):
                return True
            else:
                return False
        else:
            return False


#Valida os metodos
def validate_method (string):
    return string == "sum" or string == "subtr" or string == "prod" or string == "div" or string == "media" or string == "median" or string == "mode"

#Aplica o metodo group em todos os elementos de uma lista, genero map
def apply_group(column_name,list):
    new_list = []
    for l in list:
        if(l.group(column_name)):
            new_list.append(l.group(column_name))
    return new_list

#Valida colunas de uma linha do csv
def validate_line (columns, line, cols_number, pattern_file,data):
    valid = pattern_file.finditer(line)
    list = [*valid]
    #Numero de colunas tem de ser igual ao definido na estrutura do csv
    if (list and get_num_columns(line) == cols_number):
        flag = True
        i = 0
        j = 0
        while flag and i < len(columns):
            # Verificacao de listas (exemplo das notas no enunciado)
            if(type(columns[i]) is tuple):
                #Lista simples
                if(len(columns[i]) == 2):
                    flag = validate_rep(list, columns[i][1], j)
                    if flag:
                        max_rep = get_max_rep(columns[i][1])
                        # map que aplica group() a todos os elementos da lista, devolvendo
                        # a lista dos resultados, retirando no caso de elemntos vazios
                        rep_list = apply_group("column",list[j:j+max_rep])
                        data.add_list(columns[i][0],rep_list)
                        j+= max_rep
                #Lista com metodos
                elif(len(columns[i]) == 3):
                    flag = validate_rep_method(list, columns[i][1],columns[i][2], j)
                    if flag:
                        max_rep = get_max_rep(columns[i][1])
                        rep_list = apply_group("column",list[j:j+max_rep])
                        data.add_method_element(columns[i][0],columns[i][2],rep_list)
                        j+= max_rep
                else:
                    flag = False
            # Verificacao de coluna simples(estilo nome), aceitamos que esteja vazia
            else: 
                data.add_simple_element(columns[i],list[j].group("column"))
                j+=1
            i+=1
        #if flag: print("valido ->" + line_to_read)
        #if not flag: logs.send_error("Linha "+ str(i+1) + " inválida!")
    else:
        #print("Invalido -> " + str(get_num_columns(line_to_read))  + " "+ line_to_read)
        flag = False
    return flag
   