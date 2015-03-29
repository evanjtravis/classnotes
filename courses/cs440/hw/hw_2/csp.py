#!/usr/bin/env python

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
    # Interface Functions
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
            csp     -->     CSP object
        Variables:
            search_functions:
                A dictionary where:
                    KEYS = Names of valid early failure detection
                        strategies used by backtracking search.
                    VALUES = Functions to implement the early failure
                        detection strategies per the CSP object.
            start_state:
                The start state of the CSP object.
            start_node:
                The root assignment of the CSPAgent.
            solution:
                Initialized to None. Holds the solution node of the
                CSP after a search is executed.
        """
        self.csp = csp
        self.default_search_name = 'backtracking'
        self.search_functions = {
            'ab-pruning': self._ab_pruning,
            'min': self._minimax,
            'MAX': self._MINIMAX,
            self.default_search_name: self._dummy,
        }
        self.solution = None
        self.start_node = self.get_start_node()

    def get_start_node(self):
        """c
        """
        return self.csp.get_start_node()
    #=================================================================

    #=================================================================
    # Private Functions
    #-----------------------------------------------------------------
    def _check_search_name(self, search_name):
        """Determines if a string is a valid search name by checking
        it against the names found within search_strategies.
        Arguments:
            search_name     -->     String
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
            search_name     -->     String
            current_node    -->     Arbitrary Node type known by csp
        Globals:
            FAILURE
        Returns:
            Boolean
                or
            Node, the type of which is arbitrary and known by csp
        """
        if self.assignment_is_complete(current_node):
            return current_node
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
            current_node        -->     Arbitrary Node type known by
                                        csp
        Returns:
            Boolean
        """
        return self.csp.assignment_is_complete(current_node)


    def is_within_constraints(self, current_node, value):
        """Function wrapper for a CSP problem. Uses the data within
        the agent's csp to generate a value.
        Arguments:
            current_node        -->     Arbitrary Node type known by
                                        csp
            value               -->     Arbitrary value type known by
                                        csp
        Returns:
            Boolean
        """
        return self.csp.is_within_constraints(current_node, value)


    def search(self, search_name=None):
        """The basic search function of a CSP agent. Does some initial
        bookeeping, and then proceeds with the backtracking search.
        Arguments:
            search_name     -->     String
        """
        if search_name == None:
            search_name = self.default_search_name
        self._check_search_name(search_name)
        self.solution = self._backtracking_search(search_name,
                                                  self.start_node)
    #=================================================================

    #=================================================================
    # Display Functions
    #-----------------------------------------------------------------


    #=================================================================


#=====================================================================
# Utilities
#---------------------------------------------------------------------
def list_string(alist):
    """Handy utility function for print lists.
    Arguments:
        alist       -->     List
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
