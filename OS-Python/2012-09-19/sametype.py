'''
Prova Pratica di Laboratorio di Sistemi Operativi
19 settembre 2012
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2012.09.19.pdf

@author: Tommaso Ognibene
'''

import os, sys, subprocess

def main(argv):
    # Check number of parameters
    if len(argv) != 3:
        sys.exit("The function requires two parameters to be passed in.")
    
    # Check the two parameters
    inputFile = str(argv[1])
    topDir = str(argv[2])
    if not os.path.isfile(inputFile):
        sys.exit("First parameter should be an existing file.")
        
    if not os.path.isdir(topDir):
        sys.exit("Second parameter should be an existing directory.")
        
    fileType = getFileType(inputFile)
    sameTypeFiles = PopulateSameType(topDir, fileType)
    
    # Print results
    print("\n".join(file for file in sameTypeFiles))

'''
@summary:  Walk through the directory tree and populate a list
           of files belonging to a given type.
@param topDir:   the root directory
@param fileType: the given type
@return: the list
'''
def PopulateSameType(topDir, fileType):
    sameType = []
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            if GetFileType(filePath) == fileType:
                sameType.append(fileName)
    return sameType  

'''
@summary:  Get the type of a given file.
@param filePath: the file
@return: the file type
'''
def GetFileType(filePath):
    command = "file " + filePath
    # inputFile = 'example.zip'
    # output = 'example.zip: Zip archive data, at least v2.0 to extract'
    output = executeBash(command)
    # output = 'Zip archive data, at least v2.0 to extract'
    output = output.split(' ', 1)[1]
    # return 'Zip archive data'
    return output.split(',')[0]    

def executeBash(command):
    process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
    return process.communicate()[0].split("\n")[0]

if __name__ == "__main__":
    sys.exit(main(sys.argv))