#!/usr/bin/env python

from ConfigParser import ConfigParser
import os


_BASE = '/home/ejtravis/classNotes'
CONFIG_FILE = os.path.join(_BASE, 'config/classNotes.config')
_PARSER = ConfigParser()
_PARSER.read(CONFIG_FILE)

class AttriDict(dict):
    """A dict whose items can also be accessed as member variables.
    When assigning a variable, checks to make sure that a member of
    the dictionary's dir() is not being overwritten. An error is
    thrown when this occurs.
    """
    _INITIALIZE = True
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        self._INITIALIZE = False

    def __setitem__(self, index, value):
        if not self._is_invalid(index):
            super(AttriDict, self).__setitem__(index, value)

    def __setattr__(self, attr, value):
        if not self._is_invalid(attr):
            super(AttriDict, self).__setattr__(attr, value)

    def _is_invalid(self, attr):
        """Checks to see if attribute is invalid, either by already
        existing in the dictionary readonly attributes, or by containing
        leading underscores.
        """
        if self._INITIALIZE == False:
            dict_dir = dir(dict())
            if attr in dict_dir:
                raise AttributeError(
                    "'AttriDict' object attribute '%s' is read-only" \
                    %(attr))
            elif '_' == attr[0]:
                raise Exception("'%s' is an illegal assignment." %(attr))
            else:
                return False

settings = AttriDict() 
META = 'META'

IGNORE = _PARSER.get(META, 'IGNORE')
for section_name in _PARSER.sections():
    if (section_name[:len(IGNORE)] == IGNORE) or (section_name == META):
        continue
    settings[section_name] = dict(_PARSER.items(section_name))

