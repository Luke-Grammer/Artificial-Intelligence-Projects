from os import system, name 
from DPLL import DPLL, find_symbols, format_clause
from time import sleep
import errno
import sys

def clear(): 
    """Clears the console on windows and unix"""
    # windows 
    if name == 'nt':
        _ = system('cls')
    # posix and linux 
    else: 
        _ = system('clear') 

def Read_File(filename):
    """Reads a file, removing any excess whitespace and comment lines beginning with '#'"""
    lines = [line.rstrip('\n') for line in open(filename)] # Strip newlines from file and read into list
    lines = [line.rstrip() for line in lines if not line.startswith('#') and line] # filter out empty lines and comment lines and strip trailing whitespace
    lines = [line.lstrip() for line in lines] # strip leading whitespace
    lines = [" ".join(line.split()) for line in lines] # Seperate each term in clause by exactly one space
    return lines


def Add_To_KB(KB, filename):
    """Adds formatted file contents to a propositional knowledge base if they are not already in the knowledge base"""
    try:
        file_clauses = Read_File(filename)
        for file_clause in file_clauses:
            if file_clause not in KB:
                KB.append(file_clause) # Add each clause to KB if not already present
    except IOError as x: # File access exception handling
        if x.errno == errno.ENOENT:
            print("Error: " + filename + " does not exist!")
        elif x.errno == errno.EACCES:
            print("Error: " + filename + " cannot be read!")
        input("Press 'ENTER' to continue. . .")


def Compute_Sat(KB, facts, print_info):
    """Prints symbols, propositions, and additional information from a knowledge base, 
    then runs a DPLL satisfiability search and prints the result"""
    # Create new KB initialized from current KB and extra facts
    new_KB = KB[:]
    for fact in facts:
        if fact not in KB:        
            new_KB.append(fact)
    symbols = find_symbols(new_KB) # Collect list of symbols
    model = {} # Initialize model to 'None' for each symbol 
    for symbol in symbols:
        model[symbol] = None
    print("Props:") # Print propositional symbols
    for symbol in symbols:
        print(symbol, end = ' ')
    print("\nInitial clauses:") # Print original KB
    i = 0
    for clause in KB:
        print(str(i) + ": " + format_clause(clause))
        i += 1
    if facts:
        print("Additional facts:") # Print additional facts
        for fact in facts:
            print(str(i) + ": " + format_clause(fact))
            i += 1
    print("-----------")
    model = DPLL(new_KB, symbols, model, print_info) # Satisfiability computation
    if model: # If the model was populated
        print("KB and additional facts can be satisfied with the given model")
        print(model)
        print("-----------")
        print("True props:")
        for assignment in model:
            if model[assignment]:
                print(assignment)
    else: # If no solution was returned
        print("There is no solution given the current KB and additional facts")


def Display_Main_Menu():
    """Displays a main menu"""
    print("1. Add file to knowledge base.")
    print("2. Clear knowledge base.")
    print("3. Compute satisfiability.")
    print("4. Add or remove additional facts.")
    print("5. Exit")
    choice = input("Please select a choice: ") # Collect user choice
    clear()
    choice = choice.lstrip() #Strip whitespace
    choice = choice.rstrip()
    return choice


def Display_Fact_Menu():
    """Displays a sub-menu for managing additional facts"""
    clear() 
    print("1. Add a fact")
    print("2. Remove a fact")
    print("3. Clear facts")
    print("4. Return to menu") 
    choice = input("Please select a choice: ") # Collect user choice
    choice = choice.lstrip() #Strip whitespace
    choice = choice.rstrip()
    return choice


def main():
    """Starting point for program"""
    KB = [] # Initialize KB and facts to be empty
    facts = []
    if (len(sys.argv) == 1):
        while(True):
            clear()
            if (len(KB) > 200): # Display KB and facts if they aren't too long
                print("Current KB too large to display, length = ", len(KB))
            else:
                print("Current KB = ", KB)
            if (len(facts) > 200 ):
                print("Current fact list to large to display, length = ", len(facts))
            else:
                print("Current facts = ", facts)

            #Display main menu
            choice = Display_Main_Menu()

            if(choice == "1"): # Add file to knowledge base
                filename = input("Please enter filename: ")
                Add_To_KB(KB, filename)

            elif(choice == "2"): # Clear KB
                KB = []

            elif(choice == "3"): # Compute Satisfiability
                while(True): # Collect input for displaying extra tracing info
                    clear()
                    choice = input("Print additional tracing information? (Y/N) ")
                    if choice.lower() == 'y' or choice.lower() == 'yes':
                        print_info = True
                        break
                    elif choice.lower() == 'n' or choice.lower() == 'no':
                        print_info = False
                        break
                    else:
                        print("Unrecognized input, please try again.")
                        sleep(0.5)

                Compute_Sat(KB, facts, print_info)
                print()
                input("Press 'ENTER' to return to the main menu. . .")

            elif(choice == "4"): # Add or remove additional facts

                while(True): # Sub-menu for additional facts

                    choice = Display_Fact_Menu()

                    if(choice == "1"): # Add a fact
                        clear()
                        print("(Please enter facts of the form 'A -B' where whitespace is an implicit or and - means negation)")
                        fact = input("Please enter fact to insert: ")
                        if fact not in facts:
                            fact = fact.lstrip() # Strip whitespace and add fact if not already in additional facts
                            fact = fact.rstrip()
                            fact = " ".join(fact.split())
                            if fact:
                                facts.append(fact)
                            print("Fact added")
                        else:
                            print("Fact already in facts")
                        sleep(0.5)

                    elif(choice == "2"): # Remove a fact
                        clear()
                        fact= input("Please enter fact to remove: ")
                        fact = fact.lstrip() # Strip whitespace and remove fact if it is in additional facts
                        fact = fact.rstrip()
                        fact = " ".join(fact.split())
                        if fact in facts: 
                            facts.remove(fact)
                            print("Fact removed")
                        else:
                            print("Fact not found")
                        sleep(0.5)

                    elif(choice == "3"): # Clear facts
                        facts = []
                        print("Facts cleared.")
                        sleep(0.5)

                    elif(choice == "4"): # Return to menu
                        break

                    else:
                        print("Unrecognized choice, returning to menu")
                        sleep(1)
                        break

            elif(choice == "5"): # Exit
                break

            else:
                print("Unrecognized choice, returning to menu")
                sleep(1)
    else: # Populate KB with command line arguments and run satisfiability search
        for i in range(1,len(sys.argv)):
            Add_To_KB(KB, sys.argv[i])
        Compute_Sat(KB, facts, True)


if __name__ == '__main__': #Driver
    main()