#!/usr/bin/env python

import sys

def color(fg="white", bg="black"):
    """c
    """
    esc = '\033['
    color_labels = [
        'black',
        'red',
        'yellow',
        'green',
        'blue',
        'cyan',
        'magenta',
        'white'
    ]
    bg_colors = {
        'black': '40;',
        'red': '41;',
        'yellow': '43;',
        'green': '42;',
        'blue': '44;',
        'cyan': '46;',
        'magenta': '45;',
        'white': '47;'
    }
    fg_colors = {
        'black': '30m',
        'red': '31m',
        'yellow': '33m',
        'green': '32m',
        'blue': '34m',
        'cyan': '36m',
        'magenta': '35m',
        'white': '37m'
    }
    if type(fg) == int:
        if fg < 0:
            fg = 0
        elif fg > len(color_labels) - 1:
            fg = len(color_labels) - 1
        fg = color_labels[fg]
    if type(bg) == int:
        if bg < 0:
            bg = 0
        elif bg > len(color_labels) - 1:
            bg = len(color_labels) - 1
    colors = esc + bg_colors[bg] + fg_colors[fg]
    return colors


def color_text(text, fg_key="white", bg_key="black"):
    """c
    """
    if sys.stdout.isatty():
        # Windows doesn't support ansi escape characters
        if sys.platform != 'win32':
            text = color(fg_key, bg_key) + text
            # revert back to white, makes string larger, but easier to
            # manage.
            text += color()
    return text
