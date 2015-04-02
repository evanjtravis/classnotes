#!/usr/bin/env python
"""
This module specifies the basic framework of a CSP problem. It defines
the basic framework used to solve such a problem.
A CSPAgent interfaces with a CSP object in predefined ways. The
CSP class is then subclassed by a specific CSP problem-solving
approach, which is then subclassed by a specific CSP problem.
The needed functions are overridden as needed within the concrete
class definitions of the specific CSP problems.
"""
#=====================================================================
# Imports
#---------------------------------------------------------------------
import datetime
import sys
#=====================================================================

#=====================================================================
# Globals
#---------------------------------------------------------------------
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
FAILURE = False
MAXINT = sys.maxint
MININT = -sys.maxint - 1
NONE = "KEY NOT USED IN SHARED DATA"
#=====================================================================

#=====================================================================
# ABSTRACT CLASSES
#---------------------------------------------------------------------
#####=================================================================
##### CSP Classes
#####-----------------------------------------------------------------
class Strategy(object):
    """A class that contains all of the interfaces that
    backtracking, alpha-beta pruning, and minimax CSPs share.
    """
    #=================================================================
    # Mandatory Display Functions Interface
    #-----------------------------------------------------------------
    def get_start_node(self):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)

    def generate_solution_dict(self, solution_node):
        """Hollow function used to ensure implementation by
        non-abstract child classes. Requires those classes to
        implement a standard for printing output to stdout.
        Arguments:
            solution_node:
                Arbitrary Node whose type is known by csp
        Returns:
            A dictionary with arbitrary key-value pairs.
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================

class AdvesarialStrategy(Strategy):
    """
    """
    #=================================================================
    # Mandatory Sub-Class Interface Functions
    #-----------------------------------------------------------------
    def generate_successor(self, node, action):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def get_node_actions(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def get_utility_of(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================

    #=================================================================
    # Optional Sub-class Interface
    #-----------------------------------------------------------------
    def prioritize_nodes(self, nodes):
        """
        """
        node = nodes[0]
        return node
    #=================================================================


class BacktrackingStrategy(Strategy):
    """A generalized framwork for implementing CSP assignment problems
    that use backtracking. This class provides an interface through
    which these types of CSP problems can be represented. This class
    insures that any CSP problem that inherits from this class
    implements their own versions of basic functions needed in order
    to solve the problem.
    """
    def add(self, value, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def assignment_is_complete(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def clean_solution_node(self, solution_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def is_within_constraints(self, node, value):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def order_domain_values(self, var, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def remove(self, value, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def select_unassigned_variable(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)

#####=================================================================

class Agent(object):
    def __init__(self, strategy, agency=None):
        self.agency = agency
        self.strategy = strategy
        self.solution_node = None
        self.start_node = self.get_start_node()
    #=================================================================
    # Standard Functions
    #-----------------------------------------------------------------
    def end_search(self, toprint):
        """c
        """
        if self.solution_node == FAILURE:
            raise Exception("Search Failed.")
        if toprint == True:
            self.print_solution()


    def search(self, toprint=False):
        self.reset()
        self.solution_node = self.search_algorithm(self.start_node)
        self.solution_node =\
            self.clean_solution_node(self.solution_node)
        self.end_search(toprint)

    def get_solution_node(self):
        solution_node = self.solution_node
        return solution_node
    #=================================================================

    #=================================================================
    # Display Functions
    #-----------------------------------------------------------------
    def generate_solution_dict(self):
        """Function wrapper for a CSP problem. Uses the data with the
        agent's csp to generate a value.
        """
        return self.strategy.generate_solution_dict(self.solution_node)


    def print_solution(
            self,
            extra_data=None,
            message=None,
            suppress_solution=False):
        """Main driver of display functions.
        """
        solution_dict = self.generate_solution_dict()
        data_dict = self.generate_data_dict()
        self.print_solution_dict(
            solution_dict,
            data_dict,
            extra_data=extra_data,
            message=message,
            suppress_solution=suppress_solution
        )
    #=================================================================

    #=================================================================
    # Strategy Interface Functions
    #-----------------------------------------------------------------
    def get_start_node(self):
        """A wrapper function to the CSPAgent's csp functionality.
        Returns:
            start_node:
                Arbritrary node type known by csp
        """
        start_node = self.strategy.get_start_node()
        return start_node

    def clean_solution_node(self, solution_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            solution_node:
                Arbitrary Node whose type is known by csp
        Returns:
            clean_node:
                Arbitrary Node from csp.
        """
        clean_node = self.strategy.clean_solution_node(solution_node)
        return clean_node


    def print_solution_dict(
            self,
            solution_dict,
            data_dict,
            extra_data=None,
            message=None,
            suppress_solution=False):
        """Prints the solution dict generated by the agent's csp to
        stdout.
        """
        header = '\n########################################\n'
        print header
        if message:
            print str(message)
        if suppress_solution == False:
            for key in solution_dict:
                print "%-20s\n\t%20s" %\
                    (str(key), str(solution_dict[key]))
        for key in data_dict:
            print "%-20s\n\t%20s" %\
                (str(key), str(data_dict[key]))
        if extra_data:
            for key in extra_data:
                print "%-20s\n\t%20s" %\
                    (str(key), str(extra_data[key]))
        print header
    #=================================================================

    #=================================================================
    # Mandatory Subclass Interface Functions
    #-----------------------------------------------------------------
    def reset(self):
        """c
        """
        raise Exception(NOT_IMPLEMENTED)



    def search_algorithm(self, node):
        """
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================

    #=================================================================
    # Optional Subclass Interface Functions
    #-----------------------------------------------------------------
    def generate_data_dict(self):
        """Implemented in child classes. Provide additional
        information to be printed along with the csp's solution
        node data. Must return a dictionary. The dictionary can be
        empty.
        """
        data_dict = {}
        return data_dict
    #=================================================================


#=====================================================================

#=====================================================================
# Concrete Classes
#---------------------------------------------------------------------
class Agency(object):
    """A class designed to coordinate like-CSP Agents and shared
    data. Not fully implemented. More of a future project.
    """
    def __init__(self, agents):
        """
        """
        self.agents = agents
        self.shared = {}

    def get(self, key):
        """
        """
        self.shared.get(key, NONE)

class AdvesarialAgent(Agent):
    """c
    """
    def __init__(self, strategy, depth, maximum=True, agency=None):
        """
        """
        super(AdvesarialAgent, self).__init__(strategy, agency)
        self.maximum = maximum
        self.depth = depth
        self.terminal_nodes = {}
        self.expanded_nodes = 0
        self.turns_taken = 0
        self.average_nodes_expanded = 0
        self.time_taken = 0
        self.average_time_taken = 0
    #=================================================================
    # Mandatory Sub-class Interface
    #-----------------------------------------------------------------
    def get_value(self, node, min_or_max_func=max):
        """Hollow for concrete agent.
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================
    def clear(self):
        self.terminal_nodes = {}
        self.expanded_nodes = 0
        self.turns_taken = 0
        self.average_nodes_expanded = 0
        self.time_taken = 0
        self.average_time_taken = 0

    def get_node_from_value(self, value):
        nodes = self.terminal_nodes[value]
        node = self.strategy.prioritize_nodes(nodes)
        return node

    def search_algorithm(self, node):
        """
        """
        start_time = datetime.datetime.now()
        value = None
        if self.maximum == True:
            value = self.get_value(node)
        else:
            value = self.get_value(node, min_or_max_func=min)
        stop_time = datetime.datetime.now()
        self.time_taken += (stop_time - start_time).microseconds
        node = self.get_node_from_value(value)
        action = self.get_action_from_node(node)
        self.turns_taken += 1
        self.average_time_taken =\
            float(self.time_taken)/float(self.turns_taken)/1000000.0
        self.average_nodes_expanded =\
            float(self.expanded_nodes)/float(self.turns_taken)
        return action

    def add_to_terminal_nodes(self, utility, node):
        """c
        """
        terminal_nodes = self.terminal_nodes
        if utility in terminal_nodes:
            terminal_nodes[utility].append(node)
        else:
            terminal_nodes[utility] = [node]
        self.terminal_nodes = terminal_nodes

    def is_terminal(self, node):
        """c
        """
        depth = self.depth
        node_depth = node.get_depth()
        terminal = False
        if node_depth == depth:
            terminal = True
        utility = None
        if terminal:
            utility = self.get_utility_of(node)
            self.add_to_terminal_nodes(utility, node)
        return terminal, utility

    def reset(self):
        """c
        """
        self.terminal_nodes = {}

    def generate_data_dict(self):
        """c
        """
        data_dict = {
            "Expanded Node Count:": self.expanded_nodes,
            "Turns Taken:": self.turns_taken,
            "Average Nodes Expanded per Turn:": self.average_nodes_expanded,
            "Total Time Taken (seconds):": self.time_taken/1000000.0,
            "Average Time Taken per Turn:": self.average_time_taken
        }
        return data_dict



    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
    def generate_successor(self, node, action):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        self.expanded_nodes += 1
        #-------------------------------------------------------------
        successor = self.strategy.generate_successor(node, action)
        return successor

    def get_action_from_node(self, node):
        """
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        action = self.strategy.get_action_from_node(node)
        return action


    def get_node_actions(self, node):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        actions = self.strategy.get_node_actions(node)
        return actions


    def get_utility_of(self, node):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        utility = self.strategy.get_utility_of(node)
        return utility


    #=================================================================


class AlphaAgent(AdvesarialAgent):
    def __init__(self, csp, depth, maximum=True, agency=None):
        super(AlphaAgent, self).__init__(
                csp,
                depth,
                maximum=maximum,
                agency=agency)
        self.alpha = MININT
        self.beta = MAXINT

    def get_value(self, node, min_or_max_func=max):
        node_is_terminal, utility = self.is_terminal(node)
        if node_is_terminal:
            return utility
        a = self.alpha
        b = self.beta
        #-------------------------------------------------------------
        # Min and Max Diff
        value = MININT
        if min_or_max_func == min:
            value = MAXINT
        #-------------------------------------------------------------
        for action in self.get_node_actions(node):
            successor = \
                self.generate_successor(node, action)
            #---------------------------------------------------------
            # Min and Max Diff: Determine Recursive Step
            successor_value = None
            if min_or_max_func == max:
                successor_value = self.get_value(
                    successor,
                    min_or_max_func=min
                )
            elif min_or_max_func == min:
                successor_value = self.get_value(
                    successor,
                    min_or_max_func=max
                )
            #---------------------------------------------------------
            value = min_or_max_func(
                value,
                successor_value,
                a,
                b
            )
            #---------------------------------------------------------
            # Min and Max Diff
            if min_or_max_func == max:
                if value >= b:
                    return value
                self.alpha = max(a, value)
            elif min_or_max_func == min:
                if value <= a:
                    return value
                self.beta = min(b, value)
            #---------------------------------------------------------
        return value

    def reset(self):
        super(AlphaAgent, self).reset()
        self.alpha = MININT
        self.beta = MAXINT


class BacktrackingAgent(Agent):
    """A generalized framework for solving backtracking assignment CSP problems. This
    class provides the interface through which these types of CSP problems are
    solved. All data representation and manipulation within a CSP is
    encapsulated by a BacktrackingCSP object, and the searching mechanisms are
    encapsulated by the BacktrackingCSPAgent object.
    """
    def __init__(self, csp, agency=None):
        """Initialize the CSPAgent.
        Arguments:
            csp:
                An object that inherits from BacktrackingCSP
        Members:
            attempted_assignments:
                int, A running count of how many times a newly
                assigned variable to a value is checked against the
                csp constraints.
            csp:
                SEE ARGUMENTS
            start_node:
                The root assignment of the CSPAgent.
            solution_node:
                Initialized to None. Holds the solution node of the
                CSP after a search is executed.
        """
        super(BacktrackingAgent, self).__init__(csp, agency)
        self.attempted_assignments = 0
    #=================================================================
    # Main/CSP Interface Functions
    #-----------------------------------------------------------------
    def reset(self):
        """Reset the CSPAgent for the next search.
        """
        self.attempted_assignments = 0


    def generate_data_dict(self):
        """c
        """
        data = {
            'Attempted Assignments:': self.attempted_assignments,
        }
        return data


    def search_algorithm(self, node):
        """The backbone of a CSP assignment problem. This function is executed
        recursively until a valid assignment is achieved. This function is an implemented interface funtion of CSPAgent.
        Arguments:
            search_name:
                string, A valid search name
            node:
                Arbitrary Node type known by csp
        Globals:
            FAILURE
        Returns:
            result:
                Boolean, False when a Boolean
                OR
                Node, the type of which is arbitrary and known by csp
        CSP Interface Functions Called:
            add
            assignment_is_complete
            is_within_constraints
            order_domain_values
            remove
            select_unassigned_variable
        """
        if self.assignment_is_complete(node):
            solution_node = node
            return solution_node
        var = self.select_unassigned_variable(node)
        for value in self.order_domain_values(var, node):
            if self.is_within_constraints(node, value):
                node = self.add(value, node)
                #-----------------------------------------------------
                # Recursive Search
                result = self.search_algorithm(node)
                #-----------------------------------------------------
                if result != FAILURE:
                    return result
                node = self.remove(value, node)
        return FAILURE
    #=================================================================

    #=================================================================
    # BacktrackingCSP Interface Functions
    #   All of these functions act as wrappers for a BacktrackingCSP
    #   object's functions, but may provide some additional
    #   bookkeeping needed by the BacktrackingCSPAgent object.
    #-----------------------------------------------------------------
    def add(self, value, node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            node:
                Arbitrary Node whose type is known by csp
        Returns:
            next_node:
                Arbitrary Node from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        next_node = self.strategy.add(value, node)
        return next_node


    def assignment_is_complete(self, node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            node:
                Arbitrary Node type known by csp
        Returns:
            complete:
                Boolean, True if the current node is a complete
                assignment, false otherwise.
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        complete = self.strategy.assignment_is_complete(node)
        return complete


    def is_within_constraints(self, node, value):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            node:
                Arbitrary Node type known by csp
            value:
                Arbitrary value type known by csp
        Returns:
            valid:
                Boolean, True if node fulfills constraints of
                csp, false otherwise.
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        self.attempted_assignments += 1
        #-------------------------------------------------------------
        valid = self.strategy.is_within_constraints(node, value)
        return valid


    def order_domain_values(self, var, node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            var:
                Arbitrary variable whose type is known by csp
            node:
                Arbitrary Node whose type is known by csp
        Returns:
            domain:
                Arbitrary collection of assignable values to the
                variable known by csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        domain = self.strategy.order_domain_values(var, node)
        return domain


    def remove(self, value, node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            node:
                Arbitrary Node whose type is known by csp
        Returns:
            next_node:
                Arbitrary Node from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        next_node = self.strategy.remove(value, node)
        return next_node


    def select_unassigned_variable(self, node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            node:
                Arbitrary Node whose type is known by csp
        Returns:
            var:
                Arbitrary variable type from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        var = self.strategy.select_unassigned_variable(node)
        return var
    #=================================================================

class MinimaxAgent(AdvesarialAgent):
    """MAXIMUM AS DEFAULT ALWAYS
    """
    def get_value(self, node, min_or_max_func=max):
        """c
        """
        node_is_terminal, utility = self.is_terminal(node)
        if node_is_terminal:
            return utility
        #-------------------------------------------------------------
        # Min and Max Diff
        value = MININT
        if min_or_max_func == min:
            value = MAXINT
        #-------------------------------------------------------------
        for action in self.get_node_actions(node):
            successor = \
                self.generate_successor(node, action)
            #---------------------------------------------------------
            # Min and Max Diff: Determine Recursive Step
            successor_value = None
            if min_or_max_func == max:
                successor_value = self.get_value(
                    successor,
                    min_or_max_func=min
                )
            elif min_or_max_func == min:
                successor_value = self.get_value(
                    successor,
                    min_or_max_func=max
                )
            #---------------------------------------------------------
            value = min_or_max_func(
                value,
                successor_value,
            )
        return value
    #=================================================================
#=====================================================================

#=====================================================================
# Utilities
#---------------------------------------------------------------------
def list_string(alist):
    """Handy utility function for print lists.
    Arguments:
        alist:
            list, An arbitary collection of elements.
    Returns:
        A String with each element in the list prepended with
        newline and tab escape sequences.
    """
    msg = '['
    for elem in alist:
        msg += '\n\t'
        msg += str(elem)
    msg += '\n]'
    return msg
#=====================================================================
