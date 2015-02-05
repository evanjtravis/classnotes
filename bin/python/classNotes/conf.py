#!/usr/bin/env python

from ConfigParser import ConfigParser
import os

def get_base_dir():
    """Determines the base directory of this project based on
    the absolute path of this program's file and the location of
    the classNotes directory.
    """
    base_dir = '/'
    root = 'classNotes'
    this_path = os.path.abspath(__file__)
    if root in this_path:
        for directory in this_path.split(os.sep):
            base_dir = os.path.join(base_dir, directory)
            if directory == root:
                return base_dir
    else:
        raise Exception(
            "'%s' is not on the absolute path '%s' of this conf file." \
            %(root, this_path))


_BASE = get_base_dir()
CONFIG_FILE = os.path.join(_BASE, 'config/classNotes.config')
_PARSER = ConfigParser()
_PARSER.read(CONFIG_FILE)
_DIRS_SECTION = 'DIRS'
_TMP_BASE = _PARSER.get(_DIRS_SECTION, 'BASE')
if _TMP_BASE != _BASE:
    _PARSER.set('DIRS', 'BASE', _BASE)
    # TODO Eventually log this change

class AttriDict(dict):
    """A dict whose items can also be accessed as member variables.
    When assigning a variable, checks to make sure that a member of
    the dictionary's read-only dir() is not being overwritten. An
    error occurs otherwise.
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
                raise AttributeError(
                    "'%s' is an illegal attribute assignment.\
                    \n\t\tRemove underscore(s)." %(attr))
            else:
                return False


settings = AttriDict() 
_META = 'META'

_IGNORE = _PARSER.get(_META, 'IGNORE')
for section_name in _PARSER.sections():
    if (section_name[:len(_IGNORE)] == _IGNORE) or (section_name == _META):
        continue
    settings[section_name] = dict(_PARSER.items(section_name))

