// Author: Luke Grammer
// Date: 9/15/18

#include "BlockUtils.h"
#include <string>

const string FILENAME = "blkchp/blkchp";

int main() try
{

    pair<State, State> init_goal;
    Node *root;
    Node *goal;
    string problem_file, s = "0";

    while (true)
    { // Continually ask for user input, breaks out when s is 'q' or 'quit'
        printf("Please choose a problem number to solve (1-54) or enter 'Q' to quit\n");
        cin >> s;

        for (unsigned i = 0; i < s.size(); i++) // Change to lowercase
            s[i] = tolower(s[i]);

        if (s == "q" || s == "quit")
            break;

        if (stoi(s) < 10) // If problem 1-9, append 0 to s
            problem_file = FILENAME + "0" + to_string(stoi(s));
        else
            problem_file = FILENAME + to_string(stoi(s));

        init_goal = FileManager::read_problem(problem_file); // Read file
        root = new Node(init_goal.first, init_goal.second);
        goal = new Node(init_goal.second, init_goal.second);

        Search::GraphSearch(root, goal); // Search for goal starting from root

        delete root;
        delete goal;
    }
    return 0;
}
catch (invalid_argument)
{
    cerr << "Invalid argument entered!\nNext time enter an integer value (1-54) or 'Q' to quit.\n";
    return 1;
}
catch (exception &e)
{
    cerr << e.what() << "\n";
    return 2;
}
catch (...)
{
    cerr << "ERROR: An undefined exception occured\n";
    return 3;
}
