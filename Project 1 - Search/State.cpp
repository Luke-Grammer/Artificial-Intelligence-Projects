// Author: Luke Grammer
// Date: 9/15/18

#include "State.h"

State::State() : stacks{vector<char *>()} {} // Default constructor

State::State(vector<char *> input)
{ // Constructor deep copies input stacks
    for (unsigned i = 0; i < input.size(); i++)
    {
        stacks.push_back(strdup(input[i]));
    }
}

State::State(const State &s)
{ // Constructor deep copies input state's stacks
    for (unsigned i = 0; i < s.stacks.size(); i++)
    {
        stacks.push_back(strdup(s.stacks[i]));
    }
}

State::~State()
{ // Destructor deallocates stack blocks
    stacks.clear();
}

double State::heuristic(const State &goal) const
{ // Heuristic function for GraphSearch (applied to nodes during construction)
    double h1 = 0, h2 = 0, h3 = 0;
    int *max_goal_index = new int[stacks.size()];
    int *max_curr_index = new int[stacks.size()];

    // Goal state and current state must have same dimensions
    if (goal.stacks.size() != stacks.size())
        return 0;

    for (unsigned curr_stack = 0; curr_stack < stacks.size(); curr_stack++) // Loop through all stacks
    {
        max_goal_index[curr_stack] = strlen(goal.stacks[curr_stack]);
        max_curr_index[curr_stack] = strlen(stacks[curr_stack]);
        // Find stack heights for each stack for both the goal and current state

        // Accounting for number and depth of all out of place blocks
        for (int i = 0; stacks[curr_stack][i]; i++)
        { // Starting at the bottom of current stack, moving up
            if (i < max_goal_index[curr_stack])
            { // If the current and goal state both have blocks
                if (stacks[curr_stack][i] != goal.stacks[curr_stack][i])
                { // If those blocks aren't the same, update heuristic
                    int max_index = (max_curr_index[curr_stack] > max_goal_index[curr_stack]) ? 
                                    max_curr_index[curr_stack] : max_goal_index[curr_stack];
                    h1 += 2 * (max_index - i);
                    break;
                }
            }
            else // If the current stack is higher than the goal stack, update heuristic
                h1 += 4;
        }

        for(int i = 0; stacks[curr_stack][i]; i++) 
        { // Loop through the current stacks blocks
            for(int j = 0; goal.stacks[curr_stack][j]; j++) 
            { // Loop through goal blocks on current stack
                if(stacks[curr_stack][i] == goal.stacks[curr_stack][j])
                { // If the blocks are the same
                    if (i == j) 
                    { // If the blocks are on the same level
                        for (int k = j + 1; stacks[curr_stack][k] && goal.stacks[curr_stack][k]; k++)
                        { // Starting at the current point, going to the top
                            if (stacks[curr_stack][k] != goal.stacks[curr_stack][k])
                            { // If the blocks are different, number of moves to solve will be proportional to the difference in heights
                                h3 += (abs(max_goal_index[curr_stack] - max_curr_index[curr_stack]) + 2);
                            }
                        }

                        for (int k = j - 1; k >= 0; k--)
                        { // Run down the stack from the current position
                            if (stacks[curr_stack][k] != goal.stacks[curr_stack][k])
                            { // If the blocks are different, add number of moves to remove different block 
                                h2 += (2 * (abs(j - k)) + 2);
                                break;
                            }
                        }      
                    }
                    else
                    { // The block is in the same stack, but on the wrong level, add number of moves to move it to the correct level
                        h2 += abs(i - j) + 2;
                        break;
                    }
                }
            }
        }
    }

    delete[] max_goal_index;
    delete[] max_curr_index;
    return (h1 + h2 + h3);
}

bool State::matches(const State &other) const
{ // Returns if a state matches another given state
    for (unsigned i = 0; i < stacks.size(); i++)
    {
        for (unsigned j = 0; stacks[i][j]; j++)
        {
            if (stacks[i][j] != other.stacks[i][j])
                return false;
        }
    }
    return true;
}

void State::print() const
{ // Prints a state
    for (unsigned i = 0; i < stacks.size(); i++)
    {
        for (int j = 0; stacks[i][j]; j++)
        {
            printf("%c ", stacks[i][j]);
        }
        printf("\n");
    }
}

State &State::operator=(const State &s)
{ // Overloaded assignment operator deep copies a state
    stacks.clear();
    for (unsigned i = 0; i < s.stacks.size(); i++)
    {
        stacks.push_back(strdup(s.stacks[i]));
    }
    return *this;
}

bool State::operator==(const State &s) 
{ // Overloaded equality for state
    return this->matches(s);
}
