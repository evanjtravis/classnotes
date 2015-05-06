#!/usr/bin/env python
from gridworld import Agent
import sys

def main():
    """c
    """
    mapfile = "data_gridworld/1_map"
    agent = Agent(mapfile)
    agent.value_iteration_method()
    agent.print_mdp_solution()
    if not sys.stdout.isatty():
        agent.print_utility_by_iteration()

#=====================================================================



if __name__ == "__main__":
    main()
