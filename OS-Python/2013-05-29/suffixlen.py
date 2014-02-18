'''
Prova Pratica di Laboratorio di Sistemi Operativi
29 maggio 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.05.29.pdf

@author: Tommaso Ognibene
'''

import os, sys

def Main(argv):
    # Check number of parameters
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
        return
    
    # Check parameters
    topDir = str(sys.argv[1])
    if not os.path.isdir(topDir):
        print("The parameter should be an existing directory.")
        return
    
    # Build a dictionary with key-value pair {file extension - total size}
    extensionSize = { }
    PopulateExtensionSize(topDir, extensionSize)
    
    # Print results
    PrintResults(extensionSize)

'''
@summary:  Walk through the directory tree and populate a dictionary 
           with key-value pair {file extension - total size}.
@param topDir:        the root directory
@param extensionSize: the dictionary
'''
def PopulateExtensionSize(topDir, extensionSize):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Compute the file extension
            fileExtension = fileName[fileName.find(".") : ]
            
            # Compute the size
            filePath = os.path.join(dirPath, fileName)   
            fileSize = os.path.getsize(filePath)
            
            # Update the dictionary
            extensionSize[fileExtension] = extensionSize.get(fileExtension, 0) + fileSize

# Print results
def PrintResults(extensionSize):
    for key, value in sorted(extensionSize.items()):
        print('{0}: {1} Bytes.'.format(key, value))
        
if __name__ == "__main__":
    sys.exit(Main(sys.argv))