#!/usr/bin/env python
import sys

R_MAX =        1.0
R_MIN =       -1.0
BASE_REWARD = -0.04
ERR_C =        0.1

# Discount factor
Y =       0.99
P_CHILD = 0.8
# Perpendicular
P_PERP =  0.1

MAX_ITERATIONS = 50
MAXINT = sys.maxint
MININT = -MAXINT - 1

# Action Configuration Settings
UP =    "UP"
DOWN =  "DOWN"
RIGHT = "RIGHT"
LEFT =  "LEFT"
ACTION_COORDS = {
    UP:    (0,  1),
    DOWN:  (0, -1),
    RIGHT: (1,  0),
    LEFT:  (-1, 0)
}
ACTION_CHARS = {
    UP:    '^',
    DOWN:  'v',
    LEFT:  '<',
    RIGHT: '>'
}

ACTIONS = []
for name in ACTION_COORDS:
    action = Action(
        name,
        ACTION_COORDS[name],
        ACTION_CHARS[name],
    )
ACTIONS.append(action)

class Action(object):
    """c
    """
    def __init__(self, name, coords, label):
        """c
        """
        self.name = name
        self.coords = coords
        self.label = label


class State(object):
    """Cell
    """
    # State Configuration Settings
    PLUS =    '+'
    MINUS =   '-'
    WALL =    '%'
    START =   'p'
    DEFAULT = ' '

    REWARDS = {
        PLUS:    R_MAX,
        MINUS:   R_MIN,
        WALL:    BASE_REWARD,
        START:   BASE_REWARD,
        DEFAULT: BASE_REWARD
    }
    TERMINAL = [PLUS, MINUS]
    def __init__(
        self,
        char,
        coords,
        is_terminal):
        """c
        """
        self.char = char
        self.coords = coords
        self.is_terminal, self.reward = self.process_char(char)
        self.utility = 0.0

    def process_char(char):
        """c
        """
        is_terminal = False
        reward = self.REWARDS[self.DEFAULT]
        if char in self.REWARD:
            if char in self.TERMINAL:
                is_terminal = True
            reward = self.REWARDS[char]
        return is_terminal, reward


    def add(self, next_state):
        """add together 2 xy coords, make sure they are non-negative
        coords.
        """
        x1, y1 = self.coords
        if type(next_state) != tuple:
            x2, y2 = next_state.coords
        else:
            x2, y2 = next_state
        x = x1 + x2
        y = y1 + y2
        if (x < 0) or (y < 0):
            Add = None
        else:
            Add = (x, y)
        return Add

    def diff(self, next_state):
        """Get diff of two xy coords
        """
        srcX, srcY = self.coords
        if type(next_state) != tuple:
            destX, destY = next_state.coords
        else:
            destX, destY = next_state
        Diff = (
            srcX - destX,
            srcY - destY
        )
        return Diff


    def is_child_of(self, state, action):
        """Is given state a parent based from previous action?
        """
        return state.has_child(self, action)

    def is_parent_of(self, state, action):
        """Is given state a child based from the action?
        """
        is_parent = False
        if action in self.ACTIONS:
            next_state = self.test(action)
            if next_state == state:
                is_child = True
        return is_child

    def is_adjacent_to(self, state):
        """Are this state and the given state adjacent?
        """
        adjacent = False
        i, j = self.coords
        x, y = self.diff(state)
        if ((i == x) and (abs(y) == 1)) or\
                ((j == y) and (abs(x) == 1)):
            adjacent = True
        return adjacent

    def is_perpendicular_to(self, state, action):
        """c
        """
        is_perpendicular = False
        if state.is_adjacent_to(self):
            # diff --> guaranteed to be in HORIZ or VERT and therefore
            # not None
            next_state = self.test(action)
            diff = self.diff(state)
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
        self.map_cells, self.start_coords = self.read_map(mapfile)
        if None in self.start_coords:
            raise Exception(
                "No start character '%s' found in mapfile '%s'."%\
                            (self.START, self.mapfile))

    def read_map(self, mapfile):
        """c
        """
        f = open(mapfile, 'r')
        array = f.read().splitlines()
        f.close()
        VALUES = self.VALUES
        TERMINAL = self.TERMINAL
        start_coords = (None, None)

        for i in range(len(array)):
            array[i] = list(array[i])
            for j in range(len(array[i])):
                char = array[i][j]
                coords = (i, j)
                if char in VALUES:
                    is_terminal = False
                    if char in TERMINAL:
                        is_terminal = True
                    array[i][j] = State(
                        char,
                        VALUES[char],
                        coords,
                        is_terminal
                    )
                    if char == self.START:
                        start_coords = (i, j)
                else:
                    array[i][j] = State(
                        char,
                        VALUES[self.DEFAULT],
                        coords,
                        is_terminal
                    )
        return array, start_coords

    def value_iteration_method(self):
        """c
        """
        states = self.map_cells
        c = ERR_C
        r_max = R_MAX
        e = c * r_max
        y = Y
        delta = MAXINT
        min_delta = (e * ((1.0 - y) / y))
        iterations = 0
        while (delta >= min_delta) and (iterations < MAX_ITERATIONS):
            delta = 0.0
            iterations += 1
            for i in range(len(states)):
                for j in range(len(states[i])):
                    old_util = state.utility
                    state = states[i][j]
                    state.utility = U(state)
                    u_diff =


def iterate_values(state):
    """c
    """
    children = state.get_children()
    R_state = R(state)
    if state.is_terminal:
        return R_state
    else:
        actions = state.get_valid_actions()
        for action in actions:
            for child in children:
                # Test each action on each child
                # Return max result == action, child pair



def U(states, actions):
    """The utility of a sequence of states.
    """
    total = 0.0
    for i in range(len(args)):
        state = args[i]
        R_of_state = R(state) * (Y ** i)
        total += R_of_state
    return total



def expU(states, actions):
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


def P(state, prev_state, action):
    """Probability of moving from prev_state to state.
    """
    probs = 1.0
    # If start state, just return 1
    if prev_state != None:
        if prev_state.is_parent_of(state, action):
            probs = P_CHILD
        elif prev_state.is_perpendicular_to(state, action):
            probs = P_PERP
        else:
            probs = 0.0
    return probs


def R(state):
    """Reward function of an action
    """
    value = state.utility
    return value
