#!/usr/bin/env python
"""c
"""
import copy
import heapq
import itertools


# TODO add configuration
# TODO Extra Credit add command-line arguments (don't use optparse, just iterate
# through sys.argv)
# TODO Extra Credit implement pac-man ai with ghosts? inky = bfs, blinky = dfs,
# pinky = greedy, clyde = a*, pacman = a* dot search with different
# evaluation that is aware of ghost position. Ghosts have basic
# pathfinding search.
# TODO print BFS and DFS next to each other, print greedy and a* next
# to each other --> in solution scripts.
# TODO when generating successor states, NEVER add an anscestor state
# unless the successors would otherwise be empty.
# TODO implement diagonal nodes --> can have up to 8 successor states
# TODO organize functions and whatnot by function e.g. visual or
# searching or utilities, and then alphabetize.
# TODO FOR REPORT: Mention how tie-breaking strategy would effect
# different algos, e.g. for dfs, if the goal is far away on the y axis
# but there are a bunch of dumb nodes on the x axis.
# TODO E.C. represent wormholes --> integers 0-9 on the maze/map where
# path can jump. The successor states of wormholes are all surrounding
# nodes of all equal wormholes. Treat as a super-position
class State(object):
    """This class represents a state within a given state space.
    Each state is comprised of 2 attributes:
        coordinates --> tuple
        state_type  --> char
    """
    def __init__(self, coordinates, state_type):
        """
        Initialize the coordinates and state type of the state.
        """
        self.coordinates = coordinates
        self.state_type = state_type


    def compare(self, other):
        """c
        """
        same = False
        if self.coordinates == other.coordinates:
            same = True
        return same


    def greedy_heuristic(self, state):
        """c
        """
        # just for now
        #TODO allow assignable heuristic.
        return self.manhattan_distance_from(state)


    def manhattan_distance_from(self, state):
        """Given a State, determines the manhattan distance from
        that State.
        If the state argument is a Node, function will resolve the
        inconsistency by accessing the Node's state.
            Returns the manhattan distance --> an int
        """
        x1, y1 = self.coordinates
        if isinstance(state, Node):
            node = state
            x2, y2 = node.state.coordinates
        elif isinstance(state, tuple):
            coordinates = state
            x2, y2 = coordinates
        else:
            x2, y2 = state.coordinates
        return (abs(x1 - x2) + abs(y1 - y2))


    def get_entrance_count(self, state_keys):
        """c
        """
        entrance_count = 0
        x, y = self.coordinates
        entrances = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
        for entre in entrances:
            if entre in state_keys:
                entrance_count += 1
        return entrance_count


