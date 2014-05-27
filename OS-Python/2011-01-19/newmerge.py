'''
Prova Pratica di Laboratorio di Sistemi Operativi
19 gennaio 2011
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2011.01.19.pdf

@author: Tommaso Ognibene
'''

import os, sys

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
           
    # Generate the soft links
    for key, value in fileLastMod.items():
        srcPath = os.path.join(value[1], key)
        dstPath = os.path.join(destination, key)
        if not os.path.lexists(dstPath):
            os.symlink(srcPath, dstPath)

# Entry point
def Main(argv, argc):
    
    # Perform a sanity check and parse the parameters
    if argc < 4:
        sys.exit("The function requires at least three parameters to be passed in.")

    last = argc - 1
    source = []
    for i in range(1, last):      
        if not os.path.isabs(argv[i]):
            source.append(os.path.abspath(argv[i]))
        else:
            source.append(argv[i])
            
        if not os.path.isdir(source[i - 1]):
            sys.exit("The parameters should be existing directories.") 
            
    destination = argv[last]     
   
    MergeDirectories(source, last - 1, destination)
            
    print("Done!")

if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))