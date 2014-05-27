'''
Prova Pratica di Laboratorio di Sistemi Operativi
12 febbraio 2009
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2009.02.12.pdf

@author: Tommaso Ognibene
'''

import os, sys, shutil

def Main(argv):
    # Sanity check
    if len(argv) != 4:
        sys.exit("The function requires three paramenters to be passed in.")
    for i in range(1, 4):
        if not os.path.isdir(argv[i]):
            sys.exit("The paramenters should be existing directories.")
    
    MergeTrees([argv[1], argv[2]], argv[3]);

    print("Done!")

'''
@summary: Merge directory trees into one destination tree.
          In case of more files having the same relative path, concatenate their content.
@param sources:     the list of source directories
@param destination: the destination directory
'''
def MergeTrees(sources, destination):
    # Populate dictionary with key-value pair { relative path - [source directory] }
    fileSource = { }
    for source in sources:
        for dirPath, dirNames, fileNames in os.walk(source, topdown=True):
            relPath = os.path.relpath(dirPath, source)
            for dirName in dirNames:
                path = os.path.join(destination, relPath, dirName)
                if not os.path.isdir(path):
                    os.mkdir(path)
            for fileName in fileNames:
                path = os.path.join(relPath, fileName)
                fileSource.setdefault(path, [])
                fileSource[path] += [source]
    # Merge through file concatenation     
    Concatenate(fileSource, destination)

'''
@summary: Merge files from a list of sources to one destination.
          In case of more files having the same relative path, concatenate their content.
@param fileSource:  dictionary with key-value pair { relative path - [source directory] }
@param destination: the destination directory
'''
def Concatenate(fileSource, destination):
    for key, value in fileSource.items():
        toPath = os.path.join(destination, key)
        with open(toPath, 'wb') as outfile:
            for source in value:
                fromPath = os.path.join(source, key)
                with open(fromPath, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv))