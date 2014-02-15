'''
Prova Pratica di Laboratorio di Sistemi Operativi
13 settembre 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.09.13.pdf

@author: Tommaso Ognibene
'''

import os, sys

def Main(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function only needs one argument to be passed in")
        return
    
    # Check the parameter
    inputDir = str(sys.argv[1])
    if not os.path.isdir(inputDir):
        print("The argument should be an existing directory")
        return
    
    # Build a dictionary with key-value pair { line - number of characters }
    numChars = { }

    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        lineNumber = 1       
        with open(filePath, 'r') as file:
            for line in file:
                numChars[lineNumber] = numChars.get(lineNumber, 0) + len(line) - 1
                lineNumber = lineNumber + 1
                
    for key, value in sorted(numChars.items()):
        print('{0} {1}'.format(key, value))
        
if __name__ == "__main__":
    sys.exit(Main(sys.argv))