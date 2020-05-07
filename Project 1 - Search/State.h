#ifndef STATE_H
#define STATE_H

#include <stdio.h>
#include <string.h>
#include <cmath>
#include <vector>

using namespace std;

struct State
{
    vector<char *> stacks;

    State();
    State(vector<char *> input);
    State(const State &s);

    ~State();

    double heuristic(const State &goal) const;
    bool matches(const State &other) const;
    void print() const;

    State &operator=(const State &s);
    bool operator==(const State &s);
};

#endif