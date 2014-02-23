''' Prova Pratica di Laboratorio di Sistemi Operativi
24 settembre 2003
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2003.09.24.pdf

@author: Tommaso Ognibene  
'''

import os, sys

class Exam:
    Resources = 0
    Concurrency = 0
    def __init__(self):
        pass

def GenerateHTML(dateSize, inputDir):
    table = []
    table.append(['Data',   'Gestione Risorse',   'Concorrenza'])

    # Iterate files in the directory
    for fileName in os.listdir(inputDir):
        table.append([fileName,   'Gestione Risorse',   'Concorrenza'])
    
    for key, value in dateSize.items():
        table.append([key,   value.Resources,   value.Concurrency])
        
    htmlcode = HTML.table(table_data)
    print(htmlcode)
    htmlcode = HTML.link('Decalage website', 'http://www.decalage.info')
    print(htmlcode)

def Main(argv, argc):
    # Pre-conditions:
    # [1] Check number of parameters
    if argc != 2:
        sys.exit("The function requires one parameter to be passed in.")
    
    # [2] Check parameters
    inputDir = argv[1]
    if not (os.path.isdir(inputDir)):
        sys.exit("The paramenter should be an existing directory.")
    
    dateSize = {}
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        fileName, _ = os.path.splitext(fileName)
        date = fileName[:-4]
        pattern = fileName[-3:]
        dateSize.setdefault(date, Exam())
        size = os.path.getsize(filePath)
        print(pattern)
        print(size)
        if pattern == "con":
            dateSize[date].Concurrency = size
        else:
            dateSize[date].Resources = size
                  
    table = []
    table.append(['Data',   'Gestione Risorse',   'Concorrenza'])

    # Iterate files in the directory    
    for key, value in dateSize.items():
        table.append([key,   value.Resources,   value.Concurrency])
        
    print(table)
    
    print("Done!")
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))