#!/usr/bin/env python
import copy

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

    
    def generate_path_cost(self):
        """c
        """
        if self.parent is not None:
            return self.cost + self.parent.get_total_path_cost()
        else:
            return self.cost


    def generate_successors(self, state_space):
        """Generate the successor states of the state.
        """
        # Skip generating successors if already generated
        if self.successors:
            return
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
                    cost=1)
                self.successors.append(child)


    def generate_path(self):
        """c
        """
        if self.parent is not None:
            return self.parent.get_generated_path() + [self.state.coordinates]
        else:
            return [self.state.coordinates]


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
        # Data to keep up-to-date for output
        self.maze_array = None
        self.count_of_expanded_nodes = 0
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
        # Keep the array for use in printing out solution later
        self.maze_array = array
        # Create states from 2D array
        for row in range(len(array)):
            for col in range(len(array[row])):
                cell_text = array[row][col]
                if cell_text not in self.wall_symbol:
                    current_state = State((row, col), cell_text)
                    if cell_text in self.start_state_symbol:
                        self.start_state = current_state
                    if cell_text in self.goal_state_symbol:
                        self.goal_state = current_state
                    state_space[(row, col)] = current_state
        return state_space


    def already_in_frontier(self, node, frontier=None):
        """c
        """
        if frontier == None:
            frontier = self.frontier
        for index in range(len(frontier)):
            frontier_node = frontier[index]
            if frontier_node.state == node.state:
                if frontier_node.generate_path_cost() \
                        < node.generate_path_cost():
                    # TODO Should replace, or pop old and append new
                    # (depending on alogrithm?)
                    frontier[index] = node
                return True
        return False


    def already_visited(self, node, visited_states=None):
        """c
        """
        if visited_states == None:
            visited_states = self.visited_states
        for state in visited_states:
            if node.state == state:
                return True
        return False


    def node_is_valid(self, node):
        """c
        """
        # Check if node's state already exists in visited nodes.
        # Check if node's state already exists in frontier.
        if (not self.already_visited(node)):
            if (not self.already_in_frontier(node)):
                return True
        return False


    def _breadth_first_search(self):
        """c
        """
        current_node = self.start_node
        while current_node.state is not self.goal_state:
            # Expand the frontier specific to BFS.
            # Expand the shallowest unexpanded node.
            # Implemented with frontier as FIFO queue.
            current_node.generate_successors()
            for child in current_node.successors:
                if self.node_is_valid(child):
                    self.frontier.append(child)
            self.visited_states.append(current_node.state)
            if self.frontier:
                current_node = self.get_node_from_frontier(0)
            else:
                raise Exception('Solution not found using BFS. Empty frontier.')
        return current_node

    
    def _depth_first_search(self):
        """c
        """
        return None

    
    def get_node_from_frontier(self, index):
        """c
        """
        self.count_of_expanded_nodes += 1
        return self.frontier.pop(index)


    def _greedy_best_first_search(self):
        """c
        """
        return None

    
    def _a_star_search(self):
        """c
        """
        return None

    
    def reset_search(self):
        """c
        """
        self.frontier = []
        self.visited_states = []
        self.start_node = Node(
            state=self.start_state,
            parent=None,
            cost=0)
        self.count_of_expanded_nodes = 0

    def search(self, search_name):
        """c
        """
        functions = {
            'bfs': self._breadth_first_search(),
            'dfs': self._depth_first_search(),
            'gbfs': self._greedy_best_first_search(),
            'a*': self._a_star_search()
        }
        solution_node = functions[search_name.lower()]
        if solution_node is None:
            print "'%s' search is not yet implemented." %(search_name)
        else:
            solutions = self.generate_solutions_dict(solution_node)
            self.print_solutions_dict(solutions)
            self.reset_search()

    def generate_solutions_dict(self, solution_node):
        """c
        """
        solutions = {}
        path = solution_node.generate_path()
        solutions['Maze Solution'] = self.generate_maze_solution(path)
        solutions['Path Cost'] = solution_node.generate_path_cost()
        solutions['Expanded Node Count'] = self.count_of_expanded_nodes
        return solutions

    def generate_maze_solution(self, path):
        """c
        """
        # Possibly configurable values
        traversed_state_symbol = '.'
        ##############################
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        for coordinate in path:
            x, y = coordinate
            array[x][y] = traversed_state_symbol
        for row in range(len(array)):
            for col in range(len(array[row])):
                array_string += array[row][col]
            array_string += '\n'
        return array_string


    def print_solutions_dict(self, solutions):
        """c
        """
        for key in solutions.keys():
            print "%-25s:\t%20s" %(key, solutions[key])














