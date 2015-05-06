#!/usr/bin/env python
import sys
import math
from utils import color_text, get_max_keyvalue
class Action(object):
    """c
    """
    def __init__(self, name, coords, label):
        """c
        """
        self.name = name
        self.coords = coords
        self.label = label

A =        60
TRIALS = 5000
R_PLUS =    1.0
Ne =        5
#------------------
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

# Action Configuration Settings
UP =    "UP"
DOWN =  "DOWN"
RIGHT = "RIGHT"
LEFT =  "LEFT"
ACTION_COORDS = {
    # Moving 'up' a 2D array is moving toward the beginning where the
    # beginning is the 0th index of a row.
    UP:    (-1,  0),
    # Moving 'down' a 2D array is moving toward the end where the end
    # is the length of a column.
    DOWN:  ( 1,  0),
    # Moving to the 'right' in a 2D array is moving toward the end
    # where the end is the length of the row
    RIGHT: ( 0,  1),
    # Moving to the 'left' in a 2D array is moving toward the
    # beginning where the beginning is the 0th index of a column.
    LEFT:  ( 0, -1)
}
ACTION_CHARS = {
    None:  '.',
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
        self.previous_utilities = []

        self.utility = (None, None)
        self.actions = {
            UP:    0.0,
            DOWN:  0.0,
            LEFT:  0.0,
            RIGHT: 0.0

        }
        self.Q = {
            None:  R(self),
            UP:    0.0,
            DOWN:  0.0,
            LEFT:  0.0,
            RIGHT: 0.0
        }
        self.N = {
            None:  0,
            UP:    0,
            DOWN:  0,
            LEFT:  0,
            RIGHT: 0
        }

    def __str__(self):
        """c
        """
        print_var = ' '
        if self.is_terminal:
            print_var = self.char + print_var
            if self.char == self.PLUS:
                print_var = color_text(print_var, "green")
            else:
                print_var = color_text(print_var, "red")
        elif self.is_invalid():
            print_var = color_text(self.char + print_var, "yellow")
        else:
            action = self.utility[1]
            print_var = ACTION_CHARS[action] + print_var
        return print_var

    def set_max_utility(self):
        """
        """
        max_utility = None
        max_key = None
        actions = self.actions
        for key in actions:
            if actions[key] > max_utility:
                max_utility = actions[key]
                max_key = key
        new_utility = (max_utility, max_key)
        if self.utility[0] == None:
            self.utility = new_utility
        else:
            self.utility = max(self.utility, new_utility)

    def is_invalid(self):
        """c
        """
        invalid = False
        if self.char == self.WALL:
            invalid = True
        return invalid

    def get_children_coords(self):
        """c
        """
        children_coords = []
        for action_key in self.actions:
            action_coords = ACTION_COORDS[action_key]
            child_coords = self.add(action_coords)
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


    def is_parent_of(self, state, action):
        """Is given state a child based from the action?
        """
        is_parent = False
        new_coords = self.add(action.coords)
        if(new_coords == state.coords):
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
        is_perpendicular = False
        if state.is_adjacent_to(self):
            a_diff = self.diff(action)
            s_diff = self.diff(state)
            if add_coords(a_diff, s_diff) == (0, 0):
                is_perpendicular = True
            elif s_diff == (0,0):
                is_perpendicular = True
        return is_perpendicular


class Agent(object):
    """c
    """
    def __init__(self, mapfile):
        """c
        """
        self.mapfile = mapfile
        self.map_cells, self.start_coords, self.map_sz, START =\
            self.read_map(mapfile)
        if None in self.start_coords:
            raise Exception(
                "No start character '%s' found in mapfile '%s'."%\
                            (START, self.mapfile))
        self.RMSE = None

    def read_map(self, mapfile):
        """c
        """
        f = open(mapfile, 'r')
        array = f.read().splitlines()
        f.close()
        start_coords = (None, None)
        start_char = State.START
        map_sz = 0

        for i in range(len(array)):
            array[i] = list(array[i])
            for j in range(len(array[i])):
                map_sz += 1
                char = array[i][j]
                if char == start_char:
                    if start_coords == (None, None):
                        start_coords = (i, j)
                    else:
                        raise Exception(
                            "More than one starting character '%s'\
found in mapfile '%s'" %(start_char, mapfile)
                        )
                coords = (i, j)
                array[i][j] = State(char, coords)
        return array, start_coords, map_sz, start_char

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
        valid = False
        if coords != None:
            x, y = coords
            if self.coord_is_valid(x) and self.coord_is_valid(y):
                valid = True
                state = self.map_cells[x][y]
                if state.is_invalid():
                    valid = False
        return valid


    def get_max_action_value(self, state):
        """c
        """
        max_action_value = None
        max_action_key = None
        max_action_coords = None

        children_coords = state.get_children_coords()
        Q = state.Q
        for action_key in Q:
            if action_key == None:
                continue
            action_value = Q[action_key]
            if action_value > max_action_value:
                coords = add_coords(
                    state.coords,
                    ACTION_COORDS[action_key]
                )
                if coords in children_coords:
                    if not self.coords_are_valid(coords):
                        max_action_coords = state.coords
                    else:
                        max_action_coords = coords
                    max_action_value = action_value
                    max_action_key = action_key
        return max_action_key, max_action_value, max_action_coords


    def td_q_learning_method(self):
        """c
        """
        x, y = self.start_coords
        start_state = self.map_cells[x][y]
        trial_travel_limit = (self.map_sz * 2) + 1
        RMSE = [None]
        for _ in range(TRIALS):
            delta = 0.0
            # Previous State
            s = start_state
            # Action
            a = None
            # Reward
            r = None
            # Allow for some exploration while avoiding infinite loops
            for t in range(1, trial_travel_limit):
                alph = alpha(t)
                i, j = s.coords
                r = R(s)
                delta += (self.U(i, j) ** 2)
                if not s.is_terminal:
                    max_action_key, max_action_value, max_action_coords =\
                        self.get_max_action_value(s)
                    a = max_action_key
                    s.N[a] += 1
                    current = s.Q[a]
                    s.Q[a] += (
                        alph *\
                        (s.N[a]) *\
                        (r + Y * max_action_value - current)
                    )
                    a = self.argmax_a_F(s)
                    i, j = max_action_coords
                else:
                    u_val = s.utility[0]
                    try:
                        new_util = u_val + r
                    except TypeError:
                        new_util = r
                    s.utility = (new_util, None)
                    a = None
                    i, j = s.coords
                s = self.map_cells[i][j]
            delta *= float(1.0/float(self.map_sz))
            delta = math.sqrt(delta)
            RMSE.append(delta)
        self.RMSE = RMSE


    def argmax_a_F(self, state):
        """c
        """
        value = R_PLUS
        utility_val, utility_key = state.utility
        if utility_key == None or utility_val == None:
            utility_key, utility_val = get_max_keyvalue(state.actions)
        if not state.N[utility_key] < Ne:
            value = state.Q[utility_key]
        state.utility = (utility_val + value, utility_key)
        state.actions[utility_key] = state.utility[0]
        return utility_key


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
                    delta = self.U(i, j, delta)
            for i in range(len(states)):
                for j in range(len(states[i])):
                    state = states[i][j]
                    state.set_max_utility()


    def U(self, i, j, delta=0.0):
        """c
        """
        state = self.map_cells[i][j]
        if state.is_invalid():
            return delta
        reward = R(state)
        old_utility = state.utility[0]
        if old_utility == None:
            old_utility = 0.0
        state.previous_utilities.append(old_utility)
        children_coords = state.get_children_coords()
        actions = state.actions
        for action_key in actions:
            q_value = 0.0
            ACTION = ACTIONS[action_key]
            for child_coords in children_coords:
                if not self.coords_are_valid(child_coords):
                    i, j = state.coords
                else:
                    i, j = child_coords
                child = self.map_cells[i][j]
                if child.is_invalid():
                    child = state
                p_of_child = P(child, state, ACTION)
                child_utility = child.utility[0]
                if child_utility == None:
                    child_utility = 0.0
                q_value += (p_of_child * child_utility)
            q_value = reward + (Y * q_value)
            state.actions[action_key] = q_value
            utility_diff = abs(q_value - old_utility)
            if utility_diff > delta:
                delta = utility_diff
        return delta


    def print_mdp_solution_map(self):
        """c
        """
        msg = ''
        msg_lines = []
        states = self.map_cells
        for i in range(len(states)):
            msg_line = ''
            for j in range(len(states[i])):
                state = states[i][j]
                nxt_str = str(state)
                msg_line += nxt_str
            msg_line += '\n'
            msg_lines.append(msg_line)
        for i in range(len(msg_lines)):
            line = msg_lines[i]
            msg += line
        print msg


    def print_mdp_solution_utility_values(self):
        """c
        """
        states = self.map_cells
        msg = ''
        for i in range(len(states)):
            for j in range(len(states[i])):
                state = states[i][j]
                utility = state.utility[0]
                if utility == None:
                # Space never visited by agent
                    utility = 0.0
                msg += "(%d,%d): %-15.6f, " %\
                    (j, i, utility)
                msg += str(state)
                if state.coords == self.start_coords:
                    msg += state.char
                msg += '\n'
        print msg


    def print_mdp_solution(self):
        """c
        """
        self.print_mdp_solution_utility_values()
        self.print_mdp_solution_map()

    def print_RMSE_csv(self):
        """c
        """
        msg = ''
        RMSE = self.RMSE
        for i in range(1, len(RMSE)):
            msg += "%d,%f\n" %(i, RMSE[i])
        print msg

    def print_utility_by_iteration(self):
        """c
        """
        msg = ''
        states = self.map_cells
        for i in range(len(states)):
            for j in range(len(states[i])):
                state = states[i][j]
                for k in state.previous_utilities:
                    utility = state.previous_utilities[k]
                    msg += "(%d %d), %d, %f\n" %\
                        (i, j, k, utility)
        print msg


#=====================================================================
# Utils
#---------------------------------------------------------------------
def P(state, parent_state, action):
    """Probability of moving from prev_state to state.
    """
    probs = 0.0
    if parent_state.coords != state.coords:
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

def alpha(t):
    """c
    """
    numerator = float(A)
    denominator = float(A - 1)
    return (numerator/(denominator + t))
#=====================================================================
