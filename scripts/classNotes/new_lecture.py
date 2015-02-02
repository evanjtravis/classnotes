#!/bin/env/python

import settings
from ConfigParser import ConfigParser
import os

parser = ConfigParser()
parser.read('config/classNotes.config')


# look for files with lec.## naming convention in pwd
# find file w/ largest suffix number
# copy over template

def main():
    pass


if __name__ == '__main__':
    main()
