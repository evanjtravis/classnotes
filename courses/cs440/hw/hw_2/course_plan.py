#!/usr/bin/env python
"""
The CSP specification for the course assignment problem.

Variables:          Semester
Domains:            Combination of Courses taken in a given semester
Constraints (A):    - A student cannot take more than the maximum
                      number of credits for each semester.
                    - A student cannot take less than the minimum
                      number of credits for each semester.
                    - A course can only be taken if its pre-requisite
                      courses were taken in a previous semester.
                    - All courses interesting to a student must be
                      taken before graduation.
                    - The student cannot retake any courses.
                    - The first semester is always a Fall semester.

This program solves the course assignment problem. All possible
courses are generated based on an input file. Courses are organized
into valid combinations called Semesters which are then used to
create data that is usable by the assignment problem. Further
constraints are placed on the semesters where the credit hours for
those sememesters must fall between a minimum and maximum number.

There also exists a set of interesting courses that must be taken by
the student before they graduate.

Finally, this program makes use of a node tree structure where each
node represents the assignment of the following Semester.

The program utilizes a backtracking algorithm in order to solve the
problem.
"""
# TODO when generating domain, prioritize combos that contain
# interesting courses.
#=====================================================================
# Imports
#---------------------------------------------------------------------
import os
from csp import BacktrackingCSP
from itertools import combinations
#=====================================================================

class Course(object):
    """A representation of a course. Contains the different prices for
    the fall and spring semesters, as well as the number of credit
    hours that the course is worth. Each course is mapped to an
    identifying number that is used by different components of the
    program for aggregate or individual reference or modification.
    """
    def __init__(self, identity, FP, SP, H):
        """Initialize the Course.
        Arguments:
            identity:
                int, Uniquely identifies course.
            FP:
                int, Fall semester price.
            SP:
                int, Spring semester price.
            H:
                int, Credit hours of the course.
        Members:
            FP:
                SEE ARGUMENTS
            H:
                SEE ARGUMENTS
            identity:
                SEE ARGUMENTS
            prereqs:
                set, Collection of Course objects that are
                prerequisites to the course. Initially empty.
            SP:
                SEE ARGUMENTS
        """
        self.identity = identity # The line number the course falls in
        self.FP = FP # Fall semester price
        self.SP = SP # Spring semester price
        self.H = H # Credit hours for the course
        self.prereqs = set() # Set of prerequisite course objects


    def set_prereqs(self, prereq_ids, courses):
        """Populate the prerequisites set of the course.
        Arguments:
            prereq_ids:
                list, ID numbers mapped to existing courses.
            courses:
                dict, where keys are ID numbers of courses and values
                are the corresponding courses.
        """
        prereqs = set()
        for identity in prereq_ids:
            prereqs.update((courses[identity],))
        self.prereqs = prereqs


