import sys
import re

def get_columns_names(string):
    columns = []
    reg_exp = r'((((?P<nome>(\w|[À-ÿ\s])+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?),?))'
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

def get_num_columns_array(columns):
    count = 0
    for col in columns:
        if(type(col) is tuple):
            max = get_max_rep(col[1])
            if(max > 0):
                count += max 
        else:
            count+=1
    return count

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

def get_num_columns (linha):
    return len(linha.split(','))

pattern_content = r'((((?P<nome>(\w|[À-ÿ\s])+)((?P<repetidos>{\d+(,\d+)?})(::(?P<metodo>(\w+)))?)?),?))'
pattern_file = re.compile(pattern_content)

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')


line_to_read = file_csv.readline()
colunas = get_columns_names(line_to_read)
cols_number = get_num_columns_array(colunas)
print("Colunas ->: " + str(cols_number))

while (line_to_read != ""): #nao deteta EOF
    valid_line = pattern_file.search(line_to_read) #tenta comparar se a linha dá match
    if (valid_line and get_num_columns(line_to_read) == cols_number):
        print(line_to_read + "-> Valido")
    else:
        print(line_to_read + "-> Invalido -> " + str(get_num_columns(line_to_read)))
        #file_json.write(valid_line.group()) #escreve no ficheiro
        #file_json.write("\n")
    line_to_read = file_csv.readline() #le proxima linha




file_csv.close()
file_json.close()