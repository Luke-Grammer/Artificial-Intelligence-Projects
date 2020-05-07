
def main():
    states = ['WA', 'NT', 'SA', 'Q', 'V', 'NSW', 'T']
    colors = ['r', 'g', 'b']
    adjacent = [('WA', 'NT'), ('WA', 'SA'), 
                ('NT', 'SA'), ('NT', 'Q'), 
                ('SA', 'Q'), ('SA', 'NSW'), 
                ('SA', 'V'), ('Q', 'NSW'), 
                ('NSW', 'V')]
    print("Writing to file. . .")
    f = open('map_clauses.cnf', 'w')
    f.write("# Boolean clauses representing the knowledge base of the Australia map coloring problem in CNF\n")
    
    for state in states: # Each state is at least one color
        f.write('\n')
        for color in colors:
            f.write(state + color + " ")

        f.write('\n')
        for color in colors: # Each state is at most one color
            for other_color in colors:
                if color is not other_color:
                    f.write('-' + state + color + " -" + state + other_color + "\n")

    f.write('\n')
    for state1, state2 in adjacent: # Each state cannot be the same color as it's neighbor
        for color in colors:
            f.write("-" + state1 + color + " -" + state2 + color + "\n")

    print("Done!")


if __name__ == '__main__':
    main()