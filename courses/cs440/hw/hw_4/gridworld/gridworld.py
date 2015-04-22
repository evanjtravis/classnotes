#!/usr/bin/env python

BASE_REWARD =    -0.04
# Discount factor
Y =       0.99
P_CHILD = 0.8
# Perpendicular
P_PERP =  0.1

class Action(object):
    """c
    """
    def __init__(self, name, coords, label, utility):
        """c
        """
        self.name = name
        self.coords = coords
        self.label = label
        self.utility = utility


class State(object):
    """Cell
    """
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
    ACTION_UTILITIES = {
        UP:     BASE_REWARD,
        DOWN:   BASE_REWARD,
        LEFT:   BASE_REWARD,
        RIGHT:  BASE_REWARD,
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
            ACTION_UTILITIES[name]
        )
        ACTIONS.append(action)
    VERT = [ACTION_COORDS[UP], ACTION_COORDS[DOWN]]
    HORIZ = [ACTION_COORDS[LEFT], ACTION_COORDS[RIGHT]]
    def __init__(
        self,
        char,
        utility,
        coords,
        terminal):
        """c
        """
        self.char = char
        self.utility = utility
        self.coords = coords
        self.terminal = terminal
        self.action = None
        self.utility = None

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
    PLUS =    '+'
    MINUS =   '-'
    WALL =    '%'
    START =   'p'
    DEFAULT = "DEFAULT"

    VALUES = {
        PLUS:       1.0,
        MINUS:     -1.0,
        WALL:       0.0,
        START:      1.0,
        DEFAULT:    0.0
    }
    TERMINAL = [PLUS, MINUS]
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
                    terminal = False
                    if char in TERMINAL:
                        terminal = True
                    array[i][j] = State(
                        char,
                        VALUES[char],
                        coords,
                        terminal
                    )
                    if char == self.START:
                        start_coords = (i, j)
                else:
                    array[i][j] = State(char, VALUES[self.DEFAULT], coords)
        return array, start_coords

    def value_iteration_method(self):
        """c
        """
        start_state = self.map_cells[i][j]
        actions = state.ACTIONS
        iterate_values(start_state, actions)


def iterate_values(state, actions):
    """c
    """
    children = []
    max_value = None
    for action in actions:
        next_state = action.execute(state)
        max_value =




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
    value = state.utility
    if state.terminal:
        return value
    return value + BASE_REWARD
