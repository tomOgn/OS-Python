'''
Prova Pratica di Laboratorio di Sistemi Operativi
19 gennaio 2011
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2011.01.19.pdf

@author: Tommaso Ognibene
'''

import os
import sys

'''
@summary: Walk through a directory tree.
          Populate a dictionary with key-value pair 
          { file name - (last modification - directory) }.
          Create soft links of the last modified files in a destination directory.
@param sources:     list of source directories  
@param n:           number of source directories
@param destination: the destination directory
'''
def MergeDirectories(sources, n, destination):
    # Populate the dictionary
    fileLastMod = {}
    
    for i in range(0, n):
        for fileName in os.listdir(sources[i]):
            filePath = os.path.join(sources[i], fileName)
            lastMod = os.path.getmtime(filePath)
            if fileLastMod.get(fileName, None) == None:
                fileLastMod[fileName] = (lastMod, sources[i])
            elif fileLastMod[fileName][0] < lastMod:
                fileLastMod[fileName] = (lastMod, sources[i])
           
    # Create the soft links
    for key, value in fileLastMod.items():
        srcPath = os.path.join(value[1], key)
        dstPath = os.path.join(destination, key)
        if not os.path.lexists(dstPath):
            os.symlink(srcPath, dstPath)

# Entry point
def Main(argv):
    # Check the number of arguments
    numArgs = len(argv)
        
    if numArgs != 4:
        print("The function needs three arguments to be passed in")
    else:
        # Check input directories
        mergingDir = []
        for index in range(1, 3):
            if not os.path.isabs(str(argv[index])):
                mergingDir.append(os.path.abspath(str(argv[index])))
            else:
                mergingDir.append(str(argv[index]))
        mergedDir = str(argv[3])
        
        if not (os.path.isdir(mergingDir[0])):
            print("Firts argument should be an existing directory")
        elif not (os.path.isdir(mergingDir[1])):
            print("Second argument should be an existing directory")
        elif not (os.path.isdir(mergedDir)):
            print("Third argument should be an existing directory")        
        else:
            MergeDirectories(mergingDir, 2, mergedDir)
                    
            print("Done!")

if __name__ == "__main__":
    sys.exit(Main(sys.argv))