class CourseAssignmentCSP(BacktrackingCSP):
    """This class represents the interface through which the csp is
    solved. CourseAssignmentsCSP inherits from csp.CSP, which provides
    the functions used by a CSPAgent to solve the problem.
    """
    #=================================================================
    # Initialization Functions
    #-----------------------------------------------------------------
    def __init__(self, course_file):
        """Initialize the CourseAssignmentCSP.
        Arguments:
            course_file:
                string, A path to a valid input file.
        Members:
            B:
                int, The budget of the student.
            CMax:
                int, The maximum number of credits that the student is
                able to take in a given Semester.
            CMin:
                int, The minimum number of credits that the student is
                able to take in a given semester.
            courses:
                dict, where the keys are identifying numbers of
                courses, and where the values are the corresponding
                courses.
            course_file:
                SEE ARGUMENTS
            dirty_trick_used:
                Boolean, Is true if the domain-shrinking dirty trick
                is used during generate_domain()
            domain:
                2D list of sets, In theory, contains all valid course
                combinations. Contains the values used to create
                Semester objects which in turn are used to create
                nodes within the assignment tree.
            interesting:
                set, Contains course objects that are interesting to
                the student.
            N:
                int, The number of courses specified in the input
                file.
            next_semester:
                Semester, intialized to None but will eventually hold
                the Semester object that is created with a new value
                from the domainint, The budget of the student.
        Variables:
            data:
                dict, Where the keys are the names of the
                CourseAssignmentCSP's members and the values are the
                values that are then mapped to those members. Created
                by the parser.
            parser:
                CourseFileParser, This functionality used to exist
                within the CSP itself, but was abstracted out to avoid
                confusion. Generates the data variable.
        """
        self.course_file = os.path.basename(course_file)
        self.next_semester = None
        #-------------------------------------------------------------
        # Printed Output Specific Variables
        self.dirty_trick_used = False
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # The following variables are populated from the input file:
        self.B = 0 # The budget of MC --> the student
        self.CMax = 0 # Max number of credits per semester
        self.CMin = 0 # Min number of credits per semester
        self.courses = {}
        self.interesting = set() # Set of interesting courses
        self.N = 0 # Number of Courses
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Populate the variables with the correct values as they are
        # read in from the input file:
        parser = CourseFileParser(course_file)
        data = parser.read_search_file()
        self.set_vars(data)
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Once variables are set, we are ready to generate the domain.
        self.domain = self.generate_domain()
        #-------------------------------------------------------------

    def set_vars(self, data):
        """Maps the variables contained within data to members of the
        CourseAssignmentCSP.
        Arguments:
            data:
                dict, whose keys are members of CourseAssignmentCSP,
                and whose values are equal to the mapped values of
                those members.
        """
        self.courses = data['courses']
        self.N = data['N']
        self.CMin = data['CMin']
        self.CMax = data['CMax']
        for identity in data['interesting']:
            self.interesting.update((self.courses[identity],))
        self.B = data['B']

    #####=============================================================
    ##### Domain Generation Functions
    #####-------------------------------------------------------------
    def determine_maximum_semester_size(self):
        """Determines the maximum number of courses that can be
        present in any given Semester.
        Returns:
            max_size:
                int, The maximum number of courses that can be present
                in any given Semester as determined by the algorithm.
        """
        max_credits = self.CMax
        hours_list = self.get_course_hours_list()
        #-------------------------------------------------------------
        # Add all of the course hours together to see if they
        # are equal to or greater than CMax. If not, maximum semester
        # size defaults to number of courses.
        all_hours = sum(hours_list)
        if all_hours <= max_credits:
            return len(hours_list)
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Add up the smallest credit hours and remove them from a list
        # until we reach CMax. The number of removed courses
        # determines the maximum semester size.
        removed_count = 0
        credit_sum = 0
        while ((credit_sum < max_credits) and (len(hours_list) > 0)):
            credit_sum += hours_list[0]
            hours_list.pop(0)
            removed_count += 1
        #-------------------------------------------------------------
        max_size = removed_count
        return max_size


    def determine_minimum_semester_size(self):
        """Determines the minimum number of courses that can be
        present in any given Semester.
        Returns:
            min_size:
                int, The minimum number of courses that can be present
                in any given Semester as determined by the algorithm.
        """
        min_credits = self.CMin
        hours_list = self.get_course_hours_list()
        #-------------------------------------------------------------
        # Add up the largest credit hours and remove them from a list
        # until we reach CMin. The number of removed courses
        # determines the minimum semester size.
        removed_count = 0
        credit_sum = 0
        while ((credit_sum < min_credits) and (len(hours_list) > 0)):
            credit_sum += hours_list[-1]
            hours_list.pop(-1)
            removed_count += 1
        #-------------------------------------------------------------
        min_size = removed_count
        return min_size


    def generate_domain(self):
        """Creates and sets the domain of the course assignment CSP
        problem.
        Returns:
            domain:
                2D list of sets, where each set is a combination of
                internally valid course combinations.
        """
        courses = self.courses.values()
        #-------------------------------------------------------------
        # Determine minimum number of courses needed to fulfill
        # minimum hours per semester
        min_sz = self.determine_minimum_semester_size()
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Determine maximum number of courses allowed to be under
        # maximum hours per semester
        max_sz = self.determine_maximum_semester_size()
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Dirty Trick:
        #   If number of courses is greater than 20, just include all
        #   combinations of length min_sz by reassigning max_sz to the
        #   same value.
        #   Otherwise, time is an issue. This shortcut illustrates a
        #   proof of concept at the very least and fulfills the
        #   minimum requirements for a 3 credit assignment.
        #
        #   This change could be avoided if more solutions were
        #   implemented in order to cut down on the size of the
        #   initial domain.
        if len(courses) > 20:
            self.dirty_trick_used = True
            max_sz = min_sz
        #-------------------------------------------------------------
        clean_course_combos = []
        #-------------------------------------------------------------
        # Create base combinations of courses
        for i in range(min_sz, max_sz + 1):
            combos = combinations(courses, i)
            for a_combo in combos:
                course_combo = set(a_combo)
                #-----------------------------------------------------
                # Iterate through combinations to weed out
                # inconsistent ones:
                #   Prerequisites in same semester
                dummy = Semester(course_combo)
                if (dummy.is_internally_valid() and \
                        #---------------------------------------------
                        # Preserve commutativity
                        (course_combo not in clean_course_combos)):
                        #---------------------------------------------
                    clean_course_combos.append(course_combo)
                #-----------------------------------------------------
        domain = clean_course_combos
        return domain


    def get_course_hours_list(self):
        """A utility function used to determine the maximum and
        minimum number of courses that can be present in any given
        Semester.
        Returns:
            hours_list:
                list, A sorted collection of all credit hours that
                correspond to the CSP's courses.
        """
        hours_list = []
        for course_id in self.courses:
            course = self.courses[course_id]
            hours_list.append(course.H)
        hours_list.sort()
        return hours_list
    #####=============================================================
    #=================================================================

    #=================================================================
    # CSP Logic Functions Interface
    #-----------------------------------------------------------------
    def add(self, value, current_node):
        """A csp.CSP interface implementation. Represents the creation
        of a child node when given its parent and a new value to be
        assigned.
        Arguments:
            value:
                Not used. next_semester, which is derived from value,
                is used instead. This occurs while the value is still
                being tested against the CSP's constraints.
            current_node:
                CourseAssignmentNode, the parent node of the returned
                node.
        Returns:
            next_node:
                CourseAssignmentNode
        """
        next_semester = self.next_semester
        next_node = CourseAssignmentNode(current_node,
                                         next_semester)
        return next_node


    def assignment_is_complete(self, current_node):
        """A csp.CSP interface implementation. Implements the goal
        test of the CourseAssignmentCSP.
        Arguments:
            current_node:
                CourseAssignmentNode
        Returns:
            complete:
                Boolean, True if assignment is complete, false
                otherwise.
        """
        complete = True
        courses_taken = current_node.courses_taken
        if self.interesting.issubset(courses_taken):
            pass
        else:
            complete = False
        return complete


    def clean_solution_node(self, solution_node):
        """A csp.CSP interface implementation. Once the solution node
        is found, this function modifies it to prepare it for
        processing output.
        Arguments:
            solution_node:
                CourseAssignmentNode, is representative of a
                successful assignment.
        Returns:
            solution_node:
                CourseAssignmentNode, now clean and ready to process.
        """
        # Disregard root node, is considered empty.
        solution_node.semesters = solution_node.semesters[1:]
        return solution_node


    def get_start_node(self):
        """A csp.CSP interface implementation. Creates and returns the
        initial node for the CSP assignment problem.
        Returns:
            start_node:
                CourseAssignmentNode, containing skeleton data for a
                node so that everything works, but the solution data
                is unaffected. The start node is designed to fulfill
                all constraints and vice versa.
        """
        semester = Semester([], semester=None)
        start_node = CourseAssignmentNode(parent=None,
                                          semester=semester)
        return start_node


    def is_within_constraints(self, current_node, value):
        """A csp.CSP interface implementation. Creates a Semester
        object against the current node's semester list to ensure that
        if it were assigned to a following node that it would follow
        the constraints of the csp problem. The constraints are
        designed to pass a skeleton (or start) node.
        Arguments:
            current_node:
                CourseAssignmentNode
            value:
                set, Contains a combination of courses used to create
                a Semester object.
        Returns:
            valid:
                Boolean, True if the new value passes the constraints
                given, false otherwise.
        """
        valid = True
        next_semester_season = current_node.get_next_semester()
        next_semester = Semester(value, next_semester_season)
        self.next_semester = next_semester
        #-------------------------------------------------------------
        # A course can only be taken if its pre-requisite courses were
        # taken in a previous semester.
        courses_taken = current_node.courses_taken
        prereqs = next_semester.prereqs
        if prereqs.issubset(courses_taken):
            valid = True and valid
        else:
            valid = False
        #-------------------------------------------------------------
        return valid


    def order_domain_values(self, var, current_node):
        """A csp.CSP interface implementation. Returns a subset of the
        domain based off of the courses taken by the current_node.
        Arguments:
            var:
                Not Used. CSP assumes that the next variable to be
                assigned is just an additional semester.
            current_node:
                CourseAssignmentNode
        Returns:
            domain:
                2D list of sets
            OR
            new_domain:
                A subset of domain.
        """
        if current_node.parent == None:
            return self.domain
        else:
            new_domain = []
            bad_combos = current_node.bad_combos
            courses_taken = current_node.courses_taken
            for course_combo in self.domain:
                if ((not course_combo.intersection(courses_taken))\
                        and (course_combo not in bad_combos)):
                    new_domain.append(course_combo)
            return new_domain


    def remove(self, value, current_node):
        """A csp.CSP interface implementation. Represents the
        backtracking action of the search algorithm.
        Arguments:
            value:
                set, Contains an invalid collection of courses.
            current_node:
                CourseAssignmentNode, An invalid node whose latest
                assignment is a Semester whose course combination is
                equal to value.
        Returns:
            parent:
                CourseAssignmentNode, The parent of the current_node.
                The value argument is appended to its list of bad
                course combinations in order to avoid re-creating the
                current_node.
        """
        parent = current_node.parent
        parent.bad_combos.append(value)
        return parent


    def select_unassigned_variable(self, current_node):
        """Not used for this implementation. Overwritten here to avoid
        exception from base class. Would normally return a variable to
        be assigned, but the CSP assumes that the next variable is
        always a Semester that would be present in the node that
        follows the current_node.
        """
        pass
    #=================================================================

    #=================================================================
    # CSP Display Functions Interface
    #-----------------------------------------------------------------
    def generate_solution_dict(self, solution_node):
        """A csp.CSP interface implementation. Creates a dictionary
        whose values are used to print out the solution to stdout.
        Arguments:
            solution_node:
                CourseAssignmentNode
        Returns:
            solution_dict:
                dict, whose keys and values are (pretty) printed by
                the CSPAgent to stdout.
        """
        msg = ''
        #-------------------------------------------------------------
        # Fist Line of Output --> Total Cost, Number of Semesters
        total_cost = solution_node.get_total_cost()
        semester_count = solution_node.get_number_of_semesters()
        msg += "%d %d\n\t" %(total_cost, semester_count)
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Next N lines of output where N = semester_count
        for semester in solution_node.semesters:
            msg += "%d " %(len(semester.courses))
            for course_id in semester.course_ids:
                msg += "%d " %(course_id)
            msg += "\n\t"
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Last Line, Individual Semester Costs
        for semester in solution_node.semesters:
            msg += "%d " %(semester.cost)
        #-------------------------------------------------------------
        label = "Course Plan: %s" %(self.course_file)
        solution_dict = {
            "Dirty Trick Used?": self.dirty_trick_used,
            label: msg
        }
        return solution_dict
    #=================================================================


