// Author: Luke Grammer
// Date: 9/15/18

#include "Node.h"

Node::Node(const State &s, const State &goal, int depth, Node *par) : state{s}, parent{par}, depth{depth}
{ // Initializes all nodes between 'root' and 'goal'
    h = s.heuristic(goal);
    f = depth + h; 
}

Node::Node(const State &s, int depth, Node *par) : state{s}, parent{par}, depth{depth}, f{0} {} // Initializes 'root' and 'goal' nodes

vector<Node *> Node::successors(State goal)
{ // Find successors of a given state
    char letter_to_move;
    vector<Node *> succ;
    State temp_state_1(state);

    for (unsigned i = 0; i < temp_state_1.stacks.size(); i++) 
    { // Search through temp_state's stacks
        temp_state_1 = state;
        letter_to_move = '\0';

        int j = 0;
        while (temp_state_1.stacks[i][j])
        { // Find top block in stack
            letter_to_move = temp_state_1.stacks[i][j];
            j++;
        }

        if (letter_to_move == '\0')
            continue;

        temp_state_1.stacks[i][j - 1] = '\0'; // Remove top block

        State temp_state_2(state); // Make new temporary state

        for (unsigned k = 0; k < temp_state_2.stacks.size(); k++)
        { // Loop through stacks
            if (k != i)
            { // If on a different stack than the one we removed the block from
                temp_state_2 = temp_state_1;

                j = 0;
                while (temp_state_2.stacks[k][j]) // Find the end of the stack
                    j++;

                // And append a block to it
                size_t len = strlen(temp_state_2.stacks[k]); 

                char *ret = new char[len + 2];

                strcpy(ret, temp_state_2.stacks[k]);
                ret[len] = letter_to_move;
                ret[len + 1] = '\0';
                temp_state_2.stacks[k] = ret;

                // Then add it to the list of successors
                succ.push_back(new Node(temp_state_2, goal, depth + 1, this));
            }
        }
    }
    return succ;
}

vector<Node *> Node::traceback()
{ // Trace back to root node, adding each node in path to a vector and returning it
    vector<Node *> nodes;
    Node *temp = this;

    while (temp != nullptr)
    {
        nodes.push_back(temp);
        temp = temp->parent;
    }

    return nodes;
}

void Node::print_solution(unsigned iterations, unsigned goal_tests, unsigned max_frontier_size, double time)
{ // Prints solution path
    printf("\nSolution found!\n");
    printf("\nSolution path found: \n\n");
    vector<Node *> nodes = traceback();
    printf("Initial State, h(n) = %0.2f\n", nodes[nodes.size() - 1]->h);
    nodes[nodes.size() - 1]->print();

    for (int i = nodes.size() - 2; i >= 0; i--)
    {
        printf("step %i, h(n) = %0.2f\n", int(nodes.size() - 1 - i), nodes[i]->h);
        nodes[i]->print();
    }

    printf("\nNumber of iterations: %i\n", iterations);
    printf("Path length: %i\n", depth);
    printf("Number of goal tests: %i\n", goal_tests);
    printf("Max frontier size: %i\n", max_frontier_size);

    if (time > 60)
    {
        time /= 60.0;
        if (time > 60)
        {
            time /= 60.0;
            printf("Elapsed time: %.3fh\n", time);
        }
        else
            printf("Elapsed time: %.3fm\n", time);
    }
    else
        printf("Elapsed time: %.3fs\n", time);
}

bool Node::goal_test(Node *goal) const
{ // Checks if current state is equal to the goal state
    return state.matches(goal->state);
}

void Node::print() const
{ // Prints a node
    state.print();
}