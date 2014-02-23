'''
Prova Pratica di Laboratorio di Sistemi Operativi
13 settembre 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.09.13.pdf

@author: Tommaso Ognibene
'''

import os, sys

'''
@summary: Iterate the files of a directory.
          Populate a dictionary with key-value pair { line - number of characters }.
@param inputDir:   the input directory  
@return: the dictionary
'''
def PopulateDictionaryNumChars(inputDir):
    numChars = { }
    
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        lineNumber = 1       
        with open(filePath, 'r') as file:
            for line in file:
                numChars[lineNumber] = numChars.get(lineNumber, 0) + len(line) - 1
                lineNumber = lineNumber + 1
    
    return numChars
    
'''
@summary: Entry point.
'''
def Main(argv):
    # Check number of parameters
    if len(argv) != 2:
        sys.exit("The function requires only one parameter to be passed in.")
    
    # Check the parameter
    inputDir = str(sys.argv[1])
    if not os.path.isdir(inputDir):
        sys.exit("The parameter should be an existing directory.")
    
    # Build a dictionary with key-value pair { line - number of characters }
    numChars = PopulateDictionaryNumChars(inputDir)
                
    for key, value in sorted(numChars.items()):
        print('{0} {1}'.format(key, value))
        
if __name__ == "__main__":
    sys.exit(Main(sys.argv))