class CourseAssignmentNode(object):
    """Represents a step in the assignment of an entire class schedule
    during the student's tenure at the educational institution. Where
    a Semester represents a collection of courses, a
    CourseAssignmentNode represents a collection of Semesters.
    """
    #=================================================================
    # Initialization Functions
    #-----------------------------------------------------------------
    def __init__(self, parent, semester):
        """Initialize the CourseAssignmentNode.
        Arguments:
            semester:
                Semester, the data structure used to hold, retrieve,
                and contextulize data about collections of courses.
            parent:
                CourseAssignmentNode, the node which directly
                preceeds this created node.
        Members:
            bad_combos:
                list, Initialized to empty. Is populated with sets
                of course combinations that resulted from failed
                assignments.
            courses_taken:
                set, Initialized to None and populated by another
                function. Contains all of the courses taken when the
                semesters of the node are taken in aggregate.
            semester:
                SEE ARGUMENTS
            semesters:
                list, Containing current and ancestor semesters in
                order of occurence.
            parent:
                SEE ARGUMENTS
        """
        #-------------------------------------------------------------
        # Initial Arguments
        self.parent = parent
        self.semester = semester
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Generated Members
        self.bad_combos = []
        self.semesters = self.get_semesters()
        self.courses_taken = None
        #####---------------------------------------------------------
        ##### Depends on the complete generation of semesters.
        self.courses_taken = self.get_courses_taken()
        #####---------------------------------------------------------
        #-------------------------------------------------------------

    def get_courses_taken(self):
        """This function is used to populate the courses_taken member
        of CourseAssignmentNode.

        IMPORTANT: DEPENDS ON A COMPLETE LIST OF SEMESTERS, OTHERWISE
        PRODUCES INACCURATE DATA.
        Returns:
            courses_taken:
                set, Contains all courses taken when all of the
                CourseAssignmentNode's Semesters are taken in
                aggregate.
        """
        if self.courses_taken:
            return self.courses_taken
        courses_taken = set()
        for semester in self.semesters:
            courses_taken.update(semester.courses)
        return courses_taken


    def get_semesters(self):
        """This function is used to populate the semesters member of
        CourseAssignmentNode.
        Returns:
            list, Contains current and ancestor Semesters in order of
            occurence.
        """
        semesters = [self.semester]
        if self.parent == None:
            return semesters
        else:
            return self.parent.semesters + semesters
    #=================================================================

    #=================================================================
    # Solution Functions
    #-----------------------------------------------------------------
    def get_number_of_semesters(self):
        """This function is only executed if the node is a solution
        node, i.e. the node represents a complete assignment. The
        function determines the number of semesters present within a
        cleaned solution node.
        Returns:
            number_of_semesters:
                int
        """
        number_of_semesters = len(self.semesters)
        return number_of_semesters


    def get_total_cost(self):
        """This function is only executed if the node is a solution
        node, i.e. the node represents a complete assignment.
        The function aggregates and returns the computed cost of
        each Semester within the node's semesters member.
        Returns:
            total_cost:
                int, the sum of all Semester costs.
        """
        total_cost = 0
        for semester in self.semesters:
            total_cost += semester.cost
        return total_cost
    #=================================================================

    def get_next_semester(self):
        """Determines the next semester based on the current semester
        of the CourseAssignmentNode.
        POINT OF CLARIFICATION:
            In this instance, semester refers to the season in which
            the Semester would fall. The choices are 'F' for Fall and
            'S' for Spring.
        Returns:
            semester:
                string, Either 'F' or 'S'
        """
        semester = None
        if self.semester.semester == 'F':
            semester = 'S'
        else:
            semester = 'F'
        return semester


