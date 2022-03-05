import sys

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

lines = file_csv.readlines()

for line in lines:
    print(line)

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')

file_json.write("Ja meti aqui qq coisa")


file_csv.close()
file_json.close()