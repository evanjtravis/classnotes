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
        self.state_type = state_type


class Node():
    """c
    """
    def __init__(
            self,
            state,
            parent,
            cost):
        """c
        """
        self.state = state
        self.parent = parent
        self.cost = cost
        # Generated attributes
        self.successors = []

    
    def get_total_path_cost(self):
        """c
        """
        if self.parent is not None:
            return self.cost + self.parent.get_total_path_cost()
        else:
            return self.cost


    def generate_successors(self, state_space):
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
            if child in state_space.keys():
                node = Node(
                    state=state_space[child],
                    parent=self,
                    node_cost=1)
                self.successors.append(child)


class Search():
    """c
    """
    def __init__(self, search_file):
        """c
        """
        # Possible Configurable Values
        self.start_state_symbol = 'P'
        self.goal_state_symbol = '.'
        self.wall_symbol = '%'
        self.state_symbol = ' '
        ##############################
        self.frontier = []
        self.visited_states = []
        self.start_state = None
        self.goal_state = None
        self.search_file = search_file
        self.state_space = self.generate_state_space()
        if self.start_state == None:
            raise Exception("Start state '%s' not found." \
                    %(self.start_state_symbol))
        if self.goal_state == None:
            raise Exception("Goal state '%s' not found." \
                    %(self.goal_state_symbol))
        self.start_node = Node(
            state=self.start_state,
            parent=None,
            cost=0)
        self.start_node.generate_successors(self.state_space)



    def generate_state_space(self, search_file=None):
        """c
        """
        if search_file == None:
            search_file = self.search_file
        state_space = {}
        f = open(search_file, 'r')
        array = f.read().splitlines()
        f.close()
        # Break file text into 2D array of characters
        for line in range(len(array)):
            array[line] = list(array[line])
        # Create states from 2D array
        for row in range(len(array)):
            for col in range(len(array[row])):
                current_cell = array[row][col]
                if current_cell not in self.wall_symbol:
                    current_state = State((row, col), current_cell)
                    if current_cell in self.start_state_symbol:
                        self.start_state = current_state
                    if current_cell in self.goal_state_symbol:
                        self.goal_state = current_state
                    state_space[(row, col)] = current_state
        return state_space


    def already_in_frontier(node, frontier=None):
        """c
        """
        if frontier == None:
            frontier = self.frontier
        for index in range(len(frontier)):
            frontier_node = frontier[index]
            if frontier_node.state == node.state:
                if frontier_node.get_total_path_cost() \
                        < node.get_total_path_cost():
                    frontier[index] = node
                    self.frontier = frontier
                return True
        return False


    def already_visited(node, visited_states=None):
        """c
        """
        if visited_states == None:
            visited_states = self.visited_states
        for visited_state in visited_states:
            if node.state == visited_state:
                return True
        return False


    def node_is_valid(self, node):
        """c
        """
        # Check if node's state already exists in frontier.
        # Check if node's state already exists in visited nodes.
        if (not self.already_visited(node)):
            if (not self.already_in_frontier(node)):
                return True
        return False


    def breadth_first_search(self):
        """c
        """
        self.frontier = []
        self.visited_states = []
        current_node = self.start_node
        while current_node.state is not self.goal_state:
            # Expand the frontier specific to BFS.
            # Expand the shallowest unexpanded node.
            # Implemented with frontier as FIFO queue.
            if self.node_is_valid(current_node):
                for child in current_node.successors:
                    if self.node_is_valid(child):
                        self.frontier.append(child)
                self.visited_states.append(current_node.state)
            if self.frontier:
                current_node = self.frontier.pop(0)
                current_node.generate_successors()
            else:
                raise Exception('Solution not found using BFS.')
    
    def depth_first_search(self):
        """c
        """
        pass

    
    def greedy_best_first_search(self):
        """c
        """
        pass

    
    def a_star_search(self):
        """c
        """
        pass















