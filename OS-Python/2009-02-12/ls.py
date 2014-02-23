'''
Prova Pratica di Laboratorio di Sistemi Operativi
12 febbraio 2009
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2009.02.12.pdf

@author: Tommaso Ognibene
'''

import os, sys, datetime, time

def Main(argv):
    # Check number of paramenters
    if len(argv) != 2:
        sys.exit("The function requires one paramenter to be passed in.")
    
    # Check the parameter
    if not (os.path.isdir(argv[1])):
       sys.exit("The paramenter should be an existing directory.")
    
    # Build a dictionary with key-value pair { file extension - files }
    extensionFile = {}

    # Populate the dictionary
    PopulateDictionary(argv[1], extensionFile)
    
    # Print sorted results
    for key, values in sorted(extensionFile.items()):
        values.sort(key=str.lower)
        print("{0}:\n\t{1}".format(key, "\n\t".join(value for value in values)))
    
    print("Done!")

# Populate a dictionary
def PopulateDictionary(inputDir, extensionFile):
    for fileName in os.listdir(inputDir):
        _, fileExtension = os.path.splitext(fileName)
        # Update the dictionary
        extensionFile[fileExtension] = extensionFile.get(fileExtension, []) + [fileName]
    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))