#!/usr/bin/env python

PLUS =    '+'
MINUS =   '-'
WALL =    '%'
START =   'p'
DEFAULT = "DEFAULT"


VALUES = {
    PLUS:       1,
    MINUS:     -1,
    WALL:       0,
    START:      0,
    DEFAULT:    0
}

BASE_REWARD =    -0.04
# Discount factor
Y =       0.99
P_CHILD = 0.8
# Perpendicular
P_PERP =  0.1


class State(object):
    """Cell
    """
    UP =    (0,  1)
    DOWN =  (0, -1)
    RIGHT = (UP[1], UP[0])
    LEFT =  (DOWN[1], DOWN[0])
    ACTIONS = {
        UP:    '^',
        DOWN:  'v',
        LEFT:  '<',
        RIGHT: '>'
    }
    VERT = [UP, DOWN]
    HORIZ = [LEFT, RIGHT]
    def __init__(self, char, value, coords):
        """c
        """
        self.char = char
        self.value = value
        self.coords = coords
        # Action = diff(s.coords, s`.coords), indicating direction
        self.action = None

    def diff(self, next_state):
        """c
        """
        srcX, srcY = self.coords
        destX, destY = next_state.coords
        Diff = (
            srcX - destX,
            srcY - destY
        )
        return Diff

    def set_action(self, next_state):
        """c
        """
        action = self.diff(next_state)
        self.action = action

    def is_child_of(self, prev_state):
        """Is given state a parent based from previous action?
        """
        return prev_state.has_child(self)

    def is_parent_of(self, next_state):
        """Is given state a child based from the action?
        """
        child_is = False
        action = self.diff(next_state)
        if self.action == action:
            child_is = True
        return child_is

    def is_adjacent_to(self, state):
        """Are this state and the given state adjacent?
        """
        adjacent = False
        diff = self.diff(state)
        if diff in self.ACTIONS:
            adjacent = True
        return adjacent

    def is_perpendicular_to(self, prev_state):
        """c
        """
        is_perpendicular = False
        if prev_state.is_adjacent_to(self):
            VERT = self.VERT
            HORIZ = self.HORIZ
            action = self.action
            # diff --> guaranteed to be in HORIZ or VERT and therefore
            # not None
            diff = self.diff(prev_state)
            if diff in VERT:
                if action in HORIZ:
                    is_perpendicular = True
            elif action in VERT:
                is_perpendicular = True
        return is_perpendicular



class Agent(object):
    """c
    """
    def __init__(self, mapfile):
        """c
        """
        self.mapfile = mapfile
        self.cells = self.read_map(mapfile)

    def read_map(self, mapfile):
        """c
        """
        f = open(mapfile, 'r')
        array = f.read().splitlines()
        f.close()

        for i in range(len(array)):
            array[i] = list(array[i])
            for j in range(len(array[i])):
                char = array[i][j]
                coords = (i, j)
                if char in VALUES:
                    array[i][j] = State(char, VALUES[char], coords)
                else:
                    array[i][j] = State(char, VALUES[DEFAULT], coords)
        return array

def U(*args):
    """The utility of a sequence of states.
    """
    total = 0.0
    for i in range(len(args)):
        state = args[i]
        R_of_state = R(state) * (Y ** i)
        total += R_of_state
    return total



def expU(*args):
    """Expected Utility of a sequence of states.
    """
    total = 0.0
    prev_state = None
    for i in range(len(args)):
        if i > 0:
            prev_state = args[i -1]
        state = args[i]
        P_of_state = P(prev_state, state)
        R_of_state = R(state) * (Y ** i)
        total += P_of_state * R_of_state
    return total


def P(prev_state, state):
    """Probability of moving from prev_state to state.
    """
    probs = 1.0
    # If start state, just return 1
    if prev_state != None:
        if prev_state.is_parent_of(state):
            probs = P_CHILD
        elif prev_state.is_perpendicular_to(state):
            probs = P_PERP
        else:
            probs = 0.0
    return probs


def R(state):
    """Reward function of a state
    """
    value = state.value
    return value + BASE_REWARD
