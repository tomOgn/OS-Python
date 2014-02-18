'''
Prova Pratica di Laboratorio di Sistemi Operativi
12 febbraio 2009
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2009.02.12.pdf

@author: Tommaso Ognibene
'''

import os, sys, datetime, time

def Main(argv):
    # Verify preconditions
    Preconditions(argv)
    
    # Build a dictionary with key-value pair { file extension - files }
    extensionFile = {}

    # Populate the dictionary
    PopulateDictionary(argv[1], extensionFile)
    
    # Order the dictionary
    
    # Print the dictionary
    
    print("Done!")

def Preconditions(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
        return
    
    # Check parameter
    if not (os.path.isdir(argv[1])):
        print("Paramenter should be an existing directory.")
        return;

# Populate a dictionary
def PopulateDictionary(inputDir, extensionFile):
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        fileName, fileExtension = os.path.splitext(fileName)
        # Update the dictionary
        extensionFile[fileExtension] = extensionFile.get(fileExtension, []) + [fileName]
        
def OrderDictionary():
            for key, value in files.items():
            print('Level {0}: {1}.'.format(key, sorted(value)) ) 

    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))