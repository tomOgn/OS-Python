'''
Prova Pratica di Laboratorio di Sistemi Operativi
03 febbraio 2010
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2010.02.03.pdf

@author: Tommaso Ognibene
'''

import os, sys
from stat import *

def main(argv):
    # Check number of arguments
    if len(argv) != 1:
        print("The function does not require arguments.")
        return
    
    # Build a dictionary with key-value pair { category - number of elements }
    categoryNumber = {}
    categoryNumber["Directories"] = 0
    categoryNumber["Regular Files"] = 0
    categoryNumber["Device Files"] = 0
    populateDictionary(categoryNumber, os.getcwd())
    
    printResults(categoryNumber)

    print("Done!")

# Categorize every object within the given top directory
def populateDictionary(categoryNumber, topDir):
    for dirPath, dirNames, fileNames in os.walk(topDir):
        # Update number of directories
        categoryNumber["Directories"] += len(dirNames)
        
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            fileMode = os.stat(filePath).st_mode
            
            if S_ISREG(fileMode):
                # Update number of regular files
                categoryNumber["Regular Files"] += 1
            elif S_ISBLK(fileMode) or S_ISCHR(fileMode):
                # Update number of device files
                categoryNumber["Device Files"] += 1   

# Print results in command line
def printResults(categoryNumber):
    print("Catogory: Number of elements.")               
    for key, value in categoryNumber.items():
        print("{0}: {1}.".format(key, value))

if __name__ == "__main__":
    sys.exit(main(sys.argv))