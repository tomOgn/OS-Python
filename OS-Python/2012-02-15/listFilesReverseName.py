'''
Prova Pratica di Laboratorio di Sistemi Operativi
15 febbraio 2012
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2012-02-15.pdf

@author: Tommaso Ognibene
'''

import os, sys

def main(argv):
    # Check number of parameters
    if len(argv) != 2:
        sys.exit("The function only needs one parameter to be passed in.")
    
    # Check the parameter
    inputDir = str(sys.argv[1])
    if not os.path.isdir(inputDir):
        sys.exit("The parameter should be an existing directory.")
    
    # Build a dictionary with key-value pair { file name - True/False }
    fileNames = { }
    
    # Build a list containing the names to print
    namesToPrint = []
    
    for file in os.listdir(inputDir):
        # Remove extension
        fileName, _ = os.path.splitext(file)
        # First check if file is a palindrome
        mid = len(fileName) / 2
        if fileName[:mid] == fileName[mid::-1]:
            namesToPrint.append(fileName)
        # Else check if the reversed has been discovered
        elif fileNames.get(fileName[::-1], False):
            # 'example' and 'elpmaxe' are both in the directory
            namesToPrint.append(fileName)
            namesToPrint.append(fileName[::-1])
        # Else update the dictionary
        else:
            fileNames[fileName] = True
    
    # Print results
    print("\n".join(name for name in namesToPrint))
 
if __name__ == "__main__":
    sys.exit(main(sys.argv))