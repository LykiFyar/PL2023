import matplotlib.pyplot as plt
import numpy as np

# ler ficheiro
def readfile(filename = "myheart.csv"):
    file = open(filename)
    file.readline()
    
    list = []
    
    for line in file:
        list.append(line.strip().split(","))

    file.close()
        
    return list

def distByGender(data):
    
    dict = {}
    
    for person in data:
        if int(person[5]): # campo "temDoença"
            
           if person[1] not in dict: dict[person[1]] = 0
           else: dict[person[1]] = dict[person[1]] + 1
    
    return dict
    
def distByAge(data):
    
    list = []
    
    for person in data:
        if int(person[5]): # campo "temDoença"
            index = int(int(person[0]) / 5)
            while index >= len(list): 
                list.append(0)
            list[index] = list[index] + 1
           
    dict = {}
    for index in range(len(list)):
        if list[index] > 0:
            dict["[" + str(index*5) + "-" + str(index*5+4) + "]"] = list[index]
    
    return dict

def distByColesterolLevels(data):
    
    list = []
    
    for person in data:
        if int(person[5]): # campo "temDoença"
            index = int(int(person[3]) / 10)
            while index >= len(list): 
                list.append(0)
            list[index] = list[index] + 1
           
    dict = {}
    for index in range(len(list)):
        if list[index] > 0:
            dict["[" + str(index*10) + "-" + str(index*10+9) + "]"] = list[index]
    
    return dict

def makeTable(dict, column1, column2):
    print("====================")
    print(f"{column1}     │ {column2}")
    print("====================")
    for key in dict:
        print(f" {key}     {dict[key]} ")
    print("====================\n")


def printGraph(dict, tablelabel, xlabel, ylabel):

    # plot
    
    plt.bar(dict.keys(), dict.values())
    plt.title(tablelabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


        

data = readfile()

genderDict = distByGender(data)
makeTable(genderDict, "Sexo", "Número de Doentes")
printGraph(genderDict, "Distribuição da Doença por Sexo","Sexo", "Número de Doentes")

ageDict = distByAge(data)
makeTable(ageDict, "Idade", "Número de Doentes")
printGraph(ageDict, "Distribuição da Doença por Faixa Etária","Idade", "Número de Doentes")

colLevelsDict = distByColesterolLevels(data)
makeTable(colLevelsDict, "Nível de Colesterol", "Número de Doentes")
printGraph(colLevelsDict, "Distribuição da Doença por Nível de Colesterol", "Nível de Colesterol", "Número de Doentes")
