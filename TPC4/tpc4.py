import re
import sys
import json


def applyOp(array, op):
    if(op == "media"):
        return sum(array) / len(array)
    elif(op == "sum"):
        return sum(array)
    else:
        print("Operação inválida: " + op)
        sys.exit(1)

def csv_to_json(src, dest):
    header = []
    jsonlist = []
    
    
    with open(src, encoding="utf-8") as f:
        file = f.readlines()
    
    reg = re.compile(r"[\,\;](?!\d+})")
    header = reg.split(file[0].strip())
    
    for line in file[1:]:
        reg = re.compile(r"[\;\,]")
        data = reg.split(line.strip())
        registry = {}
        for i, elem in enumerate(data):
            if(header[i] != ""):
                list_parse = re.match(r'(?P<camp>\w+){((?P<liststart>\d+),)?(?P<listlen>\d+)}(::(?P<op>\w+))?$', header[i])
                if list_parse is None:
                    registry[header[i]] = elem                
                else:
                    listcamps = list_parse.groupdict()
                    # Tratamento de listas
                    if(listcamps["listlen"] is None):
                        print("Syntax error: " + header[i] + " - missing list length")
                        return
                    else:
                        lista = []
                        j = i
                        length = int(listcamps["listlen"])
                        # Adicionar os elementos à lista
                        while(j < i + length):
                            if(data[j] != ""):
                                lista.append(int(data[j]))
                            j += 1
                        # no caso de existir um valor mínimo para o tamanho da lista
                        if(listcamps["liststart"] is not None) :
                            minlen = int(listcamps["liststart"])
                        else:
                            minlen = 1
                        # verificar que a lista respeita as regras de tamanho do header
                        if(len(lista) >= minlen and len(lista) <= length):
                            if (listcamps["op"] is None):
                                registry[listcamps["camp"]] = lista
                            else:
                                registry[listcamps["camp"] + "_" + listcamps["op"]] = applyOp(lista, listcamps["op"])
                        else:
                            print("List with invalid size - Registry: " + line)
                            sys.exit(1)
        
        jsonlist.append(registry)
    
    with open(dest, "w", encoding="utf-8") as file:
        json_str = json.dumps(jsonlist)
        file.write(json_str)

def main(argv):
    csv_to_json(argv[1], argv[2])

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        main(["test.csv", "test.json"])
    elif len(sys.argv) == 3:
        main(sys.argv)
    else:
        print("Need 2 arguments: <src.csv> <dest.json>")