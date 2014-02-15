'''
Check if a word is a palindrome
'''

import sys

def IsPalindrome(word):
    # In case word is not a string
    if not type(word) is str:
        word = str(word)
    
    mid = len(word) / 2
    return word[:mid] == word[::-1][:mid]

def main(argv):
    # Check number of arguments
    if len(argv) != 2:
        print("The function requires one arguments to be passed in.")
        return
     
    # Check if parameter is a palindrome
    word = argv[1]
    print("The word {0} is {1}a palindrome.".format(word, "" if IsPalindrome(word) else "not "))
         
if __name__ == "__main__":
    sys.exit(main(sys.argv))