'''
Prova Pratica di Laboratorio di Sistemi Operativi
19 luglio 2010
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2010.09.13.pdf

@author: Tommaso Ognibene
'''

import os, sys, hashlib

def main(argv):
    # Check number of parameters
    if len(argv) != 3:
        print("The function needs two parameters to be passed in.")
        return;
    
    # Check input directories
    if not (os.path.isdir(argv[1])):
        print("First argument should be an existing directory.")
        return;
    
    if not (os.path.isdir(argv[2])):
        print("Second argument should be an existing directory.")
        return;
    
    # Build a dictionary with key-value pair { relative file path - MD5 hash }
    fileHash = {}
    
    for index in range(1, 3):
        compareDirectories(fileHash, argv[index])
    
    print("Done!")

# If first directory then populate the dictionary
# Otherwise find the modified files if any
def compareDirectories(fileHash, topDir):
    for dirPath, dirNames, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            hash = GetMd5Hash(filePath)
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            if not fileHash.get(relativePath, ""):
                fileHash[relativePath] = hash
            elif fileHash[relativePath] != hash:
                print("[{0}]".format(relativePath))

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

if __name__ == "__main__":
    sys.exit(main(sys.argv))