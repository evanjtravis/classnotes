#!/usr/bin/env python
"""c
"""
from basic_pathfinding import State, Node, Search

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


    def detect_dot(self, search):
        """c
        """
        dot_symbol = search.dot_symbol
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
        self.dot_states = []
        self.collected_dots = []
        self.dot_state_symbol = self.goal_state_symbol


    def evaluate(self, node):
        """c
        """
        # Look for shortest distance to dot
        goal = self.dot_states
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
        step = 48 # The point at which '0' is ascii encoded
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        if len(path) > 36: # Number of characters from '0' to 'z'
            return array_string
        for coordinate in path:
            x, y = coordinate
            array[x][y] = chr(step)
            step += 1
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
        if (search_file == None) and (self.search_file != None):
            search_file = self.search_file
        else:
            raise Exception("Invalid search file '%s'" %(search_file))
        # Saves execution time if search file has not been changed
        if (search_file == self._old_search_file):
            return self.state_space
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
                    if cell_text in self.dot_state_symbol:
                        self.dot_states.append(current_state)
                    state_space[(row, col)] = current_state
        return state_space


    def node_has_all_dots(self, node):
        """c
        """
        if len(node.generate_collected_dots) == len(self.dot_states):
            return True
        return False


    def search(self):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search. 
        """
        self.state_space = self.generate_state_space()
        
        if self.start_state == None:
            raise Exception("Start state '%s' not found." \
                    %(self.start_state_symbol))
        if self.goal_state == None:
            raise Exception("Goal state '%s' not found." \
                    %(self.goal_state_symbol))
        
        self.start_node = DotNode(
            state=self.start_state,
            parent=None,
            cost=0)
        current_node = self.start_node
        while not self.node_has_all_dots(current_node):
            self.visited_states.append(current_node.state)
            current_node.generate_successors(self.state_space)
            self.count_of_expanded_nodes += 1
            for child in current_node.successors:
                if self.node_is_valid(child):
                    self.frontier.append(child)
            if self.frontier:
                current_node = self._a_star_search()
            else:
                raise Exception(
                    "Solution not found using 'a*' search. Empty frontier.")
            if current_node is None:
                break

        solution_node = current_node

        if solution_node is None:
            print "'a*' search is not yet implemented. File = '%s'" \
                    %(self.search_file)
        else:
            solutions = self.generate_solutions_dict(solution_node)
            self.print_solutions_dict(search_name, solutions)
            # Restart the state of the Search object
            self.frontier = []
            self.visited_states = []
            self.count_of_expanded_nodes = 0


    
