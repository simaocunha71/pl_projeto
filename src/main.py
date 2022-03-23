import os
import sys , re, statistics, logs, time

"""
TODO

meter mensagens de erro bonitas (é possivel que haja mais)
contar nº de linhas invalidas e meter no logs
"""


#primeira linha do ficheiro json
first_line = True

#Le linha do csv para descobrir os headers
def get_columns_names(string):
    columns = []
    #reg_exp = r'((((?P<nome>(\w|[À-ÿ ]|(\"[^"]*\"))+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?)(,|$)))' CORRETO
    reg_exp = r'(((?P<nome>(\w|[À-ÿ ]|(\".*\"))+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?)(?P<virgulas>(,+))?(,|$))'
    columns_pattern = re.compile(reg_exp)
    matches = columns_pattern.finditer(string)
    valid_header = True
    for match in matches: 
        if(match.group("repetidos") != None):
            #verificaçao do nº de virgulas depois de uma lista
            str_virgulas = match.group("virgulas")
            n_virg = get_max_rep(match.group("repetidos"))-1
            if(n_virg == len(str_virgulas)):
                if(match.group("metodo") and match.group("repetidos") and match.group("nome") ):
                    columns.append((match.group("nome"),match.group("repetidos"), match.group("metodo")))

                elif(match.group("repetidos") and match.group("nome") ):
                    columns.append((match.group("nome"), match.group("repetidos")))

                elif(match.group("nome")):
                    columns.append(match.group("nome"))
            else:
                valid_header = False
        else:
            if(match.group("nome")):
                columns.append(match.group("nome"))
    if(valid_header == False):
        columns = []
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

#Verifica se uma string representa um numero
def matchNumeric(string_num):
    reg_exp = r'^((\+|-)?\d+)(\.\d+)?$'
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
    return string == "sum" or string == "subtr" or string == "prod" or string == "div" or string == "media" or string == "median" or string == "mode"

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
            # Verificacao de coluna simples(estilo nome)
            else: 
                # Coluna tem de estar preenchida
                if(not list[j].group("column")):
                    flag = False
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
        elif(method == "subtr"):
            total = 0
            float_list
            for e in float_list:
                total = total - e
            result = total
        elif(method == "prod"):
            total = 1
            float_list
            for e in float_list:
                total = total * e
            result = total
            result = round(result,3)
        elif(method == "div"):
            try:
                total = float_list[0]
                i = 1
                float_list
                size = len(float_list)-1
                while (i < size):
                    total = total / float_list[i]
                    i+=1
                result = total
                result = round(result,3)
            except ZeroDivisionError:
                logs.send_error("Detetada divisão por 0! Apresenta-se valor default 0.")
                result = 0
        elif(method == "media"):
            result = statistics.mean(float_list)
        elif(method == "median"):
            result = statistics.median(float_list)
        elif(method == "mode"):
            result = statistics.mode(float_list)
        new_col_name = col_name + "_" + method
        self.cols[self.index] = (new_col_name,result,1)
        self.index += 1


def process_data_qmarks_name(col_name):
    new_col_name = re.sub(r'"',r'\"',col_name)
    return new_col_name


#Funçao que escreve uma linha do csv, processada, para um ficheiro json
def write_json_object(file,data):
    if(not first_line):
        file.write(",\n") #tab
    file.write("\t{\n")
    i = 0
    size = len(data.cols)
    while(i < size):
        column_name = process_data_qmarks_name(str(data.cols[i][0]))
        file.write("\t\t" + "\"" + column_name + "\": ")
        #se nao for uma lista inclui-se ""
        if data.cols[i][2] == 0 :
            content = process_data_qmarks_name(data.cols[i][1])
            file.write("\"" + content +"\"") 
        #se for do tipo metodo ou lista nao se inclui ""
        elif data.cols[i][2] == 1 :
            #escrever lista
            if(isinstance(data.cols[i][1], list)):
                file.write("[")
                j = 0
                #escrever elementos da lista
                len_list = len(data.cols[i][1])
                while(j< len_list -1):
                    content = data.cols[i][1][j] 
                    if matchNumeric(content):
                        file.write(content + ",")
                    else:
                        content = process_data_qmarks_name(content)
                        file.write('\"' + content + '\",')
                    j += 1
                #ultimo elemento da lista
                content = data.cols[i][1][j] 
                if matchNumeric(content):
                    file.write(content + "]")
                else:
                    content = process_data_qmarks_name(content)
                    file.write('\"' + content + '\"]')
            #escrever resultado de metodo
            else:
                file.write(str(data.cols[i][1])) 
        if(i < size-1): 
            file.write(",")
        file.write("\n")
        i+=1
    file.write("\t}")




