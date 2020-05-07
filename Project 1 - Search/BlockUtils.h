// Author: Luke Grammer
// Date: 9/15/18

#ifndef BLOCK_UTILS_H
#define BLOCK_UTILS_H

#include <iostream>
#include <stdexcept>
#include <queue>
#include <list>
#include <algorithm>
#include <chrono> 

#include "Node.h"

using namespace std;

const int MAX_ITERATIONS = 10000;

struct Comparison
{
    bool operator()(Node *lhs, Node *rhs) const
    {
        return (lhs->f > rhs->f); // because I want top() to be the node with the smallest score
    }
};

struct Search
{
    static bool GraphSearch(Node *node, Node *goal)
    {
        priority_queue<Node *, vector<Node *>, Comparison> frontier;
        list<State> visited;
        vector<Node*> successors;
        unsigned iteration = 1, goal_tests = 1, max_frontier_size = 1;
        bool explored = false;
        chrono::time_point<chrono::system_clock> start_time = chrono::system_clock::now();
        double curr_time = 0;

        // Check if node contains the goal state before looping
        if (node->goal_test(goal))
        {
            printf("Root node is already in the goal state!\n");
            return true;
        }

        frontier.push(node);

        while (iteration <= MAX_ITERATIONS)
        {
            curr_time = chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now() - start_time).count() / 1000.0;

            // If frontier is empty, the goal state is not reachable
            if (frontier.empty())
                return false;

            // Otherwise, take the node out with the smallest f value and mark it as visited
            node = frontier.top();
            frontier.pop();
            visited.push_back(node->state);

            printf("Iteration = %i, depth = %i, f(n) = %0.2f, frontier = %i\n", iteration, node->depth, node->f, int(frontier.size()));
            node->print();

            // Find all successor states
            successors = node->successors(goal->state);

            // For each successor node, check if we've already encountered it, check for goal state, then push the node into the priority queue
            for (unsigned i = 0; i < successors.size(); i++)
            {
                explored = false;

                // Check if child state has been explored
                auto it = find(visited.begin(), visited.end(), successors[i]->state);
                    // If we've seen the state before, don't add it to the frontier
                    if (it != visited.end())
                        explored = true;

                // If we haven't, check if it's in the goal state and add it to the frontier
                if (!explored)
                {
                    // If node contains the goal state
                    goal_tests++;
                    if (successors[i]->goal_test(goal))
                    {
                        successors[i]->print_solution(iteration + 1, goal_tests, max_frontier_size, curr_time);
                        return true;
                    }

                    frontier.push(successors[i]);
                    if (frontier.size() > max_frontier_size)
                        max_frontier_size = frontier.size();
                }
            }

            // Empty successors
            successors.clear();
            iteration++;
        }

        if (curr_time > 60)
        {
            curr_time /= 60.0;
            if (curr_time > 60)
            {
                curr_time /= 60.0;
                printf("Search terminated after %.3fh\n", curr_time);
            }
            else
                printf("Search terminated after %.3fm\n", curr_time);
        }
        else
            printf("Search terminated after %.3fs\n", curr_time);

        printf("No solution found\n");
        visited.clear();
        return false;
    }
};

struct FileManager
{
    static pair<State, State> read_problem(const string filename)
    {

        int nstacks = -1, nblocks = -1;
        char *buf = new char[128];
        FILE *fil = nullptr;

        printf("\nInput file: %s\n", filename.c_str());
        fil = fopen(filename.c_str(), "r");
        if (!fil)
            throw runtime_error("ERROR: " + filename + " not found!\n");

        fgets(buf, 128, fil);
        sscanf(buf, "%d %d", &nstacks, &nblocks);
        printf("%d stacks, %d blocks\n", nstacks, nblocks);

        vector<char *> stacks = vector<char *>();

        for (int i = 0; i < nstacks; i++)
        {
            fgets(buf, 128, fil);
            buf[strlen(buf) - 1] = '\0'; // truncate EOL
            stacks.push_back(strdup(buf));
        }

        State init = State(stacks);
        printf("Initial state: \n");
        init.print();
        printf("#####\n");

        stacks = vector<char *>();
        for (int i = 0; i < nstacks; i++)
        {
            fgets(buf, 128, fil);
            buf[strlen(buf) - 1] = '\0'; // truncate EOL
            stacks.push_back(strdup(buf));
        }

        State goal = State(stacks);
        printf("Goal state: \n");
        goal.print();
        printf("#####\n");

        fclose(fil);
        pair<State, State> init_goal = make_pair(init, goal);
        return init_goal;
    }
};

#endif
