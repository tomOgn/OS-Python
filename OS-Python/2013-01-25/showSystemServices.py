'''
Prova Pratica di Laboratorio di Sistemi Operativi
15 febbraio 2013
Esercizio 3

URL: http://www.cs.unibo.it/~renzo/so/pratiche/2013.01.25.pdf

@author: Tommaso Ognibene
'''

import os, sys

def main(argv):
    # Check number of arguments
    numArgs = len(argv)
    
    if len(argv) != 1:
        sys.exit("The function does not require arguments to be passed in.")
    
    # Build a dictionary with key-value pair {service - run levels}
    services = {}
    
    PopulateSystemServices(services)
    printServices(services)

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

def printServices(services):
    for key, values in sorted(services.items()):
        if values != () and key != "EADME":
            values = ' '.join(value for value in values)
            print('{0} {1}'.format(key, values))

if __name__ == "__main__":
    sys.exit(main(sys.argv))