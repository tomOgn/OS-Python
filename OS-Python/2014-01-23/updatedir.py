'''
Prova Pratica di Laboratorio di Sistemi Operativi
23 gennaio 2014
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2014.01.23.pdf

@author: Tommaso Ognibene
'''

import os, sys, errno, hashlib, filecmp

'''
@summary: Get the MD5 hash without loading the whole file to memory.
          Break the file in chunks whose size is a multiple of 128.
          This takes advantage of the fact that MD5 has 128-byte digest blocks.
@param filePath:  physical address of a file 
@param chunkSize: chunk size in Bytes
@return: MD5 digest
'''
def GetMd5Hash(filePath, chunkSize = 2 ** 20):
    digest = hashlib.md5()
    with open(filePath, 'rb') as file:
        chunk = file.read(chunkSize)
        while chunk:
            digest.update(chunk)
            chunk = file.read(chunkSize)
    return digest.hexdigest()

'''
@summary: Check if two files have same content.
@param f1: file number 1
@param f2: file number 2
@return: TRUE, if they have same content
         FALSE, else
'''
def SameContent(f1, f2):
    if GetMd5Hash(f1) == GetMd5Hash(f2):
        if filecmp.cmp(f1, f2, shallow = False):
            return True
    return False

'''
@summary: Create a soft link in a forced way.
          If already exists, remove it and create a new one.
@param source:      source file
@param destination: destination file
'''
def CreateSoftLink(source, destination):
    try:
        os.symlink(source, destination)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(destination)
            os.symlink(source, destination)

'''
@summary: Entry point.
'''
def Main(argv):
    # Check number of parameters
    if len(argv) != 3:
        print("The function requires two parameters to be passed in.")
        return
    
    # Check parameters
    dirA = argv[1]
    if not os.path.isdir(dirA):
        print("The first parameter should be an existing directory.")
        return
    
    dirB = argv[2]
    if not os.path.isdir(dirB):
        print("The second parameter should be an existing directory.")
        return
       
    # Build a dictionary with key-value pair { file name - True }
    nameDict = { }
    
    for fileName in os.listdir(dirB):
        filePath = os.path.join(dirB, fileName)
        if os.path.isfile(filePath):
            print(filePath)
            nameDict[fileName] = True

    for fileName in os.listdir(dirA):
        filePathA = os.path.join(dirA, fileName)
        filePathB = os.path.join(dirB, fileName)
        if not nameDict.get(fileName, False):
            CreateSoftLink(filePathA, filePathB)
        elif nameDict.get(fileName, False) and not SameContent(filePathA, filePathB):
            CreateSoftLink(filePathA, filePathB)
        
if __name__ == "__main__":
    sys.exit(Main(sys.argv))