import re
import matplotlib.pyplot as plt


def loadFile(path):
    array = []
    
    with open(path) as file:
        for line in file.readlines():
            reg = re.match(r"(?P<número>\d*)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[^:]*)::(?P<pai>[^:]*)::(?P<mãe>[^:]*)::(?P<info>[^:]*)::\s*",line)
            if (reg is not None):
                array.append(reg.groupdict())
    
    return array
    


def calcFreqRegistosAno(array):
    dict = {}
    
    for line in array:
        if(line['data'] is not None):
            data = re.match(r"(?P<ano>\d{4})", line['data'])
            if data is not None:
                data = int(data['ano'])
                if dict.get(data) is None:
                    dict[data] = 0
                dict[data] = dict[data] + 1
    
    # dict = sorted(dict) 
    return dict

def calcFreqNomes(array):
    nomesP,apelidos,top5 = {},{},{}
    
    regex = re.compile(r"^(?P<nomeP>[^\w]*).*\s*(?P<apelido>[^\w]*)$")
    
    for line in array:
        if(line['nome'] is not None):
            nome = re.match(regex, line['nome'])
            print(str(nome.groupdict()))
            if nome is not None:
                nomeP = nome['nomeP']
                apelido = nome['apelido']
                if nomeP is not None:
                    if nomesP.get(nomeP) is None:
                        nomesP[nomeP] = 0
                    nomesP[nomeP] = nomesP[nomeP] + 1
                if apelido is not None:
                    if apelidos.get(apelido) is None:
                        apelidos[apelido] = 0
                    apelidos[apelido] = apelidos[apelido] + 1
        
    return nomesP,apelidos,top5


def printGraph(dict, tablelabel, xlabel, ylabel):

    # plot
    
    plt.bar(dict.keys(), dict.values())
    plt.title(tablelabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


array = loadFile("processos.txt")
#printGraph(calcFreqRegistosAno(array), "Frequência de processos por ano","Ano", "Frequência")
#printGraph(calcFreqNomes(array)[0], "Frequência de nomes próprios por ano","Nome Próprio", "Frequência")


print(calcFreqNomes(array)[0])