'''
Prova Pratica di Laboratorio di Sistemi Operativi
21 giugno 2010
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2010-06-21.pdf

@author: Tommaso Ognibene
'''

import os, sys, hashlib, errno

def main(argv):
    # Check number of parameters
    if len(argv) != 1:
        sys.exit("The function does not require parameters.")
    
    sameSuffix = {}
    PopulateSameSuffix(os.getcwd(), sameSuffix)
    CreateDirectoriesSymLinks(os.getcwd(), sameSuffix)
    
    print("Done!")

'''
@summary: Walk through the directory tree.
          Get the suffix of each file.
          Populate a dictionary with key-value pair {suffix - [file paths]}.
@param topDir:     the root directory
@param suffixFile: the dictionary
'''
# Build a dictionary with key-value pair { suffix - [file path] }
def PopulateSameSuffix(topDir, sameSuffix):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            _, suffix = os.path.splitext(fileName)
            filePath = os.path.join(dirPath, fileName)
            sameSuffix[suffix] = sameSuffix.get(suffix, []) + [filePath]

'''
@summary: Create a soft link in a forced way.
          If already exists, remove it and create a new one.
@param src: source file
@param dst: destination file
'''
def CreateSoftLink(src, dst):
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)

'''
@summary: Iterate the dictionary.
          Create a directory for every key.
          The value associated to every key is a list of fils.
          Each new directory shall contain soft links to these files
@param topDir:     the root directory
@param sameSuffix: the dictionary
'''
def CreateDirectoriesSymLinks(topDir, sameSuffix):
    for key, files in sameSuffix.items():
        dirPath = os.path.join(topDir, key)
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        for src in files:
            fileName = os.path.basename(src)
            dst = os.path.join(dirPath, fileName)         
            CreateSoftLink(src, dst)
            
if __name__ == "__main__":
    sys.exit(main(sys.argv))