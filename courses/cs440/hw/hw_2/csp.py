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
class CSP(object):
    """A class that contains all of the interfaces that
    backtracking, alpha-beta pruning, and minimax CSPs share.
    """
    #=================================================================
    # Display Functions Interface
    #-----------------------------------------------------------------
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

class AdvesarialCSP(CSP):
    """
    """
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


    def get_node_from_value(self, value, terminal_nodes):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def get_utility_of(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def is_terminal(self, node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)



class BacktrackingCSP(CSP):
    """A generalized framwork for implementing CSP assignment problems
    that use backtracking. This class provides an interface through
    which these types of CSP problems can be represented. This class
    insures that any CSP problem that inherits from this class
    implements their own versions of basic functions needed in order
    to solve the problem.
    """
    def add(self, value, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def assignment_is_complete(self, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def clean_solution_node(self, solution_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def get_start_node(self):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def is_within_constraints(self, current_node, value):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def order_domain_values(self, var, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def remove(self, value, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def select_unassigned_variable(self, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)

#####=================================================================

class CSPAgent(object):
    def __init__(self, csp, agency=None):
        self.agency = agency
        self.csp = csp
        self.solution_node = None
        self.start_node = self.get_start_node()


    def get_start_node(self):
        """A wrapper function to the CSPAgent's csp functionality.
        Returns:
            start_node:
                Arbritrary node type known by csp
        """
        start_node = self.csp.get_start_node()
        return start_node


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
        self.end_search(toprint)
    #=================================================================
    # Display Functions
    #-----------------------------------------------------------------
    def generate_solution_dict(self):
        """Function wrapper for a CSP problem. Uses the data with the
        agent's csp to generate a value.
        """
        return self.csp.generate_solution_dict(self.solution_node)


    def print_solution(self):
        """Main driver of display functions.
        """
        solution_dict = self.generate_solution_dict()
        data_dict = self.generate_data_dict()
        self.print_solution_dict(solution_dict, data_dict)
    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
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
        clean_node = self.csp.clean_solution_node(solution_node)
        return clean_node


    def print_solution_dict(self, solution_dict, data_dict):
        """Prints the solution dict generated by the agent's csp to
        stdout.
        """
        header = '\n########################################\n'
        print header
        for key in solution_dict:
            print "%-20s\n\t%20s" %\
                (str(key), str(solution_dict[key]))
        for key in data_dict:
            print "%-20s\n\t%20s" %\
                (str(key), str(data_dict[key]))
        print header
    #=================================================================

    #=================================================================
    # Subclass Interface Functions
    #-----------------------------------------------------------------
    def reset(self):
        """c
        """
        raise Exception(NOT_IMPLEMENTED)


    def generate_data_dict(self):
        """Implemented in child classes. Provide additional
        information to be printed along with the csp's solution
        node data. Must return a dictionary. The dictionary can be
        empty.
        """
        raise Exception(NOT_IMPLEMENTED)


    def search_algorithm(self, current_node):
        """
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================

#=====================================================================

#=====================================================================
# Concrete Classes
#---------------------------------------------------------------------
class Agency(object):
    """A class designed to coordinate like-CSP Agents and shared
    data.
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

class AdvesarialCSPAgent(CSPAgent):
    """c
    """
    def __init__(self, csp, maximum=True, agency=None):
        """
        """
        super(AdvesarialCSPAgent, self).__init__(csp, agency)
        self.maximum = maximum

    def get_value(self, current_node, min_or_max_func=max):
        """Hollow for concrete agent.
        """
        pass


    def search_algorithm(self, current_node):
        """
        """
        value = None
        if self.maximum == True:
            value = self.get_value(current_node)
        else:
            value = self.get_value(current_node, min_or_max_func=min)
        node = self.get_node_from_value(value)
        action = self.get_action_from_node(node)
        return action


    def add_to_terminal_nodes(self, utility, current_node):
        """c
        """
        terminal_nodes = self.terminal_nodes
        if utility in terminal_nodes:
            terminal_nodes[utility].append(current_node)
        else:
            terminal_nodes[utility] = [current_node]
        self.terminal_nodes = terminal_nodes

    #=================================================================
    # AdvesarialCSP Interface Functions
    #-----------------------------------------------------------------
    def generate_successor(self, node, action):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        successor = self.csp.generate_successor(node, action)
        return successor
    def get_action_from_node(self, node):
        """
        """
        pass

    def get_node_actions(self, node):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        actions = self.csp.get_node_actions(node)
        return actions

    def get_node_from_value(self, value):
        """Allow csp to prioritize nodes in dict.
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        terminal_nodes = self.terminal_nodes
        node = self.csp.get_node_from_value(value, terminal_nodes)
        return node

    def get_utility_of(self, node):
        """c
        """
        #-------------------------------------------------------------
        # Bookkeeping
        #   NONE
        #-------------------------------------------------------------
        utility = self.csp.get_utility_of(node)
        return utility


    def is_terminal(self, node):
        """c
        """
        terminal = self.csp.is_terminal(node)
        utility = None
        if terminal:
            utility = self.get_utility_of(node)
            #---------------------------------------------------------
            # Bookkeeping
            self.add_to_terminal_nodes(utility, node)
            #---------------------------------------------------------
        return terminal, utility
    #=================================================================
    def reset(self):
        """c
        """
        self.terminal_nodes = {}


class BacktrackingCSPAgent(CSPAgent):
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
        super(BacktrackingCSPAgent, self).__init__(csp, agency)
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


    def search_algorithm(self, current_node):
        """The backbone of a CSP assignment problem. This function is executed
        recursively until a valid assignment is achieved. This function is an implemented interface funtion of CSPAgent.
        Arguments:
            search_name:
                string, A valid search name
            current_node:
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
            clean_solution_node
            is_within_constraints
            order_domain_values
            remove
            select_unassigned_variable
        """
        if self.assignment_is_complete(current_node):
            solution_node = self.clean_solution_node(current_node)
            return solution_node
        var = self.select_unassigned_variable(current_node)
        for value in self.order_domain_values(var, current_node):
            if self.is_within_constraints(current_node, value):
                current_node = self.add(value, current_node)
                #-----------------------------------------------------
                # Recursive Search
                result = self.search_algorithm(current_node)
                #-----------------------------------------------------
                if result != FAILURE:
                    return result
                current_node = self.remove(value, current_node)
        return FAILURE
    #=================================================================

    #=================================================================
    # BacktrackingCSP Interface Functions
    #   All of these functions act as wrappers for a BacktrackingCSP
    #   object's functions, but may provide some additional
    #   bookkeeping needed by the BacktrackingCSPAgent object.
    #-----------------------------------------------------------------
    def add(self, value, current_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            current_node:
                Arbitrary Node whose type is known by csp
        Returns:
            next_node:
                Arbitrary Node from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        next_node = self.csp.add(value, current_node)
        return next_node


    def assignment_is_complete(self, current_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            current_node:
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
        complete = self.csp.assignment_is_complete(current_node)
        return complete


    def is_within_constraints(self, current_node, value):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            current_node:
                Arbitrary Node type known by csp
            value:
                Arbitrary value type known by csp
        Returns:
            valid:
                Boolean, True if current_node fulfills constraints of
                csp, false otherwise.
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        self.attempted_assignments += 1
        #-------------------------------------------------------------
        valid = self.csp.is_within_constraints(current_node, value)
        return valid


    def order_domain_values(self, var, current_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            var:
                Arbitrary variable whose type is known by csp
            current_node:
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
        domain = self.csp.order_domain_values(var, current_node)
        return domain


    def remove(self, value, current_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            current_node:
                Arbitrary Node whose type is known by csp
        Returns:
            next_node:
                Arbitrary Node from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        next_node = self.csp.remove(value, current_node)
        return next_node


    def select_unassigned_variable(self, current_node):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            value:
                Arbitrary value whose type is known by csp
            current_node:
                Arbitrary Node whose type is known by csp
        Returns:
            var:
                Arbitrary variable type from csp
        """
        #-------------------------------------------------------------
        # Bookkeeping:
        #   NONE
        #-------------------------------------------------------------
        var = self.csp.select_unassigned_variable(current_node)
        return var
    #=================================================================

class MinimaxCSPAgent(AdvesarialCSPAgent):
    """MAXIMUM AS DEFAULT ALWAYS
    """
    def __init__(self, csp, maximum=True, agency=None):
        """c
        """
        super(MinimaxCSPAgent, self).__init__(csp, maximum, agency)

    def get_value(self, current_node, min_or_max_func=max):
        """c
        """
        node_is_terminal, utility = self.is_terminal(current_node)
        if node_is_terminal:
            return utility
        #-------------------------------------------------------------
        # Min and Max Diff
        value = MININT
        if min_or_max_func == min:
            value = MAXINT
        #-------------------------------------------------------------
        for action in self.get_node_actions(current_node):
            successor = \
                self.generate_successor(current_node, action)
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

    def generate_data_dict(self):
        """
        """
        pass
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
