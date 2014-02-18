'''
Prova Pratica di Laboratorio di Sistemi Operativi
20 settembre 2005
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2005.09.20.pdf

@author: Tommaso Ognibene
'''

import os, sys

def Main(argv):
    # Pre-conditions:
    # (*) check number of arguments
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
        return
    
    # (*) check parameters
    if not os.path.isdir(argv[1]):
        print("The argument should be an existing directory.")
        return  
    
    # Build, sort and print a list of relative pathnames
    paths = []
    topDir = argv[1]
    BuildList(paths, topDir)
    if paths != None:
        paths.sort(key=len)
        print("\n".join(path for path in paths))
        print("Done!")
    else:
        print("No files found.")
    
def BuildList(paths, topDir):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            paths.append(relativePath)

if __name__ == "__main__":
    sys.exit(Main(sys.argv))