class CourseFileParser(object):
    """This class encapsulates all of the logic and temporary data
    structures needed to parse any given input file into usable data.
    A CourseFileParser object is instantiated by the
    CourseAssignmentCSP object once, to read in the data.
    """
    def __init__(self, course_file):
        """Initialize the CourseFileParser.
        Arguments:
            course_file:
                string, A path to a valid input file to be parsed.
        Members:
            data:
                dict, where the keys are the names of member variables
                of CourseAssignmentCSP and the values are the values
                mapped eventually mapped to those variables.
        """
        self.course_file = course_file
        self.data = {}
        self.data['courses'] = {}
        self.data['interesting'] = set()


    def read_search_file(self):
        """The main hub function that calls all of the parsing steps.
        Returns:
            data:
                dict, The completed dictionary ready to have its
                values mapped to the matching keys of the
                CourseAssignmentCSP member variables.
        """
        course_file = self.course_file
        #-------------------------------------------------------------
        # Read lines into an array
        f = open(course_file, 'r')
        array = f.read().splitlines()
        f.close()
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Split lines by spaces
        for line_number in range(len(array)):
            array[line_number] = array[line_number].split(' ')
            #---------------------------------------------------------
            # The elements in each line are still strings. Convert to
            # integers
            for element in range(len(array[line_number])):
                array[line_number][element] = \
                    int(array[line_number][element])
            #---------------------------------------------------------
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Consume each line of the array and store relevant data.
        array = self.consume_first_line(array)
        array = self.consume_n_course_lines(array)
        array = self.consume_n_prereq_lines(array)
        array = self.consume_interesting_courses_line(array)
        self.consume_last_line(array)
        #-------------------------------------------------------------
        return self.data


    def consume_first_line(self, array):
        """Consumes the first line in the array and populates the
        correct variables in the data member variable.
        Returns:
            array:
                2D list of ints, now truncated by 1 row.
        """
        first_line = array[0]
        #-------------------------------------------------------------
        # Assign values to: N, CMin, CMax
        self.data['N'] = first_line[0]
        self.data['CMin'] = first_line[1]
        self.data['CMax'] = first_line[2]
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Remove first line from array
        array.pop(0)
        #-------------------------------------------------------------
        return array


    def consume_n_course_lines(self, array):
        """Consumes the next N lines of the array as determined by the
        data read in from the first line and populates the correct
        variables in the data member variable. N corresponds to the
        number of courses present in the input file.
        These lines correspond to data that is used to create the
        available courses for the problem.
        Returns:
            array:
                2D list of ints, now trucated by N row(s).
        """
        for line_number in range(self.data['N']):
            line = array[line_number]
            #---------------------------------------------------------
            # Assign values to: identity FP, SP, H
            #####-----------------------------------------------------
            ##### Course identities start @ 1, whereas line_number
            ##### starts at 0
            #####-----------------------------------------------------
            # Create Course objects with assigned values.
            # Add these courses to the course dictionary indexed by
            #     their identity.
            identity = line_number + 1
            FP = line[0]
            SP = line[1]
            H = line[2]
            course = Course(identity, FP, SP, H)
            self.data['courses'][identity] = course
            #---------------------------------------------------------
        #-------------------------------------------------------------
        # Slice N lines from the array
        array = array[self.data['N']:]
        #-------------------------------------------------------------
        return array


    def consume_n_prereq_lines(self, array):
        """Consumes the next N lines of the array as determined by the
        data read in from the first line and populates the correct
        variables in the data member variable. N corresponds to the
        number of courses present in the input file.
        These lines are used to populate each course's set of
        prerequisite courses.
        Returns:
            array:
                2D list of ints, now truncated by N row(s).
        """
        #-------------------------------------------------------------
        # Set prerequisites on existing courses
        for line_number in range(self.data['N']):
            line = array[line_number]
            identity = line_number + 1
            #---------------------------------------------------------
            # Check to see if there are any prerequisites at all
            if line[0] == 0:
                continue
            #---------------------------------------------------------
            course = self.data['courses'][identity]
            #---------------------------------------------------------
            # Split list of pre-reqs, skipping first entry as it only
            # indicates the number of prerequisites.
            prereq_ids = line[1:]
            courses = self.data['courses']
            course.set_prereqs(prereq_ids, courses)
            #---------------------------------------------------------
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Slice N lines from the array
        array = array[self.data['N']:]
        #-------------------------------------------------------------
        return array


    def consume_interesting_courses_line(self, array):
        """Processes the first line of the truncated array in order
        to set the 'interesting' variable in the data member variable.
        This line represents the set of courses that are interesting
        to the student.
        Returns:
            array:
                list of ints, Truncated down to one last row.
        """
        interesting_line = array[0]
        #-------------------------------------------------------------
        # Split list of interesting courses, skipping first entry as
        # it only indicates the number of iteresting courses.
        interesting = interesting_line[1:]
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Update interesting courses set
        for course_id in interesting:
            self.data['interesting'].update((course_id,))
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        # Remove line
        array.pop(0)
        #-------------------------------------------------------------
        return array


    def consume_last_line(self, array):
        """Consumes the final line of array and populates the budget
        used for the CourseAssignmentCSP.
        Returns:
            None, No more rows to parse!
        """
        last_line = array[0]
        self.data['B'] = last_line[0]
        return


