'''
Prova Pratica di Laboratorio di Sistemi Operativi
18 luglio 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.07.18.pdf

@author: Tommaso Ognibene
'''

import os, sys

def Main(argv):
    # Check number of arguments
    if len(argv) != 3:
        print("The function requires two arguments to be passed in.")
        return
    
    # Check parameters
    srcDir = str(argv[1])
    dstDir = str(argv[2])
    if not os.path.isdir(srcDir):
        print("First argument should be an existing directory.")
        return
    if not os.path.isdir(dstDir):
        print("Second argument should be an existing directory.")
        return
    
    # Build a dictionary with key-value pair {file base name - occurences}
    nameFreq = { }
    for dirPath, dirNames, fileNames in os.walk(srcDir):
        for fileName in fileNames:
            nameFreq[fileName] = nameFreq.get(fileName, -1) + 1
            
            # Create a soft link
            freq = nameFreq[fileName]
            linkName = "{0}{1}".format(fileName, str(freq) if freq > 0 else "")
            srcPath = os.path.join(os.path.abspath(dirPath), fileName)
            dstPath = os.path.join(dstDir, linkName)
            if not os.path.lexists(dstPath):
                os.symlink(srcPath, dstPath)
        
    print("Done!")

if __name__ == "__main__":
    sys.exit(Main(sys.argv))