
backtracks = 0
nodes_visited = 0
choice_points = 0

def DPLL(KB, symbols, model, print_info):
    """Resets global variables for keeping track of backtracks and visited nodes, and calls DPLL_helper"""
    global backtracks
    global nodes_visited
    global choice_points
    backtracks = 0
    nodes_visited = 0   
    choice_points = 0 
    return DPLL_helper(KB, symbols, model, print_info)


def DPLL_helper(KB, symbols, model, print_info):
    """Computes satisfiability for arbitrary CNF knowledge base given 
    symbol list and model dictionary by default initialized to None for each 
    symbol and returns the satisfying model or False if unsatisfiable."""
    global nodes_visited
    global choice_points
    nodes_visited += 1 # Increment the global nodes_visited

    if print_info:
        print("Model:", model) # Print model (If printing tracing info)

    if None not in model.values(): # If all symbols in model are assigned a value
        for assignment in evaluate(KB, model):
            if not assignment: # If some clause evaluates to false, model does not satisfy KB 
                return False
        if model: # If complete model is satisfying and non-empty (If the number of symbols is not zero)
            print("Success!") 
            print("-----------")
            print("Total backtracks: ", backtracks)
            print("Total choice points: ", choice_points)
            print("Total nodes visited: ", nodes_visited)
            return model
        else: # If complete model is empty, return unsatisfiable
            return False
        
    p = find_unit_clause(KB, model, print_info)# Find unit clause in KB
    if not p:
        p = find_pure_symbol(KB, symbols, model, print_info) # Find pure symbol in KB

    if p: # If unit clause was found, update model
        if p.startswith('-'):
            model[p[1:]] = False
            new_symbols = [x for x in symbols if x != p[1:]] 
        else:
            model[p] = True
            new_symbols = [x for x in symbols if x != p]
        return DPLL_helper(KB, new_symbols, model, print_info) # Continue search with new model

    p = symbols[0]
    rest = symbols[1:] 
    temp_model = dict(model)
    model[p] = True # Create a model where the next unassigned symbol is true
    temp_model[p] = False # Create a model where the next unassigned symbol is false
    if print_info:
        print("Choice point for", p)
        print("Choosing True")
    choice_points += 1
    # If either model finds a solution, return the satisfying model
    return DPLL_helper(KB, rest, model, print_info) or backtrack(KB, p, rest, temp_model, print_info)
    

def backtrack(KB, p, symbols, model, print_info):
    """Prints to console, updates backtracks, and returns result of DPLL search with the given model and KB."""
    global backtracks
    backtracks += 1 # Increment the number of backtracks

    if print_info:
        print("Backtrack!")
        print("Choosing False for", p)
    return DPLL_helper(KB, symbols, model, print_info)


def find_symbols(KB):
    """Returns a list of all unique symbols in an arbitrary CNF knowledge base."""
    symbols = [] # List of symbols initially empty
    for clause in KB: # Loop through every clause in the KB
        clause = clause.split() 
        for term in clause: # Loop through every term in clause, adding symbol to list if not already present
            if term.startswith('-'):
                term = term[1:]
            if term not in symbols: 
                symbols.append(term)
    symbols.sort() # Sort symbol list
    return symbols


def evaluate(KB, model):
    """Returns a list of truth values (one for each clause in the KB) 
    given a complete model and CNF knowledge base"""
    assignments = [] # List of assignments initially empty
    for clause in KB: # Loop through every clause in the KB
        clause = clause.split() 
        assignments.append(False) # By default make evaluation false
        for term in clause: # Loop through every term in the clause
            # If any term evaluates to true with given model, replace the clause's assignment with true
            if term.startswith('-'): 
                term = term[1:]
                if model[term] is False:
                    assignments.pop()
                    assignments.append(True)
                    break 
            else:
                if model[term] is True:
                    assignments.pop()
                    assignments.append(True)
                    break
    return assignments


def find_unit_clause(KB, model, print_info):
    """Finds a unit clause in a CNF knowledge base that is not yet value-initialized in model"""
    
    for symbol in model: # Loop through symbols in model
        if model[symbol] is not None: # If the model already has an assignment for the symbol, keep looking
            continue
        
        for clause in KB: # Loop through clauses in the KB
            clause = clause.split()

            if symbol not in clause and "-" + symbol not in clause: # If the current symbol is not in the clause, skip to next clause
                continue
            
            if symbol in clause and "-" + symbol in clause: # If the current symbol appears both both negated and positive in the same clause, skip to next clause
                continue
            
            if symbol in clause: # If the symbol appears positive, it must be positive if it is a unit clause
                force_value = True 
            else:
                force_value = False # Likewise if negative, it must be negative if unit clause

            skip = False # Initialize skip to false

            for term in clause: # Loop through each term in clause
                if term.startswith('-'): # If term is negative
                    if term[1:] == symbol: # If the term is the current symbol, skip
                        continue
                    else:
                        if model[term[1:]] is False or model[term[1:]] is None: # Otherwise, if another term is true or empty, skip clause
                            skip = True
                            break

                else: # If term is positive symbol
                    if term == symbol: # If the term is the current symbol, skip
                        continue
                    else:
                        if model[term] is True or model[term] is None: # Otherwise, if another term is true or empty, skip clause
                            skip = True
                            break
            
            if skip is False: # If clause was not skipped, it is a unit clause
                if print_info:
                    print("Unit clause on " + format_clause(" ".join(clause)) + " implies " + symbol + " is " + str(force_value))
                if symbol in clause:
                    return symbol
                else:
                    return "-" + symbol


def find_pure_symbol(KB, symbols, model, print_info):
    """Finds a pure symbol in a CNF knowledge base that is not yet value-initialized in model"""
    tracker = None

    for symbol in symbols: # Loop through symbols in model
        skip = False # Initialize skip to false

        if model[symbol] is not None: # If model is already assigned a value, skip
            continue

        for clause in KB: # Loop through clauses in KB
            if skip: # if skip is true, go to next symbol
                break
            
            clause = clause.split()
            if symbol not in clause and "-" + symbol not in clause: # If the symbol does not appear in the clause, skip to next clause
                continue
            
            for term in clause: # Loop through terms in clause
                if term.startswith('-'): # If it's negated and equals the current symbol
                    if term[1:] == symbol:
                        if tracker is None: # If tracker is uninitialized, initialize it to false
                            tracker = False
                        if tracker is True: # If tracker is true, it appears positively somewhere else, and is not pure.
                            tracker = None # Reset tracker
                            skip = True # Skip to next symbol
                            break
                else: # If it's positive and equals the current symbol
                    if term == symbol:
                        if tracker is None: # If tracker is uninitialized, initialize it to true
                            tracker = True
                        if tracker is False: # If tracker is false, it appears negatively somewhere else, and is not pure.
                            tracker = None # Reset tracker
                            skip = True # Skip to next symbol
                            break
        
        if tracker is not None: # If the tracker was initialized and never reset, then the current symbol is pure
            if print_info:
                print("Found pure symbol", symbol)
            if tracker is True:
                if print_info:
                    print("Setting to True")
                return symbol
            else: 
                if print_info:
                    print("Setting to False")
                return '-' + symbol

    
def format_clause(clause):
    """Joins together terms in a whitespace seperated CNF clause with 'v' symbols"""
    return "(" + " v ".join(clause.split()) + ")"