class Semester(object):
    """Represents either a Fall or Spring semester at a given
    institution. Semesters are defined by the courses that the student
    takes during them.
    """
    #=================================================================
    # Intialization Functions
    #-----------------------------------------------------------------
    def __init__(self, courses, semester='F'):
        """Initialize the Semester.
        Arguments:
            courses:
                set, Contains an internally valid combination of
                Course objects.
            semester:
                String, Is either 'F' for Fall or 'S' for spring.
                Defaults to 'F'. Can be None in the case of the start
                node.
        Members:
            cost:
                int, The calculated cost of all courses within a given
                Fall or Spring semester.
            courses:
                SEE ARGUMENTS
            course_ids:
                list, Contain the unique identifiers of all of the
                courses.
            hours:
                int, Contains the sum of the credit hours for all of
                the Semester's courses.
            prereqs:
                set, Contains the prerequisites for all of the
                Semester's courses.
            semester:
                SEE ARGUMENTS
        """
        self.cost = None
        self.courses = set(courses)
        self.course_ids = None
        self.hours = None
        self.prereqs = None
        self.semester = semester
        self._generate_None_vars()


    def _generate_None_vars(self):
        """Generates and populates all of the members that are
        initialized to None during the __init__ function. This is done
        by iterating over the Semester courses and incrementing,
        adding, or appending to local variables as needed. These local
        variables are then mapped onto their respective member
        variables.
        """
        cost = 0
        hours = 0
        course_ids = []
        prereqs = set()
        if self.semester == None: # Indicates the starting node
            self.course_ids = set()
            self.cost = 0
            self.hours = 0
            self.prereqs = set()
            return
        for course in self.courses:
            if self.semester == 'F':
                cost += course.FP
            elif self.semester == 'S':
                cost += course.SP
            else:
                raise Exception("Invalid semester season: '%s'."\
                                %(self.semester))
            hours += course.H
            course_ids.append(course.identity)
            prereqs.update(course.prereqs)
        self.cost = cost
        self.hours = hours
        self.course_ids = set(course_ids)
        self.prereqs = prereqs
    #=================================================================

    def is_internally_valid(self):
        """Determines whether or not the Semester fufills a series of
        local constraints.
        Returns:
            valid:
                Boolean, True if the contraints are met, false
                otherwise.

        NOTE: CMin and CMax Range is determined by finding min and max
        semester sizes, and so are not checked here.
        """
        prereqs = self.prereqs
        valid = True
        #-------------------------------------------------------------
        # Compare courses set and each course's prerequisite courses
        # to see if they intersect.
        intersection = prereqs.intersection(self.courses)
        if len(intersection) > 0:
            valid = False
        #-------------------------------------------------------------
        return valid



