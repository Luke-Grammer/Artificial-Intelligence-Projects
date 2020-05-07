// Author: Luke Grammer
// Date: 9/15/18

#ifndef NODE_H
#define NODE_H

#include "State.h"

using namespace std;

struct Node
{
    State state;
    Node *parent;
    int depth;
    double f, h;

    Node(const State &s, const State &goal, int depth = 0, Node *par = nullptr);
    Node(const State &s, int depth = 0, Node *par = nullptr); // Default args

    vector<Node *> successors(State goal);
    vector<Node *> traceback();
    void print_solution(unsigned iterations, unsigned goal_tests, unsigned max_frontier_size, double time);
    bool goal_test(Node *goal) const;
    void print() const;
};

#endif