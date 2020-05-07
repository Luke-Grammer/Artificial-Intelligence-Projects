import sys

def main():
    if len(sys.argv) != 2: # Checking command line arguments
        print("ERROR: Expected a single command line argument!")
        return
    if not sys.argv[1].isdigit():
        print("ERROR: Command line argument expected a digit!")
        return

    N = int(sys.argv[1])
    rows = N + 1
    cols = N + 1

    print("Writing to file. . .")
    f = open( str(N) + '_queens_clauses.cnf', 'w')
    f.write("# Boolean clauses representing the knowledge base of the " + str(N) + " queens problem in CNF\n")
    
    for i in range(1, rows): # Each row has at least one queen
        for j in range(1, cols):
            f.write("Q" + str(i) + str(j) + " ")
        f.write("\n")
    
    f.write("\n\n")
    for i in range(1, rows): # Each column has at least one queen
        for j in range(1, cols):
            f.write("Q" + str(j) + str(i) + " ")
        f.write("\n")

    f.write("\n\n")
    for i in range(1, rows): # Each row has at most one queen
        for j in range(1, cols):
            for k in range(j, cols):
                if j != k:
                    f.write("-Q" + str(i) + str(j) + " " + "-Q" + str(i) + str(k) + "\n")
        f.write("\n")

    f.write("\n")
    for i in range(1, cols): # Each column has at most one queen
        for j in range(1, rows):
            for k in range(j, rows):
                if j != k:
                    f.write("-Q" + str(j) + str(i) + " " + "-Q" + str(k) + str(i) + "\n")
        f.write("\n")

    f.write("\n")
    for i in range(1, rows): # No queens can be in the diagonal of another queen
        for j in range(1, cols):
            for k,l in zip(range(i + 1, rows), range(j + 1, cols)): # Right diagonal
                f.write("-Q" + str(i) + str(j) + " -Q" + str(k) + str(l) + "\n")

            for k,l in zip(range(i + 1, rows), range(j - 1, 0, -1)): # Left diagonal
                f.write("-Q" + str(i) + str(j) + " -Q" + str(k) + str(l) + "\n")
        f.write("\n")

    
    print("Done!")
    

if __name__ == '__main__':
    main()