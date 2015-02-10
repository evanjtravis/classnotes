#!/usr/bin/env python
class State():
    """Represents a state for a given state space.
    """
    def __init__(self, coordinates, Search):
        """
        coordinates = (x,y) coordinates within file/graph
        """
        self.coordinates = coordinates
        self.successors = []
        Search.state_space[coordinates] = self

    def set_successors(self):
        """Generate the successor states of the state.
        """
        x,y = self.coordinates
        children = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for child in children:
            if child in self.Search.state_space.keys():
                self.successors.append(child)

class Node():
    """
    """
    def __init__(self, state, parent, path=None):
        if path == None:
            self.path = get_path_from_anscestors()
        else:
            self.path = path
        self.total_path_cost = get_path_cost_of_path()
        self.base_path_cost = get_base_path_cost()

    def get_path_from_anscestors(self):
        pass
    def get_path_cost_from_path():
        pass


class Search():
    """
    """
    def __init__(self):
        self.frontier = []
        self.visited_nodes = []
        self.start_state = None
        self.goal_state = None
        self.path_cost = 0
        self.state_space = {}

