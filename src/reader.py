import sys
import re

pattern = r'(?:\"(?P<id>.+)\",)(?:\"(?P<nome>.+)\",)(?:\"(?P<curso>.+)\",)(?:(\d+),)(?:(\d+),)(?:(\d+),)(\d+)' #a mudar
pattern_file = re.compile(pattern)

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')


line_to_read = file_csv.readline()
while (line_to_read != ""): #nao deteta EOF
    valid_line = pattern_file.search(line_to_read) #tenta comparar se a linha dá match
    if (valid_line):
        file_json.write(valid_line) #escreve no ficheiro
    line_to_read = file_csv.readline() #le proxima linha



file_csv.close()
file_json.close()