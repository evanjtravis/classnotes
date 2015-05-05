#!/usr/bin/env python

import sys
from gridworld import Agent



def main():
    """c
    """
    mapfile = "data_gridworld/1_map"
    agent = Agent(mapfile)
    agent.td_q_learning_method()
    agent.print_mdp_solution()
    if not sys.stdout.isatty():
        agent.print_RMSE_csv()


if __name__ == "__main__":
    main()
