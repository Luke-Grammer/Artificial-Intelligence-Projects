from os import system, name
from time import sleep
import Logic
import sys

def clear(): 
    """Clears the console on windows and unix"""
    # windows 
    if name == 'nt':
        _ = system('cls')
    # posix and linux 
    else: 
        _ = system('clear') 

def main():
    """Starting point for program"""
    KB = []
    #clear()
    try:
        if len(sys.argv) > 1:
            KB = Logic.readFile(sys.argv[1])
            if len(sys.argv) > 2:
                print("Results: ")
                for query in sys.argv[2:]:
                    for value in Logic.ask(KB, query):
                        print(value)
            else:
                print("No queries entered!")
                choice = input("Would you like to enter a query? (Y/N): ")
                clear()
                while choice.lower() == 'y' or choice.lower() == 'yes':
                    query = ""
                    while not query:
                        query = input("Please enter your query: ")
                    print("Results: ")
                    for value in Logic.ask(KB, query):
                        print(value)

                    choice = input("Would you like to enter another query? (Y/N): ")
                    if choice.lower() != 'y' and choice.lower() != 'yes' and choice.lower() != 'n' and choice.lower() != 'no':
                        print("Error: Unrecognized input!")
                        sleep(1)
                    clear()
        else:
            print("ERROR: Expected more command line arguments!")
    except AttributeError:
        print("ERROR: Improperly formatted query!")


if __name__ == '__main__': #Driver
    main()