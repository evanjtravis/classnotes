#!/usr/bin/env python
import sys

class Action(object):
    """c
    """
    def __init__(self, name, coords, label):
        """c
        """
        self.name = name
        self.coords = coords
        self.label = label


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

ACTIONS = {}
for _name in ACTION_COORDS:
    _action = Action(
        _name,
        ACTION_COORDS[_name],
        ACTION_CHARS[_name],
    )
    ACTIONS[_name] = _action



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
        coords):
        """c
        """
        self.char = char
        self.coords = coords
        self.is_terminal, self.reward = self.process_char(char)
        self.utility = (0.0, None)
        self.actions = {
            UP:    BASE_REWARD, # TO BE FLOATS
            DOWN:  BASE_REWARD,
            LEFT:  BASE_REWARD,
            RIGHT: BASE_REWARD
        }

    def get_children_coords(self):
        """c
        """
        children_coords = []
        for action_key in self.actions:
            action_coords = ACTION_COORDS[action_key]
            child_coords = self.add(action_coords)
            if child_coords not in children_coords:
                children_coords.append(child_coords)
        return children_coords


    def process_char(self, char):
        """c
        """
        is_terminal = False
        reward = self.REWARDS[self.DEFAULT]
        if char in self.REWARDS:
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
        if(self.add(action.coords) == state.coords):
            is_parent = True
        return is_parent

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
        is_perpendicular = True
        if state.is_adjacent_to(self):
            a_diff = self.diff(action)
            s_diff = self.diff(state)
            if add_coords(a_diff, s_diff) == (0, 0):
                is_perpendicular = False
        return is_perpendicular


class Agent(object):
    """c
    """
    def __init__(self, mapfile):
        """c
        """
        self.mapfile = mapfile
        self.map_cells, self.start_coords = self.read_map(mapfile)
        START = self.map_cells[0][0].START
        if None in self.start_coords:
            raise Exception(
                "No start character '%s' found in mapfile '%s'."%\
                            (START, self.mapfile))

    def read_map(self, mapfile):
        """c
        """
        f = open(mapfile, 'r')
        array = f.read().splitlines()
        f.close()
        start_coords = (None, None)

        for i in range(len(array)):
            array[i] = list(array[i])
            for j in range(len(array[i])):
                char = array[i][j]
                coords = (i, j)
                array[i][j] = State(char, coords)
        return array, start_coords



    def coord_is_valid(self, coord):
        """c
        """
        valid = False
        if coord >= 0 and coord < len(self.map_cells):
            valid = True
        return valid

    def coords_are_valid(self, coords):
        """c
        """
        x, y = coords
        valid = self.coord_is_valid(x) and self.coord_is_valid(y)
        return valid


    def value_iteration_method(self):
        """c
        """
        states = self.map_cells
        c = ERR_C
        r_max = R_MAX
        e = c * r_max
        y = Y
        delta = MININT
        min_delta = (e * ((1.0 - y) / y))
        iterations = 0
        while (delta >= min_delta) and (iterations < MAX_ITERATIONS):
            delta = 0.0
            iterations += 1
            for i in range(len(states)):
                for j in range(len(states[i])):
                    delta = self.U(i, j, delta)
        return states


    def U(self, i, j, delta=0.0):
        """c
        """
        state = self.map_cells[i][j]
        if state.is_terminal:
            return delta
        reward = R(state)
        old_utility = state.action[0]
        children_coords = state.get_children_coords()
        actions = state.actions
        for action_key in actions:
            q_value = 0.0
            ACTION = ACTIONS[action_key]
            for child_coords in children_coords:
                if not self.coords_are_valid(child_coords):
                    q_value += BASE_REWARD
                else:
                    i, j = child_coords
                    child = self.map_cells[i][j]
                    p_of_child = P(child, state, ACTION)
                    child_utility = child.action[0]
                    q_value += (p_of_child * child_utility)
            q_value = reward + (q_value * Y)
            state.actions[action_key] = q_value
            if q_value > old_utility:
                state.action = (q_value, action_key)
            utility_diff = abs(q_value - old_utility)
            if utility_diff > delta:
                delta = utility_diff
        self.map_cells[i][j] = state
        return delta



def P(state, parent_state, action):
    """Probability of moving from prev_state to state.
    """
    probs = 0.0
    if parent_state.is_parent_of(state, action):
        probs = P_CHILD
    elif parent_state.is_perpendicular_to(state, action):
        probs = P_PERP
    return probs


def R(state):
    """Reward function of an action
    """
    value = state.reward
    return value


def add_coords(coord_1, coord_2):
    """Like add() for State class, but two separate coords.
    """
    i, j = coord_1
    x, y = coord_2
    a = i + x
    b = j + y
    return (a, b)
