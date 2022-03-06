import sys

#ficheiro a abrir como input
filename_to_open = sys.argv[1]

file_csv = open(filename_to_open,"r")

filename_to_save = filename_to_open.replace("csv","json") #muda terminação de csv para json
file_json = open(filename_to_save,'w')


line = file_csv.readline()
while (line != ""): #nao deteta EOF
    file_json.write(line) #do something
    line = file_csv.readline() #le proxima linha



file_csv.close()
file_json.close()