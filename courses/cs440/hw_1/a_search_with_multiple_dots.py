#!/usr/bin/env python
"""c
"""
# TODO superfy as many functions as possible.
# TODO create functions to debug. First, just generate state space and
# whatnot, then create fake path and see successors of selected node.
# TODO getting state space really out of whack. Need to rethink how to
# generate.
# TODO Have Node keep track of collected dots
import copy
from basic_pathfinding import State, Node, Search
class DotState(State):
    """c
    """
    def __init__(self, coordinates, state_type, acquired_dots):
        """c
        """
        super(DotState, self).__init__(coordinates, state_type)
        self.acquired_dots = acquired_dots

    def compare(self, other_state):
        """c
        """
        if self.coordinates == other_state.coordinates:
            if self.state_type == other_state.state_type:
                if self.acquired_dots == other_state.acquired_dots:
                    return True
        return False


class DotNode(Node):
    """c
    """
    def __init__(self, state, parent, cost):
        """c
        """
        super(DotNode, self).__init__(state, parent, cost)
        self.coordinates = state.coordinates
        self.state_type = state.state_type
        self.parent = parent
        self.cost = cost
        self.acquired_dots = []
        del self.state
        self.state = None
        self.acquired_dots = set(self.generate_acquired_dots())
        self.state = DotState(
            self.coordinates,
            self.state_type,
            self.acquired_dots)

    def create_successor(self, state):
        """c
        """
        return DotNode(
            state=state,
            parent=self,
            cost=1)

    def generate_acquired_dots(self):
        """c
        """
        acquired = []
        if self.acquired_dots:
            return self.acquired_dots
        elif self.parent is not None:
            acquired +=\
                list(self.parent.generate_acquired_dots())
        if self.state_type == '.': # TODO put in class scope
            acquired.append(self.coordinates)
        return acquired


class DotSearch(Search):
    """c
    """
    def __init__(self, search_file):
        """c
        """
        super(DotSearch, self).__init__(search_file)
        self.dot_coordinates = set([])
        self.dot_coordinate_symbol = self.goal_state_symbol


    def evaluate(self, node):
        """c
        """
        # Look for shortest distance to dot
        # TODO Look for shortest distance to all unvisited dots
        goal = self.dot_coordinates
        smallest_distance_from_dot = None
        node.generate_acquired_dots()
        dots_left = goal.difference(node.acquired_dots)
        for dot_coord in dots_left:
            if smallest_distance_from_dot == None:
                smallest_distance_from_dot =\
                    node.manhattan_distance_from(dot_coord)
                continue
            man_dist = node.manhattan_distance_from(dot_coord)
            if man_dist < smallest_distance_from_dot:
                smallest_distance_from_dot = man_dist
        path_cost = node.generate_path_cost()
        return path_cost + smallest_distance_from_dot


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


    def add_to_state_space(self, array, row, col):
        """c

        """
        state_space = self.state_space
        cell_text = array[row][col]
        if cell_text not in self.wall_symbol:
            current_state = DotState((row, col), cell_text, set([]))
            if cell_text in self.start_state_symbol:
                self.start_state = current_state
            if cell_text in self.dot_coordinate_symbol:
                self.dot_coordinates.update((row, col))
            state_space[(row, col)] = current_state
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
        node_has_all_dots = False
        acquired = current_node.acquired_dots
        goal = self.dot_coordinates
        if goal == acquired:
            node_has_all_dots = True
        return node_has_all_dots


    def already_visited(self, node, visited_states=None):
        """c
        """
        if visited_states == None:
            visited_states = self.visited_states
        for state in visited_states:
            if node.state.compare(state) == True:
                return True
        return False


    def search(self):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search.
        """
        super(DotSearch, self).search('a*')


#EOF
