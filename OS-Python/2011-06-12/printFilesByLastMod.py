'''
Prova Pratica di Laboratorio di Sistemi Operativi
22 giugno 2011
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2011.06.22.pdf

@author: Tommaso Ognibene
'''

import os, sys, operator

'''
@summary: Represenation of a file
'''
class File(object):
    def __init__(self, lastModification = None, relativePath = None):
        self.lastModification = lastModification
        self.relativePath = relativePath

'''
@summary:  Walk through the directory tree and populate a list of the files.
           Sort list by lastModification attribute in increasing order.
@param topDir: the root directory       
@param files:  the list
'''
def PopulateLastModifications(topDir, files):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            lastModification = os.path.getmtime(filePath)
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            files.append(File(lastModification, relativePath))
        files.sort(key = operator.attrgetter("lastModification"), reverse = False)

def Main(argv):
    # Check number of arguments
    numArgs = len(argv)
    if numArgs != 2:
        print("The function needs one argument to be passed in.")
        return
    
    # Check parameters
    topDir = str(argv[1])
    if not os.path.isdir(topDir):
        print("The argument should be an existing directory.")
        return
    
    # Build a list of file elements 
    files = []
    PopulateLastModifications(topDir, files)
    
    # Print results
    print("\n".join(file.relativePath for file in files))
    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))