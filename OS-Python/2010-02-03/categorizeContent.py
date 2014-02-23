#!/usr/local/bin/python3
'''
Prova Pratica di Laboratorio di Sistemi Operativi
03 febbraio 2010
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2010.02.03.pdf

@author: Tommaso Ognibene
'''

import os, sys
from stat import *

def Main(argv):
    # Check number of parameters
    if len(argv) != 1:
        sys.exit("The function does not require parameters to be passed in.")
    
    # Build a dictionary with key-value pair { category - number of elements }
    categoryNumber = {}
    categoryNumber["Directories"] = 0
    categoryNumber["Regular Files"] = 0
    categoryNumber["Device Files"] = 0
    populateCategoryNum(categoryNumber, os.getcwd())
    
       # Print results in command line
    for key, value in categoryNumber.items():
        print("{0}: {1}.".format(key, value))

    print("Done!")

'''
@summary: Walk through the directory tree and populate a dictionary 
          with key-value pair {category - number of elements}.
@param topDir:         the root directory
@param categoryNumber: the dictionary
'''
def populateCategoryNum(categoryNumber, topDir):
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

if __name__ == "__main__":
    sys.exit(Main(sys.argv))