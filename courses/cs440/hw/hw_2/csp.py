#!/usr/bin/env python
"""
This module specifies the basic framework of a CSP problem. It defines
the basic framwork used to solve such a problem.
A CSPAgent interfaces with a CSP object in predefined ways. The
CSP class is then subclassed by a specific CSP problem, and the needed
functions are overridden as needed.
"""

#=====================================================================
# Globals
#---------------------------------------------------------------------
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
FAILURE = False
#=====================================================================

class CSP(object):
    """A generalized framwork for implementing CSP problems. This
    class provides an interface through which CSP problems can be
    represented. This class insures that any CSP problem that
    inherits from this class implements their own versions of basic
    functions needed in order to solve the CSP problem.
    """
    #=================================================================
    # Logic Functions Interface
    #-----------------------------------------------------------------
    def ab_pruning(self, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


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


    def MAXI(self, current_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)


    def mini(self, current_node):
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
    #=================================================================

    #=================================================================
    # Display Functions Interface
    #-----------------------------------------------------------------
    def generate_solution_dict(self, solution_node):
        """Hollow function used to ensure implementation by child
        classes.
        """
        raise Exception(NOT_IMPLEMENTED)
    #=================================================================


class CSPAgent(object):
    """A generalized framework for solving CSP problems. This
    class provides the interface through which CSP problems are
    solved. All data representation and manipulation within a CSP is
    encapsulated by a CSP object, and the searching mechanisms are
    encapsulated by the CSPAgent object. A CSPAgent object can use any
    arbitrary CSP object so long as it implements the correct
    interface functions.
    """
    #=================================================================
    # Initialization Functions
    #-----------------------------------------------------------------
    def __init__(self, csp):
        """Initialize the CSPAgent.
        Arguments:
            csp:
                An object that inherits from CSP
        Members:
            attempted_assignments:
                int, A running count of how many times a newly
                assigned variable to a value is checked against the
                csp constraints.
            csp:
                SEE ARGUMENTS
            default_search_name:
                string, The search name used by default.
            search_functions:
                A dictionary where:
                    KEYS = Names of valid early failure detection
                        strategies used by backtracking search.
                    VALUES = Functions to implement the early failure
                        detection strategies per the CSP object.
            start_node:
                The root assignment of the CSPAgent.
            solution_node:
                Initialized to None. Holds the solution node of the
                CSP after a search is executed.
        """
        self.attempted_assignments = 0
        self.csp = csp
        self.default_search_name = 'backtracking'
        self.search_functions = {
            'ab-pruning': self._ab_pruning,
            'min': self._minimax,
            'MAX': self._MINIMAX,
            self.default_search_name: self._dummy,
        }
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
    #=================================================================

    #=================================================================
    # Private Functions
    #-----------------------------------------------------------------
    def _check_search_name(self, search_name):
        """Determines if a string is a valid search name by checking
        it against the names found within search_strategies.
        Arguments:
            search_name:
                string, A valid search name.
        Exceptions:
            Raised:
                - On invalid search_name
        """
        if search_name not in self.search_functions:
            msg = "Incorrect search name.\nSearch Names:\n%s" %\
                list_string(self.search_functions.keys())
            raise Exception(msg)
    #=================================================================

    #=================================================================
    # Search Functions
    #-----------------------------------------------------------------
    def _ab_pruning(self):
        """Function wrapper for a CSP problem using alpha-beta
        pruning. Executes the steps associated with the agent's csp.
        """
        self.csp.ab_pruning()


    def _backtracking_search(self, search_name, current_node):
        """The backbone of the CSP search algorithm. is executed
        recursively until a valid assignment is achieved. If any
        intervening steps are required, they are executed depending on
        the given search_name.
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
        """
        if self.assignment_is_complete(current_node):
            solution_node = self.csp.clean_solution_node(current_node)
            return solution_node
        var = self.csp.select_unassigned_variable(current_node)
        for value in self.csp.order_domain_values(var,
                                                  current_node):
            if self.is_within_constraints(current_node, value):
                current_node = self.csp.add(value, current_node)
                #-----------------------------------------------------
                # Apply inference to reduce the space of possible
                # assignments and detect failure early.
                self.search_functions[search_name](current_node)
                #-----------------------------------------------------
                result = self._backtracking_search(search_name,
                                              current_node)
                if result != FAILURE:
                    return result
                current_node = self.csp.remove(value, current_node)
        return FAILURE


    def _dummy(self, current_node):
        """Function that does nothing.
        """
        pass

    def _minimax(self, current_node):
        """Function wrapper for a CSP problem using minimax. Executes
        the steps associated with the agent's csp.
        """
        self.csp.mini()


    def _MINIMAX(self, current_node):
        """Function wrapper for a CSP problem using Minimax. Executes
        the steps associated with the agent's csp.
        """
        self.csp.MAXI()
    #=================================================================

    #=================================================================
    # Logic Functions
    #-----------------------------------------------------------------
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
        self.attempted_assignments += 1
        valid = self.csp.is_within_constraints(current_node, value)
        return valid


    def reset(self):
        """Reset the CSPAgent for the next search.
        """
        self.attempted_assignments = 0


    def search(self, search_name=None, toprint=False):
        """The basic search function of a CSP agent. Does some initial
        bookeeping, and then proceeds with the backtracking search.
        Arguments:
            search_name:
                string, a valid search name indicating which search
                algorithm to use.
        """
        self.reset()
        if search_name == None:
            search_name = self.default_search_name
        self._check_search_name(search_name)
        self.solution_node = self._backtracking_search(search_name,
                                                  self.start_node)
        if self.solution_node == FAILURE:
            raise Exception("Search Failed.")
        if toprint == True:
            self.print_solution()
    #=================================================================

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
        self.print_solution_dict(solution_dict)


    def print_solution_dict(self, solution_dict):
        """Prints the solution dict generated by the agent's csp to
        stdout.
        """
        header = '\n########################################\n'
        print header
        for key in solution_dict:
            print "%-20s\n\t%20s" %\
                (str(key), str(solution_dict[key]))
        print "Attempted Assignments: %d" %\
            (self.attempted_assignments)
        print header
    #=================================================================


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
