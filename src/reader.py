from enum import Flag
import sys
import re

#primeira linha do ficheiro json
first_line = True

#Le linha do csv para descobrir os headers
def get_columns_names(string):
    columns = []
    reg_exp = r'((((?P<nome>(\w|[À-ÿ ])+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?)(,|$)))'
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

#Verifica se uma string representa um numero
def matchNumeric(string_num):
    reg_exp = r'((\+|-)?\d+)(\.\d+)?'
    p = re.compile(reg_exp)
    value = p.match(string_num)
    return value != None



#Valida se uma lista está preenchida um numero minimo de vezes (tuplo com 3 elems)
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
    return string == "sum" or string == "media"

#Aplica o metodo group em todos os elementos de uma lista
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
                    max_rep = get_max_rep(columns[i][1])
                    # map que aplica group() a todos os elementos da lista, devolvendo
                    # a lista dos resultados, retirando no caso de elemntos vazios
                    rep_list = apply_group("column",list[j:j+max_rep])
                    data.add_list(columns[i][0],rep_list)
                    j+= max_rep
                #Lista com metodos
                elif(len(columns[i]) == 3):
                    flag = validate_rep_method(list, columns[i][1],columns[i][2], j)
                    max_rep = get_max_rep(columns[i][1])
                    rep_list = apply_group("column",list[j:j+max_rep])
                    data.add_method_element(columns[i][0],columns[i][2],rep_list)
                    j+= max_rep
                else:
                    flag = False
            # Verificacao de coluna simples(estilo nome)
            else: 
                # Coluna tem de estar preenchida
                if(not list[j].group("column")):
                    flag = False
                else:
                    data.add_simple_element(columns[i],list[j].group("column"))
                j+=1
            i+=1
        if flag: print("valido ->" + line_to_read)
        else: print("invalido na iteracao i = " + str(i) +" j = " +str(j) +" ->" + line_to_read)
    else:
        print("Invalido -> " + str(get_num_columns(line_to_read)) + line_to_read)
        flag = False
    return flag
   

#classe que guarda as colunas de uma linha de forma a serem facilmente 
# identificaveis
class line:
    cols = []
    index = 0
    def __init__(self,columns):
        self.cols = [None] * len(columns)
        
    #adiciona um elemento simples na lista de colunas
    def add_simple_element(self,col_name,list):
        self.cols[self.index] = (col_name,list,0)
        self.index += 1

    #adiciona uma lista na lista de colunas
    def add_list(self,col_name,list):
        self.cols[self.index] = (col_name,list,1)
        self.index += 1
    
    #calcula o resultado de um metodo e adiciona na lista de colunas
    def add_method_element(self,col_name,method,l):
        result = 0
        float_list = list(map(float,l))
        if(method == "sum"):
            result = sum(float_list)
        elif(method == "media"):
            total = 0
            float_list
            for e in float_list:
                total += e
            if(total != 0): 
                result = total/len(float_list)
        new_col_name = col_name + "_" + method
        self.cols[self.index] = (new_col_name,result,1)
        self.index += 1


#Funçao que escreve uma linha do csv, processada, para um ficheiro json
def write_json_object(file,data):
    if(not first_line):
        file.write(",\n") #tab
    file.write("\t{\n")
    i = 0
    size = len(data.cols)
    while(i < size):
        file.write("\t\t" + "\"" + str(data.cols[i][0]) + "\": ")
        #caso contrario inclui-se ""
        if data.cols[i][2] == 0 :
            file.write("\"" + data.cols[i][1] +"\"") #necessario fazer o parse dos tuplos
        #se for do tipo metodo ou lista nao se inclui ""
        elif data.cols[i][2] == 1 :
            #escrever lista
            if(isinstance(data.cols[i][1], list)):
                file.write("[")#necessario fazer o parse dos tuplos
                j = 0
                while(j<len(data.cols[i][1])-1):
                    file.write(data.cols[i][1][i] + ",") #necessario fazer o parse dos tuplos
                    j += 1
                file.write(data.cols[i][1][j] + "]")
            #escrever resultado de metodo
            else:
                file.write(str(data.cols[i][1])) #necessario fazer o parse dos tuplos
        if(i < size-1): 
            file.write(",")
        file.write("\n")
        i+=1
    file.write("\t}")




################################################ Script da leitura do csv #####################################################


pattern_content = r'((?P<column>(\w|[À-ÿ ])*)(,|$))'
pattern_file = re.compile(pattern_content)

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r",encoding='utf8')

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w',encoding='utf8')
file_json.write("[\n")
#Tratar da primeira linha
line_to_read = file_csv.readline()
columns = get_columns_names(line_to_read)
cols_number = get_num_columns_array(columns)
#print("columns ->: " + str(cols_number))

while (line_to_read != ""): #nao deteta EOF
    data = line(columns)
    valid = validate_line(columns,line_to_read,cols_number,pattern_file,data)
    if valid: 
        write_json_object(file_json,data)
        first_line = False
        """
        print("******DEBUG******")
        print(data.cols[0])
        print(data.cols[1])
        print(data.cols[2])
        print(data.cols[3])
        print("*****************")
        """
    else:
         del data
    line_to_read = file_csv.readline() #le proxima linha
file_json.write("\n]\n")

file_csv.close()
file_json.close()