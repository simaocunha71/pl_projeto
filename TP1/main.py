import os
import sys , re, statistics, logs, time
from validate_csv import *
from line import *

"""
TODO
arranjar datasets fixolas
"""

#variaveis globais
first_line = True #primeira linha do ficheiro json
flag_logs = False #flag de logs
invalidLines = 0


#Substitui '"' por '\"' 
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
flag_validName = True


if(len(sys.argv) > 1 and len(sys.argv) <= 3):
    #verificacao da flag dos logs
    if(len(sys.argv) == 3 and sys.argv[2] == "-l"):
        flag_logs = True

    if(flag_logs):
        inicio = time.time()
        logs.send_message(logs.ANSII_COLOUR.GREEN + "Conversor de ficheiros csv para ficheiros json - Grupo 6 | Processamento de linguagens (2021/2022)" + logs.ANSII_COLOUR.RESET)

    #expressao para ler colunas
    pattern_content = r'((?P<column>(\w|[^",{}\n]|(\"[^"]*\"))*)(,|$))'
    pattern_file = re.compile(pattern_content)

    filename_to_open = sys.argv[1]

    #expressao para verificar se a extensao do ficheiro e valida
    re_name_file = r'^((.+)\/)?(?P<fn>(\w+(\.+)))(?P<ext>[cC][sS][vV])$'

    p_nf = re.compile(re_name_file)
    fnopen_match = p_nf.search(filename_to_open)

    if(fnopen_match != None):
        file_csv = open(filename_to_open,"r",encoding='utf8',errors="surrogateescape")
        filename_to_save = filename_to_open.replace(filename_to_open[-3:],"json") #muda terminação de csv para json

        file_json = open(filename_to_save,'w',encoding='utf8',errors="surrogateescape")

        only_nameInput = fnopen_match.group("fn") + fnopen_match.group("ext")
        only_nameOutput = fnopen_match.group("fn") + "json"

        file_json.write("[\n")
        #Tratar da primeira linha
        line_to_read = file_csv.readline()
        columns = get_columns_names(line_to_read)
        if(len(columns) == 0):
            logs.send_error("Header inválido! Ficheiro json vazio...")
        else:
            cols_number = get_num_columns_array(columns)


            line_to_read = file_csv.readline()
            #print("columns ->: " + str(cols_number))
            nLinhas = 2
            #tratar linha a linha do ficheiro
            while (line_to_read != ""): #nao deteta EOF
                data = line(columns)
                valid = validate_line(columns,line_to_read,cols_number,pattern_file,data)
                if valid: 
                    write_json_object(file_json,data)
                    first_line = False
                else:
                    #print(str(invalidLines) + ": \"" + line_to_read + "\"")
                    invalidLines+=1
                    del data
                nLinhas+=1
                line_to_read = file_csv.readline() #le proxima linha

        file_json.write("\n]\n")

        file_csv.close()
        file_json.close()
    else:
        flag_validName = False
    fim = time.time()

    ###################################################################### LOGS ####################################################################
    if(flag_logs):
        if(invalidLines > 1):
            logs.send_error("Foram encontradas " + str(invalidLines+1) + " linhas inválidas em " + str(nLinhas-1) + " linhas lidas.")
        elif(invalidLines == 1):
            logs.send_error("Foi encontrada 1 linha inválida em " + str(nLinhas-1) + " linhas lidas.")
        elif(flag_validName == True):
            logs.send_message(logs.ANSII_COLOUR.GREEN +"Todas as linhas são válidas!" + logs.ANSII_COLOUR.RESET)

        try:
            logs.send_message("Ficheiro a converter: "+ logs.ANSII_COLOUR.YELLOW + only_nameInput + logs.ANSII_COLOUR.RESET + " (" + str(os.stat(filename_to_open).st_size) + " bytes) - encontrado na diretoria " + logs.ANSII_COLOUR.YELLOW + filename_to_open + logs.ANSII_COLOUR.RESET )
        except Exception:
            logs.send_error("Ficheiro a converter não é do tipo csv!")
            sys.exit(1)

        try: 
            logs.send_message("Novo ficheiro: " + logs.ANSII_COLOUR.YELLOW + only_nameOutput + logs.ANSII_COLOUR.RESET + " (" + str(os.stat(filename_to_save).st_size) + " bytes) - disponível em " + logs.ANSII_COLOUR.YELLOW + filename_to_save + logs.ANSII_COLOUR.RESET )
            
        except Exception:
            logs.send_error("Ficheiro json não encontrado!")
            sys.exit(1)

        logs.send_message("Tempo de execução: " + logs.ANSII_COLOUR.YELLOW + str(round(fim-inicio,5)) + logs.ANSII_COLOUR.RESET + " ms")
else:
    logs.send_error("Numero de argumentos invalido.")