class Node(object):
    """This class represents a node within a search algorithm.
    Each Node is comprised of 4 attributes:
        state      --> State
        parent     --> Node
        cost       --> int
        successors --> Node list
    """
    def __init__(
            self,
            state,
            parent,
            cost):
        """Initialize state, parent, and node cost of Node.
        """
        self.state = state
        self.parent = parent
        self.cost = cost
        # Generated attributes
        self.successors = []
        self.path = []
        self.heap_count = None
        self.heap_priority = None
        self.total_path_cost = 0
        self.total_path_cost = self.generate_path_cost()

    #TODO merge generate_path and generate_path_cost
    def generate_path(self):
        """Recursively works its way down the Node's ancestors to
        the start state, aggregating the coordinates of each node
        into a list.
        """
        if self.parent is not None:
            return self.parent.generate_path() + \
                [self.state.coordinates]
        else:
            return [self.state.coordinates]


    def generate_path_cost(self):
        """Recursively works its way down the Node's ancestors to
        the start state, aggregating the cost of each node.
        """
        if self.total_path_cost:
            return self.total_path_cost
        if self.parent is not None:
            return self.cost + self.parent.generate_path_cost()
        else:
            return self.cost


    def generate_successors(self, state_space):
        """Generate the successor Nodes of the Node.
        Succesor nodes can only be located in the cardinal
        directions.
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
            if child in state_space:
                state = self.get_state_from_state_space(child, state_space)
                node = self.create_successor(state)
                self.successors.append(node)

    def get_state_from_state_space(self, coords, state_space):
        """c
        """
        return copy.copy(state_space[coords])


    def create_successor(self, state):
        """c
        """
        # TODO dynamically assign cost for later version of program.
        return Node(
            state=state,
            parent=self,
            cost=1)

    def manhattan_distance_from(self, state):
        """Wrapper function. Returns the manhattan distance (int)
        of Node's state to given State (int).
        """
        return self.state.manhattan_distance_from(state)


class Agent(object):
    """This class represents all of the data and functions associated
    with a search, such as the frontier and state space.
        start_state_symbol --> char, defines the start state in the
                                     maze
        goal_state_symbol --> char, defines the goal state in the
                                    maze
        wall_symbol --> char, marks the walls in the maze
        state_symbol --> char, marks the states in the maze
        maze_array --> char list, contains entire maze in a 2D char
                       list
        count_of_expanded_nodes --> Keeps track of the running count
                                    of expanded Nodes for a single
                                    search
        frontier --> Node list
        visited_states --> State list
        start_state --> State, Generated with the state space
        goal_state --> State, Generated with the state space
        search_file --> string, Name of file in local directory to
                                read in as a maze.
        state_space --> dict, A dictionary whose keys are state
                              coordinates and whose values are the
                              resultant states.

    """
    def __init__(self, search_file, state_space=None):
        """Initialize the search_file of the Search.
        """
        # Possible Configurable Values
        self.start_state_symbol = 'P'
        self.goal_state_symbol = '.'
        self.wall_symbol = '%'
        self.state_symbol = ' ' # Can't configure with ConfigParser
        self.path_state_symbol = '.'
        self.traversed_state_symbol = '0'
        self.frontier_state_symbol = 'X'
        ##############################
        # Data to keep up-to-date for output
        self.maze_array = None
        self.count_of_expanded_nodes = 0
        self.solutions_dict = {
            'Path Cost': None,
            'Expanded Node Count': None,
            'Maze Solution': None
        }
        self.frontier = []
        self.visited_states = []
        self.start_state = None
        self.start_node = None
        self.goal_state = None
        self.solution_node = None
        self.search_file = search_file
        # Saves time by not generating pre-made state_space
        if state_space == None:
            self.state_space = {}
        else:
            self.state_space = state_space
        self.base_state_space = {}
        self.heap_counter = itertools.count()
        self.status = 'Failed'
        # Used to customize printout
        self.SHOW_VISITED = False
        self.SHOW_FRONTIER = False


    def _a_star_search(self):
        """Pick the node on the frontier with the lowest evaluation
        function result.
        The heuristic used is the Manhattan distance from goal
        The evaluation function = heuristic result + path cost
            Returns the next node to be expanded
        """
        next_node = self.get_from_frontier_heap()
        return next_node


    def get_from_frontier_heap(self):
        """c
        """
        return heapq.heappop(self.frontier)[2]

    def _breadth_first_search(self):
        """Expands the shallowest unexpanded node.
        Implemented with frontier as FIFO queue.
            Returns the next node to be expanded
        """
        next_node = self.frontier.pop(0)
        return next_node


    def _depth_first_search(self):
        """Expands the deepest unexpanded node.
        Implemented with frontier as LIFO stack.
            Returns the next node to be expanded.
        """
        next_node = self.frontier.pop()
        return next_node


    def _greedy_best_first_search(self):
        """Picks the node on the frontier with the lowest heuristic
        function result.
        The heuristic used is the Manhattan distance from goal.
            Returns the next node to be expanded.
        """
        frontier = self.frontier
        next_node = frontier[0]
        index_to_pop = None
        goal = self.goal_state
        for index in range(len(frontier)):
            node = frontier[index]
            if (node.manhattan_distance_from(goal) < \
                    next_node.manhattan_distance_from(goal)):
                next_node = node
                index_to_pop = index
        if index_to_pop is None:
            index_to_pop = 0
        next_node = frontier.pop(index_to_pop)
        return next_node

    def already_in_heap(self, node, frontier):
        """c
        """
        to_replace = False
        in_frontier = False
        index_to_pop = None
        for index in range(len(frontier)):
            entry = frontier[index]
            frontier_node = entry[2] # where child is
            # TODO standardize schema of heap item in class scope
            if frontier_node.state.compare(node.state):
                if frontier_node.generate_path_cost() \
                        < node.generate_path_cost():
                    to_replace = True
                    index_to_pop = index
                    break
                in_frontier = True
        if to_replace == True:
            # Node will be added to frontier automatically during the
            # search while loop. This function will return False in
            # order to allow the search loop to add the replacing
            # node.
            frontier.pop(index_to_pop)
            heapq.heapify(frontier)
        return in_frontier

    def already_in_frontier(self, node, search_name, frontier=None):
        """A Node is given as an argument. Determines if the Node's
        State is currently in the frontier.
        If the Node's state is already in the frontier, the path cost
        of each Node is compared, and the Node in the frontier is
        replaced if its path cost is greater than the path cost of
        the passed Node.
        NOTE: The passed Node will replace the old Node at the same
        index for this implementation.
            return True if the node is already in the frontier,
            Else return False
        """
        heap_searches = ['a*'] #TODO set in class scope
        if frontier == None:
            frontier = self.frontier
        if frontier == []:
            return False
        if search_name in heap_searches:
            return self.already_in_heap(node, frontier=frontier)
        for index in range(len(frontier)):
            frontier_node = frontier[index]
            if frontier_node.state.compare(node.state):
                if frontier_node.generate_path_cost() \
                        < node.generate_path_cost():
                    frontier[index] = node
                return True
        return False


    def already_visited(self, node, visited_states=None):
        """A Node is given as an argument. Determines if the Node's
        State has been visited by the Search.
            return True if the node has already been expanded,
            Else returm false
        """
        if visited_states == None:
            visited_states = self.visited_states
        for visited in visited_states:
            if node.state.compare(visited):
                return True
        return False


    def evaluate(self, node):
        """Determines the Node's A* algorithm evaluation function.
        Utilizes the manhattan distance.
            Returns the sum of path_cost and manhattan distance
        """
        goal = self.goal_state
        man_dist = node.manhattan_distance_from(goal)
        path_cost = node.generate_path_cost()
        return man_dist + path_cost


    def generate_maze_solution(self, path):
        """Uses the maze array to build the string printed to stdout.
        """
        visited = self.visited_states
        frontier = self.frontier
        array = copy.deepcopy(self.maze_array)
        array_string = ''
        if array is None:
            return array_string
        if self.SHOW_FRONTIER == True:
            for node in frontier:
                x, y = node.state.coordinates
                array[x][y] = self.frontier_state_symbol
        if self.SHOW_VISITED == True:
            for state in visited:
                x, y = state.coordinates
                array[x][y] = self.traversed_state_symbol
        for coordinate in path:
            x, y = coordinate
            array[x][y] = self.path_state_symbol
        for row in range(len(array)):
            for col in range(len(array[row])):
                array_string += array[row][col]
            array_string += '\n'
        return array_string


    def generate_solutions_dict(self, solution_node):
        """Calls the necessary functions to generate the solution
        dictionary. Takes the solution Node as an argument.
            Returns the solutions dictionary.
        """
        solutions = self.solutions_dict
        path = solution_node.generate_path()
        solutions['Maze Solution'] = self.generate_maze_solution(path)
        solutions['Path Cost'] = solution_node.generate_path_cost()
        solutions['Expanded Node Count'] = \
            self.count_of_expanded_nodes


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
        base_state_count = 0
        f = open(search_file, 'r')
        array = f.read().splitlines()
        f.close()
        # Break file text into 2D array of characters
        for line in range(len(array)):
            array[line] = list(array[line])
        # Keep the array for use in printing out solution later
        self.maze_array = copy.deepcopy(array)
        # Create states from 2D array
        for row in range(len(array)):
            for col in range(len(array[row])):
                if self.add_to_state_space(array, row, col):
                    base_state_count += 1
        self.base_state_space = copy.deepcopy(self.state_space)
        return base_state_count

    def add_to_state_space(self, array, row, col):
        """c
        """
        state_space = self.state_space
        cell_text = array[row][col]
        if cell_text not in self.wall_symbol:
            current_state = State((row, col), cell_text)
            if cell_text in self.start_state_symbol:
                self.start_state = current_state
            if cell_text in self.goal_state_symbol:
                self.goal_state = current_state
            state_space[(row, col)] = current_state
            return True
        return False


    def node_is_valid(self, node, search_name):
        """A Node is given as an argument. Determines if the Node
        is valid by comparing its state with the states in the
        visited nodes list and the frontier list.
            return True if Node is not expanded or on the frontier,
            Else return False
        """
        # Check if node's state already exists in visited nodes.
        # Check if node's state already exists in frontier.
        if (not self.already_visited(node)):
            if (not self.already_in_frontier(node, search_name)):
                return True
        return False


    def print_solutions_dict(self, search_name, do_not_print):
        """Iterates through the keys of the solutions dictionary
        and prints the values in a readable format to stdout.
        Each solution is printed out with a lable indicating the
        search algorithm used.
        """
        if do_not_print == True:
            return
        solutions = self.solutions_dict
        search_name = search_name.upper()
        # Notify user of status of search
        self.status = self.status.upper()
        print "########## SEARCH STATUS: %s ##########" %(self.status)
        # Print the search label
        print "########## %s SEARCH RESULTS for '%s' ##########" \
                %(search_name, self.search_file)
        # Print the solutions dictionary
        for key in solutions.keys():
            print "%25s:\n%s" %(key, solutions[key])


    def generate_start_node(self):
        """c
        """
        return Node(
            state=self.start_state,
            parent=None,
            cost=0)

    def valid_start_state(self):
        """c
        """
        if self.start_state is None:
            return False
        return True

    def valid_goal_state(self):
        """c
        """
        if self.goal_state == None:
            return False
        return True

    def has_reached_goal(self, current_node):
        """c
        """
        if not current_node.state.compare(self.goal_state):
            return False
        return True

    def add_to_visited_states(self, state):
        """c
        """
        self.visited_states.append(state)


    def search(self,
               search_name,
               new_state_space=True,
               do_not_print=True):
        """The main driver of the program. Generates needed data for
        the search then calls the necessary functions to aggregate and
        display results to stdout. Finally, resets the state of the
        Search object for the next search.
        """
        # Restart the state of the Search object
        # Restart at the beginning of the search so that these
        # variables can be accessed and analyzed at the end of a
        # successful or failed search.
        self.reset()
        if (new_state_space == True):
            self.state_space = {}
            self.generate_state_space()
        if not self.state_space:
            self.generate_state_space()
        #########################################
        if not self.valid_start_state():
            raise Exception("Start state '%s' not found." \
                    %(self.start_state_symbol))
        if not self.valid_goal_state():
            raise Exception("Goal state '%s' not found." \
                    %(self.goal_state_symbol))

        self.start_node = self.generate_start_node()
        # TODO move functions dict to class accessible location
        functions = {
            'bfs': self._breadth_first_search,
            'dfs': self._depth_first_search,
            'gbfs': self._greedy_best_first_search,
            'a*': self._a_star_search
        }
        search_name = search_name.lower()
        current_node = self.start_node
        while not self.has_reached_goal(current_node):
            self.add_to_visited_states(current_node.state)
            current_node.generate_successors(self.state_space)
            self.count_of_expanded_nodes += 1
            for child in current_node.successors:
                if self.node_is_valid(child, search_name):
                    self.add_to_frontier(search_name, child)
            if self.frontier:
                # Unique functions for each search called
                current_node = functions[search_name]()
            else:
                self.SHOW_VISITED = True
                self.generate_solutions_dict(current_node)
                self.print_solutions_dict(search_name, do_not_print)
                raise Exception(
                    "'%s' search failed. Empty frontier." \
                            %(search_name))
            if current_node is None:
                break

        self.solution_node = current_node
        solution_node = self.solution_node
        self.status = 'Success'
        self.generate_solutions_dict(solution_node)
        self.print_solutions_dict(search_name, do_not_print)

    def add_to_frontier(self, search_name, child):
        """c
        """
        # TODO reference heap_algos once moved to class accessible
        # location
        heap_algos = ['a*']
        frontier = self.frontier
        if search_name in heap_algos:
            priority = None
            count = next(self.heap_counter)
            if search_name == 'a*':
                priority = self.evaluate(child)
            child.heap_priority = priority
            child.heap_count = count
            entry = [priority, count, child]
            heapq.heappush(frontier, entry)
        else:
            frontier.append(child)

    def reset(self):
        """c
        """
        self.frontier = []
        self.visited_states = []
        self.count_of_expanded_nodes = 0
        self.status = 'Failed'
        self.heap_counter = itertools.count()
        self.solution_node = None


