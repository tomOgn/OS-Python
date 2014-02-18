''' FUN-ctions Repository

@summary: A repository of modular functions to be re-used
@author: Tommaso Ognibene
@version: 2014-02-14
'''

import os, errno, hashlib, operator, filecmp

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
@summary: Walk through the directory tree and populate a dictionary 
          with key-value pair {file size - [file names]}.
@param topDir:   the root directory
@param sameSize: the dictionary
'''
def PopulateSameSize(topDir, sameSize):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            fileSize = os.path.getsize(filePath)
            sameSize[fileSize] = sameSize.get(fileSize, []) + [filePath]  

'''
@summary: Read a list of file paths and populate a dictionary 
          with key-value pair {MD5 hash - [file names]}.
@param filePaths:   the list of physical addresses
@param sameContent: the dictionary
'''
def PopulateSameContent(filePaths, sameContent):
    for filePath in filePaths:
        md5 = GetMd5Hash(filePath)
        sameContent[md5] = sameContent.get(md5, []) + [filePath]
        
'''
@summary:  Walk through the directory tree and populate a dictionary 
           with key-value pair {file extension - total size}.
@param topDir:        the root directory
@param extensionSize: the dictionary
'''
def PopulateExtensionSize(topDir, extensionSize):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Compute the file extension
            fileExtension = fileName[fileName.find(".") : ]
            
            # Compute the size
            filePath = os.path.join(dirPath, fileName)   
            fileSize = os.path.getsize(filePath)
            
            # Update the dictionary
            extensionSize[fileExtension] = extensionSize.get(fileExtension, 0) + fileSize
            
'''
@summary:  Iterate the soft links in the directory /proc.
           Build a list of the active processes.
@param processes: the list
'''
def PopulateActiveProcesses(processes):
    for pid in os.listdir('/proc'):
        # Check if the soft link is accessible
        if pid.isdigit() and os.access('/proc/' + pid + '/exe', os.R_OK):
            path = os.readlink('/proc/' + pid + '/exe')
            processes.append(pid + ' ' + path)  

'''
@summary:  Get system services from /etc/init.d.
           Populate a dictionary with key-value pair {system service - run levels}.
@param services: the list
'''
def PopulateSystemServices(services):
    # Get system services from /etc/init.d
    for service in os.listdir('/etc/init.d'):
        services.setdefault(service, ())
    
    # Search system services for each run level
    for runLevel in range(0, 6):
        for file in os.listdir('/etc/rc' + str(runLevel)  + '.d'):
            # S20kerneloops ->
            # letter = 'S'
            # number = '20'
            # service = 'kerneloops'
            letter = file[0]
            number = "".join(character for character in file[1:] if character.isdigit())           
            service = file[len(number) + 1:]
            services[service] = services.get(service, ()) + ((letter + str(runLevel)),)

'''
@summary: Represenation of a file
'''
class File(object):
    def __init__(self, lastModification = None, relativePath = None):
        self.lastModification = lastModification
        self.relativePath = relativePath

'''
@summary:  Walk through the directory tree and populate a list of the files.
           Sort list by lastModification attribute in increasing order.
@param topDir: the root directory       
@param files: the list
'''
def PopulateLastModifications(topDir, files):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            lastModification = os.path.getmtime(filePath)
            relativePath = os.path.join(os.path.relpath(dirPath, topDir), fileName)
            files.append(File(lastModification, relativePath))
        files.sort(key = operator.attrgetter("lastModification"), reverse = False)

'''
@summary: Walk through a directory tree.
          Populate a dictionary with key-value pair { file name - directories }.
@param topDir:   the root directory  
@param fileDirs: the dictionary
'''
def PopulateFileDirectories(topDir, fileDirs):
    for dirPath, _, fileNames in os.walk(topDir):
        for fileName in fileNames:
            # Find parent directory
            root = os.path.basename(topDir)
            parent = os.path.basename(dirPath)
            if root == parent: parent = ''
            parent = '/' + parent
            
            # Update dictionary
            fileDirs[fileName] = fileDirs.get(fileName, '') + parent + ' '

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
@summary: Iterate the dictionary.
          Create a directory for every key.
          The value associated to every key is a list of files.
          For each new directory create soft links to these files
@param topDir:     the root directory
@param sameSuffix: the dictionary
'''
def CreateDirectoriesSymLinks(topDir, sameSuffix):
    for key, files in sameSuffix.items():
        dirPath = os.path.join(topDir, key)
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        for source in files:
            fileName = os.path.basename(source)
            destination = os.path.join(dirPath, fileName)
            if not os.path.lexists(destination):
                os.symlink(source, destination)

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

        