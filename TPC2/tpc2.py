from sys import stdin

def main():
    on = False
    totalsum = 0
    
    for line in stdin:
        line = line.lower()
        i = 0
        
        while i < len(line):
            
            if(line[i] == '='):
                print(f"A soma atual é: {totalsum}")
                i += 1
                
            else:
                if(on):
                    if(line[i].isdigit()):
                            
                        j = 1
                        
                        while(i+j < len(line) and line[i+j].isdigit()):
                            j += 1
                        
                        totalsum += int(line[i:i+j])
                        i += j
                
                if(line[i:i+2] == 'on'):
                    on = True
                    i += 2
                
                elif(line[i:i+3] == 'off'):
                    on = False
                    i += 3
                                
                else:
                    i += 1

main()