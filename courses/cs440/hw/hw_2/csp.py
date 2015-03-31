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
# Globals
#---------------------------------------------------------------------
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
FAILURE = False
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

class AlphaBetaPruningCSP(CSP):
    pass


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


class MinimaxCSP(CSP):
    pass
#####=================================================================

class CSPAgent(object):
    def __init__(self, csp):
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
class AlphaBetaPruningCSPAgent(CSPAgent):
    def search_algorithm(self, current_node):
        """
        """
        pass


    def reset(self):
        """c
        """
        pass


    def generate_data_dict(self):
        """
        """
        pass


class BacktrackingCSPAgent(CSPAgent):
    """A generalized framework for solving backtracking assignment CSP problems. This
    class provides the interface through which these types of CSP problems are
    solved. All data representation and manipulation within a CSP is
    encapsulated by a BacktrackingCSP object, and the searching mechanisms are
    encapsulated by the BacktrackingCSPAgent object.
    """
    def __init__(self, csp):
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
        super(BacktrackingCSPAgent, self).__init__(csp)
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

class MinimaxCSPAgent(CSPAgent):
    def search_algorithm(self, current_node):
        """
        """
        pass


    def reset(self):
        """c
        """
        pass


    def generate_data_dict(self):
        """
        """
        pass
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
