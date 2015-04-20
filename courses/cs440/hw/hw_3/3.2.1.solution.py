#!/usr/bin/env python
import os
from bag_o_words import Agent

DATADIR = "spam_detection"
TRAINF = os.path.join(DATADIR, "train_email.txt")
TESTF = os.path.join(DATADIR, "test_email.txt")
def main():
    """c
    """
    agent = Agent(TRAINF, TESTF, "spam")
    agent.whole_shebang()


if __name__ == "__main__":
    main()
