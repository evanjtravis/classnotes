#!/usr/bin/env python
import copy

# Possibly configurable value
FUN = True


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
            return self.cost + self.parent.generate_path_cost()
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
                self.successors.append(node)


    def generate_path(self):
        """c
        """
        if self.parent is not None:
            return self.parent.generate_path() + [self.state.coordinates]
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
        self.state_space = None


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
        if frontier == []:
            return False
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
        if node.state in visited_states:
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
        # Expand the shallowest unexpanded node.
        # Implemented with frontier as FIFO queue
        current_node = self.frontier.pop(0)
        return current_node

    
    def _depth_first_search(self):
        """c
        """
        # Expand the deepest unexpanded node.
        # Implemented with frontier as LIFO stack. 
        current_node = self.frontier.pop()
        return current_node


    def _greedy_best_first_search(self):
        """c
        """
        # Pick the node on the frontier with the lowest heuristic
        # function result.
        # Heuristic is Manhattan distance from goal
        frontier = self.frontier
        current_node = frontier[0]
        index_to_pop = None
        for index in range(len(frontier)):
            node = frontier[index]
            if (self.manhattan_distance_of(node) < \
                    self.manhattan_distance_of(current_node)):
                current_node = node
                index_to_pop = index
        if index_to_pop is None:
            index_to_pop = 0
        current_node = frontier.pop(index_to_pop)
        return current_node


    def manhattan_distance_of(self, node):
        """c
        """
        x1, y1 = self.goal_state.coordinates
        x2, y2 = node.state.coordinates
        return (abs(x1 - x2) + abs(y1 - y2))
    

    def evaluate(self, node):
        """c
        """
        man_dist = self.manhattan_distance_of(node)
        path_cost = node.generate_path_cost()
        return man_dist + path_cost


    def _a_star_search(self):
        """c
        """
        # Pick the node on the frontier with the lowest evaluation
        # function result.
        # Heuristic is Manhattan distance from goal
        # Evaluation function = heuristic result + path cost
        
        frontier = self.frontier
        current_node = frontier[0]
        index_to_pop = None
        for index in range(len(frontier)):
            node = frontier[index]
            current_node_evaluation = self.evaluate(current_node)
            node_evaluation = self.evaluate(node)
            if (node_evaluation < \
                    current_node_evaluation):
                current_node = node
                index_to_pop = index
        if index_to_pop is None:
            index_to_pop = 0
        current_node = frontier.pop(index_to_pop)
        return current_node
    
        
    def search(self, search_name):
        """c
        """
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
        functions = {
            'bfs': self._breadth_first_search,
            'dfs': self._depth_first_search,
            'gbfs': self._greedy_best_first_search,
            'a*': self._a_star_search
        }
        search_name = search_name.lower()
        # COMMON PARTS OF SEARCH ALGORITHM
        current_node = self.start_node
        while current_node.state is not self.goal_state:
            self.visited_states.append(current_node.state)
            current_node.generate_successors(self.state_space)
            self.count_of_expanded_nodes += 1
            for child in current_node.successors:
                if self.node_is_valid(child):
                    self.frontier.append(child)
            if self.frontier:
                current_node = functions[search_name]()
            else:
                raise Exception(
                    "Solution not found using '%s' search. Empty frontier." \
                            %(search_name))
            if current_node is None:
                break

        solution_node = current_node

        if solution_node is None:
            print "'%s' search is not yet implemented. File = '%s'" \
                    %(search_name, self.search_file)
        else:
            solutions = self.generate_solutions_dict(solution_node)
            self.print_solutions_dict(search_name, solutions)
            # Restart the state of the Search object
            self.frontier = []
            self.visited_states = []
            self.count_of_expanded_nodes = 0


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
        visited = self.visited_states
        # Possibly configurable values
        path_state_symbol = '.'
        traversed_state_symbol = '0'
        ##############################
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        if FUN == True:
            for state in visited:
                x, y = state.coordinates
                array[x][y] = traversed_state_symbol
        for coordinate in path:
            x, y = coordinate
            array[x][y] = path_state_symbol
        for row in range(len(array)):
            for col in range(len(array[row])):
                array_string += array[row][col]
            array_string += '\n'
        return array_string


    def print_solutions_dict(self, search_name, solutions):
        """c
        """
        search_name = search_name.upper()
        print "########## %s SEARCH RESULTS for '%s' ##########" \
                %(search_name, self.search_file)
        for key in solutions.keys():
            print "%25s:\n%s" %(key, solutions[key])














