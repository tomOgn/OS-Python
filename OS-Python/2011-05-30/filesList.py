'''
Prova Pratica di Laboratorio di Sistemi Operativi
30 maggio 2011
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2011.05.30.pdf

@author: Tommaso Ognibene
'''

import os, sys

'''
@summary: Walk through a directory tree.
          Populate a dictionary with key-value pair { file name - directories }.
@param topDir:   the root directory  
@param fileDirs: the dictionary
'''
def PopulateFileDirectories(topDir, fileDirs):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Find parent directory
            root = os.path.basename(topDir)
            parent = os.path.basename(dirPath)
            if root == parent: parent = ''
            parent = '/' + parent
            
            # Update dictionary
            fileDirs[fileName] = fileDirs.get(fileName, '') + parent + ' '
            

def main(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
        return
    
    # Check the parameter
    topDir = str(argv[1])
    if not os.path.isdir(topDir):
        print("The argument should be an existing directory.")
        return
    
    # Build a dictionary with key-value pair { file name - directories }
    fileDirs = {}
    
    PopulateFileDirectories(topDir, fileDirs)

    # Print results
    for key, value in sorted(fileDirs.items()):
        print("{0}\t{1}".format(key, value))
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))