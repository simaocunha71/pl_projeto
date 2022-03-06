from enum import Flag
import sys
import re

#Le linha do csv para descobrir os headers
def get_columns_names(string):
    columns = []
    reg_exp = r'((((?P<nome>(\w|[À-ÿ ])+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?),?))'
    columns_pattern = re.compile(reg_exp)
    matches = columns_pattern.finditer(string)
    for match in matches:
        if(match.group("metodo") and match.group("repetidos") and match.group("nome")):
            columns.append((match.group("nome"),match.group("repetidos"), match.group("metodo")))

        elif(match.group("repetidos") and match.group("nome")):
            columns.append((match.group("nome"), match.group("repetidos")))

        elif(match.group("nome")):
            columns.append(match.group("nome"))
    
    return columns

#Devolve o numero de colunas máximo dos headers
def get_num_columns_array(columns):
    count = 0
    print("**************** \n Colunas: " + str(columns) + "\n****************\n")
    for col in columns:
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
    return len(line.split(','))

#Valida se uma lista está preenchida um numero minimo de vezes (tuplo com 2 elems)
def validate_rep(line, limits, index):
    min = get_min_rep(limits)
    max = get_max_rep(limits)

    if (min <= max):
        i = 0
        filled = 0
        while(i < max and filled < min):
            if(line[index].group("column") != None):
                filled += 1
            i+=1
            index += 1
        if(filled >= min):
            return True
    else:
        return False

#Verifica se uma string representa um numero
def matchNumeric(string_num):
    reg_exp = r'((\+|-)?\d+)(\.\d+)?'
    p = re.compile(reg_exp)
    value = p.match(string_num)
    return value.group() != None



#Valida se uma lista está preenchida um numero minimo de vezes (tuplo com 3 elems)
def validate_rep_method(line, limits, method, index):
    if (validate_method(method)):
        min = get_min_rep(limits)
        max = get_max_rep(limits)

        if (min <= max):
            i = 0
            filled = 0
            flag = True
            while(i < max and flag):
                if(line[index].group("column") != None):
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
    return string == "sum" or string == "media"



#Valida colunas de uma linha do csv
def validate_line (columns, line, cols_number, pattern_file):
    valid = pattern_file.finditer(line)
    if (valid and get_num_columns(line) == cols_number):
        flag = True
        i = 0
        j = 0
        while flag and i < len(columns):
            # Caso de repetiçoes onde se espera vários itens iguais (exemplo das notas no enunciado)
            if(type(columns[i]) is tuple):
                if(len(columns[i]) == 2):
                    flag = validate_rep(valid, columns[i][1], j)
                    j+=get_max_rep(columns[i][1])
                elif(len(columns[i]) == 3):
                    flag = validate_rep_method()
                else:
                    flag = False

            else: #Quando se encontra um valor (exemplo: nome)
                if(valid[j].group() == ','):
                    flag = False
                else:
                    pass
                j+=1
            i+=1

    else:
        print(line_to_read + "-> Invalido -> " + str(get_num_columns(line_to_read)))
        return False
        #file_json.write(valid_line.group()) #escreve no ficheiro
        #file_json.write("\n")
    







################################################ Script da leitura do csv #####################################################


pattern_content = r'((?P<column>(\w|[À-ÿ\s])*),?)'
pattern_file = re.compile(pattern_content)

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')


line_to_read = file_csv.readline()
columns = get_columns_names(line_to_read)
cols_number = get_num_columns_array(columns)
print("columns ->: " + str(cols_number))


while (line_to_read != ""): #nao deteta EOF
    validate_line(columns,line_to_read,cols_number,pattern_file)
    line_to_read = file_csv.readline() #le proxima linha




file_csv.close()
file_json.close()