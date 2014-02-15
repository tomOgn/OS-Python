'''
Prova Pratica di Laboratorio di Sistemi Operativi
15 febbraio 2011
Esercizio 2

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2011.02.15.pdf

@author: Tommaso Ognibene
'''

import os, sys, subprocess, shlex

def main(argv):
    # Check number of parameters
    numArgs = len(argv)   
    if numArgs > 2:
        print("The function requires zero or one parameter to be passed in.")
        return
    
    if numArgs == 1:
        inputDir = os.getcwd()
    else:
        inputDir = str(argv[1])
        
        # Check the input directory
        if not os.path.isdir(inputDir):
            print("The argument should be an existing directory.")
            return
    
    # Build a dictionary with key-value pair { file type - file names }
    typeFiles = {}
    
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        fileType = getFileType(filePath)
        typeFiles[fileType] = typeFiles.get(fileType, []) + [fileName]
        
    # Print results
    for key, values in sorted(typeFiles.items()):
        print("{0}:\n\t{1}".format(key, "\n\t".join(value for value in values)))
    
def getFileType(filePath):
    command = 'file "' + os.path.normpath(filePath) + '"'
    # filePath = '/home/somewhere/example.zip'
    # output = 'example.zip: Zip archive data, at least v2.0 to extract'
    output = executeBash(command)
    # output = 'Zip archive data, at least v2.0 to extract'
    output = output.split(': ', 1)[1]
    # return 'Zip archive data'
    return output.split(',')[0]    

def executeBash(command):
    process = subprocess.Popen(shlex.split(command), stdout = subprocess.PIPE)
    return process.communicate()[0].split("\n")[0]
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))