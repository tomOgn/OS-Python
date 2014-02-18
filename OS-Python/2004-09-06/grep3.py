''' Prova Pratica di Laboratorio di Sistemi Operativi
06 settembre 2004
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2004.09.06.pdf

@author: Tommaso Ognibene  
'''

import os, sys, re

'''
@summary: Count the overlapping occurences of a pattern in a text
@param patternDict: dictionary with key-value pair {pattern - occurences}
@param text: text to be processed
'''
def CountOverlappingMatches(patternDict, text):
    start = 0
    for key, _ in patternDict.items():
        object = re.compile(key)
        match = object.search(text, start)
        while match is not None:
            patternDict[key] = patternDict.get(key, 0) + 1
            start = 1 + match.start()       
            match = object.search(text, start)

'''
@summary: Find the overlapping occurences of a patter in a text
@param pattern: regular expression patter
@param text: input text
@return: list of the overlapping occurences
'''
def FindOverlappingMatches(pattern, text):
    matches = []
    start = 0
    object = re.compile(pattern)
    match = object.search(text, start)
    while match is not None:
        matches.append(match.group())
        start = 1 + match.start()       
        match = object.search(text, start)
    return matches

def Main(argv, argc):
    # Pre-conditions:
    # [1] check number of arguments
    if argc != 3:
        print("The function requires two parameters to be passed in.")
        return
    
    # [2] check parameter
    if not os.path.isdir(argv[1]):
        print("The first parameter should be an existing directory.")
        return

    # Get the overlapping patterns from the input string
    inputDir = argv[1]
    inputString = argv[2]
    patterns = FindOverlappingMatches('.{3}', inputString) 
    
    # Build a dictionary with key-value pair {pattern - occurences}
    patternDict = { }
        
    for pattern in patterns:
        patternDict.setdefault(pattern, 0);  
        
    for fileName in os.listdir(inputDir):
        filePath = os.path.join(inputDir, fileName)
        with open(filePath) as file:   
            for line in file:
                CountOverlappingMatches(patternDict, line)
    
    for key, value in patternDict.items():
        print('{0}\t{1}'.format(key, value))
    
    print("Done!")
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))