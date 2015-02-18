#!/usr/bin/env python
"""c
"""
# TODO superfy as many functions as possible.
import copy
from basic_pathfinding import State, Node, Search
from itertools import combinations
class DotState(State):
    """c
    """
    def __init__(self, coordinates, state_type, acquired_dots):
        """c
        """
        super(DotState, self).__init__(coordinates, state_type)
        self.acquired_dots = acquired_dots
        self.is_a_dot = False


class DotNode(Node):
    """c
    """
    def __init__(self, state, parent, cost):
        """c
        """
        super(DotNode, self).__init__(state, parent, cost)
        self.has_dot = self.detect_dot()
        self.collected_dots = self.generate_collected_dots()


    def generate_collected_dots(self):
        """c
        """
        add = []
        if self.has_dot:
            add = self.state.coordinates
            if self.parent is not None:
                return [add] + self.parent.generate_collected_dots()
            else:
                return [add]
        else:
            if self.parent is not None:
                return add + self.parent.generate_collected_dots()
            else:
                return add


    def generate_successors(self, state_space):
        """c
        """
        super(DotNode, self).generate_successors(state_space)
        for i in range(len(self.successors)):
            child = self.successors[i]
            state = child.state
            parent = child.parent
            cost = child.cost
            self.successors[i] = DotNode(state, parent, cost)


    def detect_dot(self):
        """c
        """
        # Configure this in line with search dot_symbol
        dot_symbol = '.'
        if self.state.state_type == dot_symbol:
            return True
        return False


class DotSearch(Search):
    """c
    """
    def __init__(self, search_file):
        """c
        """
        super(DotSearch, self).__init__(search_file)
        self.dot_coordinates = []
        self.collected_dots = []
        self.dot_coordinate_symbol = self.goal_state_symbol


    def evaluate(self, node):
        """c
        """
        # TODO REFACTOR basic_pathfinding for man_dist to take tuple
        # arg
        # Look for shortest distance to dot
        goal = self.dot_coordinates
        distance_of_closest_dot = goal[0]
        for dot_state in goal:
            man_dist = node.manhattan_distance_from(dot_state)
            if (man_dist < distance_of_closest_dot):
                distance_of_closest_dot = man_dist
        path_cost = node.generate_path_cost()
        return path_cost + distance_of_closest_dot


    def generate_maze_solution(self, path):
        """Uses the maze array to build the string printed to stdout.
        """
        #step = 48 # The point at which '0' is ascii encoded
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        #if len(path) > 62: # Number of characters from '0' to 'z'
        #    array_string = '* Path very long. *'
        #    return array_string
        for coordinate in path:
            x, y = coordinate
            #array[x][y] = chr(step)
            array[x][y] = 'x' #TODO ERASE LINE
            #step += 1
        for row in range(len(array)):
            for col in range(len(array[row])):
                array_string += array[row][col]
            array_string += '\n'
        return array_string


    def generate_state_space(self, search_file=None):
        """Iterate through the search_file, recording the States
        along with the start and goal States. The file is broken
        up into a 2D array, thereby determining the coordinates
        of the generated States by using the row and column
        numbers.
            Returns the state_space dictionary.
        """
        super(DotSearch, self).generate_state_space()
        state_space = self.state_space
        # Append to state space coordinates all DotStates with
        # differing combinations of collected dots.
        # 2**n combinations where n = number of dots.
        dot_coordinates = self.dot_coordinates
        dot_coordinate_combinations = []
        for i in range(1, len(dot_coordinates)):
            dot_coordinate_combinations += \
                combinations(dot_coordinates, i)
        for i in range(len(dot_coordinate_combinations)):
            dot_coordinate_combinations[i] = \
                list(dot_coordinate_combinations[i])
        # Add states to state_space that represent
        # all combinations of dot aquisition.
        for _, value in state_space.iteritems():
            base_state = value[0]
            base_coordinates = base_state.coordinates
            base_state_type = base_state.state_type
            for dot_coord_combo in dot_coordinate_combinations:
                value.append(
                    DotState(
                        coordinates=base_coordinates,
                        state_type=base_state_type,
                        acquired_dots=dot_coord_combo
                    )
                )
            # Remove states where dot aquisition is logically true but
            # represented as false within the data
            if base_state_type == self.dot_coordinate_symbol:
                self.remove_nonsensical_states(base_coordinates)


    def remove_nonsensical_states(self, coordinates):
        """c
        """
        keep_list = []
        states = self.state_space[coordinates]
        for i in range(len(states)):
            state = states[i]
            if coordinates in state.acquired_dots:
                keep_list.append(state)
        self.state_space[coordinates] = keep_list



    def add_to_state_space(self, array, row, col):
        """c

        """
        # TODO USE DOT STATES
        state_space = self.state_space
        cell_text = array[row][col]
        if cell_text not in self.wall_symbol:
            current_state = DotState((row, col), cell_text, {})
            if cell_text in self.start_state_symbol:
                self.start_state = current_state
            if cell_text in self.dot_coordinate_symbol:
                self.dot_coordinates.append((row, col))
            if (row, col) in state_space:
                state_space[(row, col)] = [current_state]
            else:
                state_space[(row, col)].append(current_state)


    def node_has_all_dots(self, node):
        """c
        """
        if len(node.generate_collected_dots()) == len(self.dot_coordinates):
            return True
        return False


    def valid_goal_state(self):
        """c
        """
        return True


    def generate_start_node(self):
        """c
        """
        return DotNode(
            state=self.start_state,
            parent=None,
            cost=0)


    def has_reached_goal(self, current_node):
        """c
        """
        return self.node_has_all_dots(current_node)


    def search(self):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search.
        """
        super(DotSearch, self).search('a*')


#EOF
