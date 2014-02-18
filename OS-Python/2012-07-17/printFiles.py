'''
Prova Pratica di Laboratorio di Sistemi Operativi
17 luglio 2012

Esercizio 3

http://www.cs.unibo.it/~renzo/so/pratiche/2012.07.17.pdf

@author: Tommaso Ognibene
'''

import os, sys

def main(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function requires one argument to be passed in.")
    else:
        # Check the parameter
        topDir = str(sys.argv[1])
        if not os.path.isdir(topDir):
            print("The argument should be an existing directory.")
            return
        
        # Build a dictionary with key-value pair { level - file names }
        files = {}

        # Get file names by a top-down traversal of the sub-tree
        level = -1
        for (_, _, fileNames) in os.walk(topDir, topdown = True):
            level += 1
            for fileName in fileNames:
                files[level] = files.get(level, ()) + (fileName,)
                    
        # Print results
        for key, value in files.items():
            print('Level {0}: {1}.'.format(key, sorted(value)) )  

if __name__ == "__main__":
    sys.exit(main(sys.argv))