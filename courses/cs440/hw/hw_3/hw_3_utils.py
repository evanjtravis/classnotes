#!/usr/bin/env python

import math
import sys

#=====================================================================
# Utils
#---------------------------------------------------------------------
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

def color_text(text, fg_key, bg_key):
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

def get_color_index(log_odd, min_odd, max_odd):
    """c
    """
    num_of_colors = 7
    the_range = max_odd - min_odd
    chunk = the_range / num_of_colors
    index = -1
    found = False
    if log_odd == min_odd:
        return 0
    elif log_odd == max_odd:
        return num_of_colors
    while (not found) and (index < num_of_colors):
        index += 1
        found = log_odd >= (max_odd - (chunk * index))
    return index

def ratio(numerator, denominator, smoothing=0.0, v=1.0):
    """c
    """
    smoothing = float(smoothing)
    v = float(v)
    numerator = (float(numerator) + smoothing)
    denominator = (float(denominator) + (smoothing * v))
    if denominator == 0.0:
        return 0.0
    return numerator / denominator


def log(num):
    """c
    """
    if num == 0:
        return -25
    else:
        return math.log(num)

