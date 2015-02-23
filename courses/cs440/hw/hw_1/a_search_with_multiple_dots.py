#!/usr/bin/env python
"""c
"""
# TODO superfy as many functions as possible.
# TODO create functions to debug. First, just generate state space and
# whatnot, then create fake path and see successors of selected node.
# TODO getting state space really out of whack. Need to rethink how to
# generate.
import copy
from basic_pathfinding import State, Node, Agent


class DotState(State):
    """c
    """
    def __init__(self, coordinates=None, state_type=None, state=None):
        """c
        """
        if isinstance(state, State):
            coordinates = state.coordinates
            state_type = state.state_type
        if coordinates is None:
            print "Poor state creation. Coordinates are 'None'."
            raise Exception()
        super(DotState, self).__init__(coordinates, state_type)
        self.acquired_dots = None


    def compare(self, other):
        """c
        """
        same = False
        if super(DotState, self).compare(other):
            if self.acquired_dots == other.acquired_dots:
                same = True
        return same


class DotNode(Node):
    """c
    """
    def __init__(self, state, parent, cost):
        """c
        """
        super(DotNode, self).__init__(state, parent, cost)
        self.acquired_dots = None
        self.acquired_dots = self.generate_acquired_dots()
        self.state.acquired_dots = self.acquired_dots


    def generate_acquired_dots(self):
        """c
        """
        acquired = set([])
        acquired.update((self.state.coordinates,))
        if self.acquired_dots:
            return self.acquired_dots
        if self.parent is not None:
            acquired.update(self.parent.generate_acquired_dots())
        return acquired


    def generate_successors(self, state_space):
        """c
        """
        # Skip generating successors if already generated
        if self.successors:
            return
        coords = self.state.coordinates
        adjacent = state_space[coords]
        for coord in adjacent:
            base_node = adjacent[coord]
            state = DotState(state=base_node.state)
            cost = base_node.generate_path_cost()
            node = DotNode(
                state=state,
                parent=self,
                cost=cost)
            self.successors.append(node)


class DotAgent(Agent):
    """c
    """
    def __init__(self, search_file):
        """c
        """
        super(DotAgent, self).__init__(search_file)
        self.dot_coordinates = []
        self.dot_coordinate_symbol = self.goal_state_symbol


    def evaluate(self, node, option='e'):
        """c
        """
        evaluation = None
        state_space = self.state_space
        goal = self.dot_coordinates
        node.generate_acquired_dots()
        node_coords = node.state.coordinates
        dots_left = goal.difference(node.acquired_dots)
        if len(dots_left) == 0:
            return 0
        path_cost = node.generate_path_cost()
        # OPTION A: get total distance from unvisited nodes
        if option == 'a':
            total_distance_from_dots = 0
            for dot_coord in dots_left:
                sol_node = state_space[node_coords][dot_coord]
                total_distance_from_dots += sol_node.generate_path_cost()
            evaluation = path_cost + total_distance_from_dots
        #OPTION B: distance to closest unvisited dot
        elif option == 'b':
            least_dist = None
            for dot_coord in dots_left:
                sol_node = state_space[node_coords][dot_coord]
                if least_dist == None:
                    least_dist = sol_node.generate_path_cost()
                    continue
                sol_cost = sol_node.generate_path_cost()
                least_dist = min([sol_cost, least_dist])
            evaluation = path_cost + least_dist
        #OPTION C: average distance of unvisited dots
        elif option == 'c':
            avg_distance_from_dots = 0
            for dot_coord in dots_left:
                sol_node = state_space[node_coords][dot_coord]
                avg_distance_from_dots += sol_node.generate_path_cost()
            avg_distance_from_dots = \
                int(avg_distance_from_dots/len(dots_left))
            evaluation = path_cost + avg_distance_from_dots
        #OPTION D: closest distance multiplied by length of dots_left
        elif option == 'd':
            least_dist = None
            for dot_coord in dots_left:
                sol_node = state_space[node_coords][dot_coord]
                if least_dist == None:
                    least_dist = sol_node.generate_path_cost()
                    continue
                sol_cost = sol_node.generate_path_cost()
                least_dist = min([sol_cost, least_dist])
            evaluation = path_cost + (least_dist * len(dots_left))
        #OPTION E: just the distance from closest node: no path cost
        elif option == 'e':
            least_dist = None
            for dot_coord in dots_left:
                sol_node = state_space[node_coords][dot_coord]
                if least_dist == None:
                    least_dist = sol_node.generate_path_cost()
                    continue
                sol_cost = sol_node.generate_path_cost()
                least_dist = min([sol_cost, least_dist])
            evaluation = least_dist
        print evaluation
        return evaluation



    def generate_state_space(self, search_file=None):
        """c
        """
        super(DotAgent, self).generate_state_space()
        self.dot_coordinates = set(self.dot_coordinates)
        # Generate adjacency matrix of spaces with dots in them.
        base_space = self.base_state_space
        dot_state_space = {}
        agent = Agent(search_file, state_space=base_space)
        dot_coordinates = list(self.dot_coordinates)
        for x in range(len(dot_coordinates)):
            coordx = dot_coordinates[x]
            dot_state_space[coordx] = {}
            for y in range(len(dot_coordinates)):
                coordy = dot_coordinates[y]
                # No need to check if the coordinates are equal. Basic
                # pathfinding module will just check the while loop
                # condition, and it will function as an if condition.
                ######################################################
                # Get optimal path cost between points coordx and
                # coordy
                start = copy.copy(base_space[coordx])
                goal = copy.copy(base_space[coordy])
                agent.goal_state = goal
                agent.start_state = start
                agent.search(
                    'a*',
                    new_state_space=False)
                solution = agent.solution_node
                dot_state_space[coordx][coordy] = solution
        # Overwrite base state space with adjacency matrix.
        # States should now be generated on the fly as needed based
        # off of the adjacency matrix.
        self.state_space = dot_state_space




    def generate_maze_solution(self, path):
        """Uses the maze array to build the string printed to stdout.
        """
        step = 48 # The point at which '0' is ascii encoded
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        if len(path) > 62: # Number of characters from '0' to 'z'
            array_string = '* Path very long. *'
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


    def add_to_state_space(self, array, row, col):
        """c
        """
        state_space = self.state_space
        cell_text = array[row][col]
        if cell_text not in self.wall_symbol:
            current_state = DotState((row, col), cell_text)
            if cell_text in self.start_state_symbol:
                self.start_state = current_state
                # Treat starting position as a dot_state to be
                # collected.
                self.dot_coordinates.append((row, col))
            if cell_text in self.dot_coordinate_symbol:
                self.dot_coordinates.append((row, col))
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
        if goal.issubset(acquired):
            node_has_all_dots = True
        return node_has_all_dots


    def search(self, do_not_print=True):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search.
        """
        super(DotAgent, self).search('a*', do_not_print)


#EOF
