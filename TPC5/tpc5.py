from sys import stdin, exit
import re

# Regular expression rules for simple tokens
t_MOEDA    = r'MOEDA ((\d+[ce](,[ ]*)?)*)'
t_NUMERO   = r'^T=(\d+)'
t_ABORTAR  = r'^ABORTAR$'
t_LEVANTAR = r'^LEVANTAR$'
t_POUSAR   = r'^POUSAR$'



def stringMoedas(x):
    if x/100 >= 1: 
        return str(int(x/100)) + "e" + str(x%100) + "c" 
    else: 
        return str(x) + "c"

def stringSaldo(x):
    return "saldo = " + stringMoedas(x)

def returnTroco(x):
    troco = {'1e': 0, '2e': 0, '50c': 0, '20c': 0, '10c': 0, '5c': 0, '2c': 0, '1c': 0}
    while x > 0:
        if x >= 200:
            x -= 200
            troco['2e'] += 1
        elif x >= 100:
            x -= 100
            troco['1e'] += 1
        elif x >= 50:
            x -= 50
            troco['50c'] += 1
        elif x >= 20:
            x -= 20
            troco['20c'] += 1
        elif x >= 10:
            x -= 10
            troco['10c'] += 1
        elif x >= 5:
            x -= 5
            troco['5c'] += 1
        elif x >= 2:
            x -= 2
            troco['2c'] += 1
        elif x >= 1:
            x -= 1
            troco['1c'] += 1
    res = "troco = "
    for key, value in troco.items():
        if value > 0:
            if len(res) > 8:
                res += ", "
            res += str(value) + "x" + key
    return res


# State variables
moedas_validas = {'1e': 100, '2e': 200, '50c': 50, '20c': 20, '10c': 10, '5c': 5, '2c': 2, '1c': 1}
init = False
balance = 0

for line in stdin:
    line = line.strip()
    
    moedas = re.match(t_MOEDA, line)
    number = re.match(t_NUMERO, line)
    if(moedas is not None and init):
        listmoedas = moedas.group(1).split(r',')
        res = ""
        for moeda in listmoedas:
            if moeda.strip() in moedas_validas.keys():
                balance += moedas_validas[moeda.strip()]
            else:
                res += moeda + ' - Moeda inválida;'
        res += stringSaldo(balance)
        print(res)
    elif(re.match(t_LEVANTAR,line) is not None):
        print("Introduza moedas...")
        init = True
    elif(re.match(t_POUSAR,line) is not None and init):
        print(returnTroco(balance) + '; Volte sempre!')
        init = False
        balance = 0
    elif(re.match(t_ABORTAR, line) is not None and init):
        print('Operação abortada, moedas devolvidas: ' + stringMoedas(balance))
        balance = 0
        init = False
    elif(number is not None and init):
        # números bloqueados: 601 e 641
        if(re.match(r'6[04]1\d{6}',number.group(1)) is not None):
            print('Chamada bloqueada - Tente outro número')
        # chamadas internacionais
        elif(re.match(r'00\d{9,}',number.group(1)) is not None):
            if(balance >= 150):
                balance -= 150
                print('Chamada efetuada para ' + number.group(1) + ", " + stringSaldo(balance))
            else:
                print("Saldo insuficiente - custo da chamada: 1e50c")
        # chamadas nacionais
        elif(re.match(r'2\d{8}',number.group(1)) is not None):
            if(balance >= 25):
                balance -= 25
                print('Chamada efetuada para ' + number.group(1) + ", " + stringSaldo(balance))
            else:
                print("Saldo insuficiente - custo da chamada: 25c")
        # chamadas azuis
        elif(re.match(r'808\d{6}',number.group(1)) is not None):
            if(balance >= 10):
                balance -= 10
                print('Chamada efetuada para ' + number.group(1) + ", " + stringSaldo(balance))
            else:
                print("Saldo insuficiente: custo da chamada: 10c")
        # chamadas verdes
        elif(re.match(r'800\d{6}',number.group(1)) is not None):
            print('Chamada efetuada para ' + number.group(1) + ", " + stringSaldo(balance))
        # número inválido
        else:
            print("Número inválido: " + number.group(1) + ", " + stringSaldo(balance))
    else:
        print('ERRO: Comando desconhecido ou inválido')