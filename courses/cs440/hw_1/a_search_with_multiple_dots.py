#!/usr/bin/env python
"""c
"""
# TODO superfy as many functions as possible.
# TODO create functions to debug. First, just generate state space and
# whatnot, then create fake path and see successors of selected node.
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


class DotNode(Node):
    """c
    """
    def __init__(self, state, parent, cost):
        """c
        """
        super(DotNode, self).__init__(state, parent, cost)


    def generate_successors(self, state_space):
        """c
        """
        super(DotNode, self).generate_successors(state_space)
        # After populating basic successors, iterate through
        # successors list and keep the Nodes whose collected dot list
        # is equal to this Node's.

        # If we come across an unvisited Node that contains its own
        # dot that this node has not yet collected, it is also kept
        # on the successors list.

        # These two rules also allow backtracking over already visited
        # states containing dots without recollecting the dot.

        # Check EACH of these conditions
        ################################
        # Unvisted      non-dot
        # unvistied     dot
        # visited       non-dot
        # visited       dot
        ################################
        # Therefore, successors should be organized by unvisited dots
        # and, failing that, go through the rest to see which gets us
        # closer to the goal. --> refactor evaluate function to choose
        # unvisited dots first.
        # Prioritize multiple unvisited dots in successors?
        #   how would that work?
        keep_list = []
        for successor in self.successors:
            if (self.valid_unvisited_nondot(successor) or \
                self.valid_visited_nondot(successor) or \
                self.valid_unvisited_dot(successor) or \
                self.valid_visited_dot(successor)):
                # THEN
                keep_list.append(successor)
        self.successors = keep_list

    def valid_unvisited_nondot(self, successor):
        """c
        """
        if successor.state.acquired_dots == \
                self.state.acquired_dots:
            return True
        return False

    def valid_visited_nondot(self, successor):
        """c
        """
        # Don't go to this coordinate if not found more dots.
        suc_acquired = successor.state.acquired_dots
        acquired = self.state.acquired_dots
        difference = acquired.difference(suc_acquired)
        if len(difference) > 0:
            if suc_acquired.issubset(acquired):
                return True
        return False

    def valid_unvisited_dot(self, successor):
        """c
        """
        suc_acquired = successor.state.acquired_dots
        acquired = self.state.acquired_dots
        difference = suc_acquired.difference(acquired)
        if len(difference) == 1:
            if acquired.issubset(suc_acquired):
                if successor.state.coordinates in difference:
                    return True
        return False

    def valid_visited_dot(self, successor):
        """c
        """
        suc_acquired = successor.state.acquired_dots
        acquired = self.state.acquired_dots
        if successor.state.coordinates in acquired:
            if suc_acquired == acquired:
                return True
        return False

    def create_successor(self, state):
        """c
        """
        return DotNode(
            state=state,
            parent=self,
            cost=1)


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
        # Look for shortest distance to dot
        goal = self.dot_coordinates
        distance_of_closest_dot = None
        for dot_coord in goal:
            if distance_of_closest_dot == None:
                distance_of_closest_dot = \
                    node.manhattan_distance_from(dot_coord)
                continue
            man_dist = node.manhattan_distance_from(dot_coord)
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
        print "\tAdding combos of dot acquisition to state space."
        state_space = self.state_space
        # Append to state space coordinates all DotStates with
        # differing combinations of collected dots.
        # 2**n combinations where n = number of dots.
        dot_coordinates = self.dot_coordinates
        dot_coordinate_combinations = []
        for i in range(1, len(dot_coordinates)):
            dot_coordinate_combinations += \
                combinations(dot_coordinates, i)
        # turn dot_coordinates into set in order to perform set
        # operations on it.
        self.dot_coordinates = set(self.dot_coordinates)
        # Make each tuple a set
        for i in range(len(dot_coordinate_combinations)):
            dot_coordinate_combinations[i] = \
                set(dot_coordinate_combinations[i])
        # Add states to state_space that represent
        # all combinations of dot aquisition.
        print "\tRemoving nonsensical states from state space."
        num_states = 0
        num_states_pre_nonsense = 0
        for _, states in state_space.iteritems():
            base_state = states[0]
            base_coordinates = base_state.coordinates
            base_state_type = base_state.state_type
            if base_state_type not in self.dot_coordinate_symbol:
                states = \
                    self.remove_nonsensical_non_dot_states(states)
            if states:
                for dot_coord_combo in dot_coordinate_combinations:
                    states.append(
                        DotState(
                            coordinates=base_coordinates,
                            state_type=base_state_type,
                            acquired_dots=dot_coord_combo
                        )
                    )
                # Remove states where dot aquisition is logically true
                # but represented as false within the data.
                # I.E. A state's set of aquired dots does not
                # contain its own dot.
                num_states_pre_nonsense += len(states)
                if base_state_type in self.dot_coordinate_symbol:
                    states = \
                        self.remove_nonsensical_dot_states(
                            states,
                            base_coordinates
                        )
                num_states += len(states)
        # Go through state space keys and delete entries whose values
        # are empty lists.
        empty_coords = []
        for coord in state_space:
            if not state_space[coord]:
                empty_coords.append(coord)
        for coord in empty_coords:
            del state_space[coord]
        print "Finished removing invalid states."
        print "\tNumber of States:              %d" %(num_states)
        print "\tMax Number of Original States: %d" \
            %(num_states_pre_nonsense)
        print "\t  - (Includes nonsensical states)"
        return num_states

    def remove_nonsensical_dot_states(self, states, coordinates):
        """c
        """
        keep_list = []
        # Remove states that are dot states and that do not have their
        # own dot acquired
        for i in range(len(states)):
            state = states[i]
            if coordinates in state.acquired_dots:
                keep_list.append(state)
        # TODO remove states that are dot states and that cannot be
        # collected without another dot being collected before or
        # after this dot.
        # Get surrounding states:
        #   if all states are dot states:
        #       remove the states at (row, col) where 1 of the
        #       surrounding states is not collected.
        return keep_list

    def remove_nonsensical_non_dot_states(self, states):
        """c
        """
        # Remove states with only one entrance (dead ends).
        # Should not effect dot states.
        keep_list = []
        state = states[0]
        min_entrances = 2
        state_keys = self.state_space.keys()
        if state.get_entrance_count(state_keys) < min_entrances:
            return keep_list
        else:
            return states

    def add_to_state_space(self, array, row, col):
        """c

        """
        state_space = self.state_space
        cell_text = array[row][col]
        if cell_text not in self.wall_symbol:
            current_state = DotState((row, col), cell_text, set())
            if cell_text in self.start_state_symbol:
                self.start_state = current_state
            if cell_text in self.dot_coordinate_symbol:
                self.dot_coordinates.append((row, col))
            if (row, col) in state_space:
                state_space[(row, col)].append(current_state)
            else:
                state_space[(row, col)] = [current_state]
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
        if current_node.state.acquired_dots == self.dot_coordinates:
            node_has_all_dots = True
        return node_has_all_dots


    def search(self):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search.
        """
        super(DotSearch, self).search('a*')


#EOF