################################################ Script da leitura do csv #####################################################
inicio = time.time()

logs.send_message(logs.ANSII_COLOUR.GREEN + "Conversor de ficheiros csv para ficheiros json - Grupo 6 | Processamento de linguagens (2021/2022)" + logs.ANSII_COLOUR.RESET)

pattern_content = r'((?P<column>(\w|[À-ÿ ]|(\"[^"]*\"))*)(,|$))'
pattern_file = re.compile(pattern_content)

filename_to_open = sys.argv[1]

re_name_file = r'^((.+)\/)?(?P<fn>(\w+(\.+([cCsSvV]+))))$'

p_nf = re.compile(re_name_file)
fnopen_match = p_nf.search(filename_to_open)


file_csv = open(filename_to_open,"r",encoding='utf8')
filename_to_save = filename_to_open.replace(filename_to_open[-3:],"json") #muda terminação de csv para json

file_json = open(filename_to_save,'w',encoding='utf8')

#Expressao regular para reconhecer paths de ficheiros com formato json
re_output = re.sub(r'[cCsSvV]+',r'json',re_name_file)
p_re_output = re.compile(re_output)
fnsave_match = p_re_output.search(filename_to_save)


file_json.write("[\n")
#Tratar da primeira linha
line_to_read = file_csv.readline()
columns = get_columns_names(line_to_read)
if(len(columns) == 0):
    logs.send_error("Header inválido! Ficheiro json vazio...")
cols_number = get_num_columns_array(columns)


line_to_read = file_csv.readline()
invalidLinesArray = []
#print("columns ->: " + str(cols_number))
nLinhas = 0

while (line_to_read != ""): #nao deteta EOF
    data = line(columns)
    valid = validate_line(columns,line_to_read,cols_number,pattern_file,data)
    if valid: 
        write_json_object(file_json,data)
        first_line = False
    else:
        invalidLinesArray.append(nLinhas)
        del data
    nLinhas += 1
    line_to_read = file_csv.readline() #le proxima linha
file_json.write("\n]\n")

print(str(invalidLinesArray))
file_csv.close()
file_json.close()

fim = time.time()

###################################################################### LOGS ####################################################################

try:
    logs.send_message("Ficheiro a converter: "+ logs.ANSII_COLOUR.YELLOW + fnopen_match.group("fn") + logs.ANSII_COLOUR.RESET + " (" + str(os.stat(filename_to_open).st_size) + " bytes) - encontrado na diretoria " + logs.ANSII_COLOUR.YELLOW + filename_to_open + logs.ANSII_COLOUR.RESET )
except Exception:
    logs.send_error("Ficheiro a converter não é do tipo csv!")
    sys.exit(1)

try: 
    logs.send_message("Novo ficheiro: " + logs.ANSII_COLOUR.YELLOW + fnsave_match.group("fn") + logs.ANSII_COLOUR.RESET + " (" + str(os.stat(filename_to_save).st_size) + " bytes) - disponível em " + logs.ANSII_COLOUR.YELLOW + filename_to_save + logs.ANSII_COLOUR.RESET )
    
except Exception:
    logs.send_error("Ficheiro json não encontrado!")
    sys.exit(1)

logs.send_message("Tempo de execução: " + logs.ANSII_COLOUR.YELLOW + str(round(fim-inicio,5)) + logs.ANSII_COLOUR.RESET + " ms")