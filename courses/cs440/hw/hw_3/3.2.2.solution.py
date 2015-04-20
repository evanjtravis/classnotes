#!/usr/bin/env python

from eight_newsgroups import Agent
import os

DATADIR = "8category"

TRAINF = os.path.join(DATADIR, "8category.training.txt")
TESTF = os.path.join(DATADIR, "8category.testing.txt")




def main():
    """c
    """
    agent = Agent(TRAINF, TESTF)
    agent.whole_shebang()




if __name__ == "__main__":
    main()
