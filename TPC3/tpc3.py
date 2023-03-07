import re
import matplotlib.pyplot as plt
import json


def loadFile(path):
    array = []
    
    with open(path) as file:
        for line in file.readlines():
            reg = re.match(r"(?P<número>\d*)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[^:]*)::(?P<pai>[^:]*)::(?P<mãe>[^:]*)::(?P<info>[^:]*)::\s*",line)
            if (reg is not None):
                res = reg.groupdict()
                if (res['info'] is not None):
                    res['info'] = re.split(r"\s*\.\s*",res['info'])
                array.append(res)
    return array
    

# a. Calcula a frequência de processos por ano (primeiro elemento da data);
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
    nomesP,apelidos = {},{}
    
    regex = re.compile(r"^(?P<nomeP>\w*).*\s(?P<apelido>\w*)$")
    
    for line in array:
        if(line['nome'] is not None):
            nome = re.match(regex, line['nome'])
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
        
    return nomesP,apelidos

def calcFreqRelacoes(array):
    rels = {}
    
    regex = re.compile(r".*\,\s*(?P<relacao>\w*).*$")
    
    relacoes_validas = ["avo", "avos", "mae", "pai", "pais", "irmao", "irmaos", "tio", "tios", "neto", "netos", "filho", "filhos", "bisavo", "bisavos", "primo", "primos", "sobrinho", "sobrinhos"]
    
    for line in array:
        if(line['info'] is not None):
            for inforegistry in line['info']:
                relacao = re.match(regex, inforegistry.lower())
                if relacao is not None:
                    rel = relacao.group(1)
                    if rel is not None:
                        if rel in relacoes_validas:
                            if rels.get(rel) is None:
                                rels[rel] = 0
                            rels[rel] = rels[rel] + 1
    return rels

def convert_to_json(array):
    dict = {}
    
    dict['pessoas'] = array
    
    with open("pessoas.json", "w", encoding="utf-8") as file:
        json_str = json.dumps(dict)
        file.write(json_str)


def makeTableByDict(dict, column1, column2):
    print("====================")
    print(f"{column1}     │ {column2}")
    print("====================")
    for key in dict:
        print(f" {key}     {dict[key]} ")
    print("====================\n")
    
def makeTableByTupleList(list, column1, column2):
    print("====================")
    print(f"{column1}     │ {column2}")
    print("====================")
    for item,value in list:
        print(f" {item}     {value} ")
    print("====================\n")

def printGraph(dict, tablelabel, xlabel, ylabel):

    # plot
    
    plt.bar(dict.keys(), dict.values())
    plt.title(tablelabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


array = loadFile("processos.txt")
opcao = -1
while opcao!=0:
    
    print("1. Gráfico de frequência de processos por ano")
    print("2. Gráfico de frequência de nomes próprios por ano")
    print("3. Gráfico de frequência de apelidos por ano")
    print("4. Top 5 Nomes Próprios")
    print("5. Top 5 Apelidos")
    print("6. Frequência de vários tipos de relações de parentesco")
    print("7. Criar ficheiro Json com primeiros 20 registos\n")
    opcao = int(input("Indique a opção: "))
    
    # a. Calcula a frequência de processos por ano (primeiro elemento da data)
    if opcao==1:
        printGraph(calcFreqRegistosAno(array), "Frequência de processos por ano","Ano", "Frequência")
    
    # b. Calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o ultimo em cada nome) por séculos
    elif opcao==2:
        printGraph(calcFreqNomes(array)[0], "Frequência de nomes próprios por ano","Nome Próprio", "Frequência")
    elif opcao==3:
        printGraph(calcFreqNomes(array)[1], "Frequência de Apelidos por ano","Apelido", "Frequência")
    elif opcao==4:
        nomesP,apelidos = calcFreqNomes(array)
        print(f"Top 5 Nomes Próprios Usados: ")
        makeTableByTupleList(sorted(nomesP.items(), key=lambda x:x[1], reverse=True)[:5], "Nomes Próprios", "Frequência")
    elif opcao==5:
        nomesP,apelidos = calcFreqNomes(array)
        print(f"Top 5 Apelidos Usados: ")
        makeTableByTupleList(sorted(apelidos.items(), key=lambda x:x[1], reverse=True)[:5], "Apelidos", "Frequência")
    
    # c. Calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.
    elif opcao==6:
        rels = calcFreqRelacoes(array)
        print(rels)
        print(f"Frequência de vários tipos de relação: ")
        printGraph(rels, "Frequência de relações de parentesco", "Relações de Parentesco", "Frequência")
    # d. Converta os 20 primeiros registos num novo ficheiro de output mas em formato Json.
    elif opcao==7:
        print("\n\n\n")
        convert_to_json(array[:20])