import statistics, logs

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