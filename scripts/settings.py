#!/usr/bin/env python

from ConfigParser import ConfigParser

CONFIG_FILE = '../config/classNotes.config'
_PARSER = ConfigParser()
_PARSER.read(CONFIG_FILE)
_SECTION = ''

PROJECT = dict(_PARSER.items('PROJECT'))
DIRS = dict(_PARSER.items('DIRS'))
FILETYPES = dict(_PARSER.items('FILETYPES'))
WRITING_CONVENTIONS = dict(_PARSER.items('WRITING_CONVENTIONS'))

