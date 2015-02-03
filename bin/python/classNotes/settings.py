#!/usr/bin/env python

from ConfigParser import ConfigParser
import os

class BaseDirectoryNoMatchError(Exception):
    pass


_BASE = '/home/ejtravis/classNotes'
CONFIG_FILE = os.path.join(_BASE, 'config/classNotes.config')
_PARSER = ConfigParser()
_PARSER.read(CONFIG_FILE)
_SECTION = ''

PROJECT = dict(_PARSER.items('PROJECT'))
DIRS = dict(_PARSER.items('DIRS'))
FILETYPES = dict(_PARSER.items('FILETYPES'))
WRITING_CONVENTIONS = dict(_PARSER.items('WRITING_CONVENTIONS'))

_base_kw = 'base'
if _BASE != DIRS[_base_kw]:
    raise Exception("Base directory in program :%s: does not match Base directory in config :%s:." %(_BASE, DIRS[_base_kw]))
