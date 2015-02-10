#!/usr/bin/env python
class State():
    """Represents a state within a given state space.
    """
    def __init__(self, coordinates, state_type):
        """
        coordinates = (x,y) coordinates within file/graph
        state_type = character within 2D array
        """
        self.coordinates = coordinates
        self.state_type =


class Node():
    """c
    """
    def __init__(
            self,
            search,
            state,
            parent_node,
            path,
            path_cost):
        """c
        """
        self.search = search
        self.state = state
        self.parent_node = parent_node
        self.path = path
        self.total_path_cost = self.get_total_path_cost()
        self.successors = []

    
    def get_total_path_cost(self):
        """c
        """
        pass


    def expand_frontier(self):
        """c
        """
        pass


    def set_successors(self):
        """Generate the successor states of the state.
        """
        x, y = self.state.coordinates
        children = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for child in children:
            if child in self.search.state_space.keys():
                self.successors.append(child)


class Search():
    """c
    """
    def __init__(self, search_file):
        """c
        """
        self.frontier = []
        self.visited_nodes = []
        self.start_state = None
        self.goal_state = None
        self.solution_path_cost = 0
        self.uniform_cost = True
        self.search_file = search_file
        self.state_space = self.initialize_state_space(search_file)
        # Possible Configurable Values
        self.start_state_symbol = 'P'
        self.goal_state_symbol = '.'
        self.wall_symbol = '%'
        self.state_symbol = ' '


    def initialize_state_space(self, search_file=None):
        """c
        """
        if search_file == None:
            search_file = self.search_file
        state_space = {}
        f = open(search_file, 'r')
        array = f.read().splitlines()
        f.close()
        # Break file into 2D array of characters
        for line in range(len(array)):
            array[line] = list(array[line])
        # Create states from 2D array
        for row in range(len(array)):
            for col in range(len(array[row])):
                current_cell = array[row][col]
                if current_cell not in self.wall_symbol:
                    current_state = State((row, col), current_cell)

















