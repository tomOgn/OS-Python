'''
Prova Pratica di Laboratorio di Sistemi Operativi
20 febbraio 2014
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2014.02.20.pdf

@author: Tommaso Ognibene
'''

import os, sys, errno, filecmp

'''
@summary: Entry point.
'''
def Main(argv):
    # Check number of parameters
    if len(argv) != 3:
        print("The function requires two parameters to be passed in.")
        return
    
    # Check parameters
    dirA = argv[1]
    if not os.path.isdir(dirA):
        print("The first parameter should be an existing directory.")
        return
    
    dirB = argv[2]
    if not os.path.isdir(dirB):
        print("The second parameter should be an existing directory.")
        return
       
    # Build a dictionary with key-value pair { file name - True }
    nameDict = { }
    
    for fileName in os.listdir(dirB):
        filePath = os.path.join(dirB, fileName)
        if os.path.isfile(filePath):
            nameDict[fileName] = True

    for fileName in os.listdir(dirA):
        filePathA = os.path.join(dirA, fileName)
        filePathB = os.path.join(dirB, fileName)
        if not nameDict.get(fileName, False):
            os.link(filePathA, filePathB)
        elif os.path.getmtime(filePathA) > os.path.getmtime(filePathB):
            os.remove(filePathB)
            os.link(filePathA, filePathB)
        
if __name__ == "__main__":
    sys.exit(Main(sys.argv))