#!/usr/local/bin/python3
'''
Prova Pratica di Laboratorio di Sistemi Operativi
25 luglio 2005
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2005.07.25.pdf

@author: Tommaso Ognibene
'''

import os, sys,re

def IsNatural(number):
    return number % 1 == 0 and number >= 0

def Average(numbers):
    return sum(numbers) / float(len(numbers))

def Main(argv, argc):
    # Pre-conditions:
    # [1] check number of arguments
    if argc < 3:
        print("The function requires at least two parameters to be passed in.")
        return
    
    # [2] check parameters
    if not os.path.isfile(argv[1]):
        print("The first parameter should be an existing file.")
        return  
    
    numColumns = argc - 2
    columns = argv[2 : ]
    for i in range(numColumns):
        if not columns[i].isdigit():
            print("The parameters after the file should be natural numbers.")
            return  
    
    # numbers of each chosen column
    values = [[] for i in range(numColumns)]
    
    with open(argv[1]) as file:   
        for line in file:
            match = re.findall('\d+', line) 
            if match:
                for i in range(numColumns):
                    value = int(match[int(columns[i]) - 1])
                    values[i].append(value)
    
    for i in range(numColumns):
        print(str(columns[i]) + ":" +
              " min:" + str(min(values[i])) +
              " max:" + str(max(values[i])) +
              " avg:" + str(Average(values[i])))
                    
if __name__ == "__main__":
    sys.exit(Main(sys.argv, len(sys.argv)))