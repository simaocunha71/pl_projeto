import sys
import re

def get_columns_names(string):
    columns = []
    reg_exp = r'((((?P<nome>(\w|[À-ÿ])+)((?P<repetidos>{\d(,\d)?})(::(?P<metodo>(\w+)))?)?),?))'
    compila = re.compile(reg_exp)
    matches = compila.finditer(string)
    for match in matches:
        if(match.group("metodo") and match.group("repetidos") and match.group("nome")):
            columns.append((match.group("nome"),match.group("repetidos"), match.group("metodo")))

        elif(match.group("repetidos") and match.group("nome")):
            columns.append((match.group("nome"), match.group("repetidos")))

        elif(match.group("nome")):
            columns.append(match.group("nome"))

    
    print(columns)

pattern_content = r'(?:\"(?P<id>.+)\",)(?:\"(?P<nome>.+)\",)(?:\"(?P<curso>.+)\",)(?:(\d+),)(?:(\d+),)(?:(\d+),)(\d+)' #a mudar
pattern_file = re.compile(pattern_content)

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')


line_to_read = file_csv.readline()
get_columns_names("Número,Nome,Curso,Notas{3,5}::sum,,,,,")

"""
while (line_to_read != ""): #nao deteta EOF
    valid_line = pattern_file.search(line_to_read) #tenta comparar se a linha dá match
    if (valid_line):
        file_json.write(valid_line.group()) #escreve no ficheiro
        file_json.write("\n")
    line_to_read = file_csv.readline() #le proxima linha

"""



file_csv.close()
file_json.close()