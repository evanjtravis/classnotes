#!/usr/bin/env python
"""
CSP Specification for problem.

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

"""
# REMEMBER: CourseState holds information based on the semester,
# CourseNode hold information based on a collection of CourseStates.
from itertools import combinations
from basic_pathfinding import Agent, Node, State
from copy import deepcopy

class CourseState(State):
    """Represents a semester.
    """
    def __init__(self, courses, semester='F'):
        """c
        """
        super(CourseState, self).__init__(self, None, None)
        self.courses = set(courses)
        self.course_ids = None
        self.semester = semester
        self.cost = None
        self.hours = None
        self._generate_None_vars()


    def _generate_None_vars(self):
        """c
        """
        cost = 0
        hours = 0
        course_ids = []
        if self.semester == None: # Indicates the starting node
            self.corse_ids = set()
            self.cost = 0
            self.hourse = 0
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
        self.cost = cost
        self.hours = hours
        self.course_ids = set(course_ids)


    def is_locally_valid(self, course_sort):
        """c
        """
        CMin = course_sort.CMin
        CMax = course_sort.CMax
        prereqs = set()
        if (self.hours < CMin) or (self.hours > CMax):
            return False
        # Compare courses set and each course's prerequisite courses
        # to see if they intersect.
        for course in self.courses:
            prereqs.update(course.prereqs)
        intersection = prereqs.intersection(self.courses)
        if len(intersection) > 0:
            return False
        return True

    def compare(self, other):
        """c
        """
        if self.courses == other.courses:
            if self.semester == other.semester:
                return True
        return False


class CourseNode(Node):
    """c
    """
    def __init__(self, state, parent, cost, hours):
        """c
        """
        # Determine cost for node based on it's state's semester cost
        super(CourseNode, self).__init__(state, parent, cost)
        self.hours = hours
        self.total_hours = 0
        self.total_hours = None
        self.total_hours = self.generate_hours()
        self.classes_taken = set()
        self.classes_taken = self.generate_classes_taken()


    def generate_classes_taken(self):
        """c
        """
        # Save some time. Don't go all the way back to the start node
        # if you don't have to.
        if self.classes_taken:
            return self.classes_taken

        classes_taken = deepcopy(self.state.course_ids)
        if self.parent is not None:
            classes_taken.update(self.parent.generate_classes_taken())
            return classes_taken
        else:
            return classes_taken


    def generate_hours(self):
        """Akin to generate_path_cost, to recursively add up the hours
        for the entire node based on parent states.
        """
        if self.total_hours:
            return self.total_hours
        if self.parent is not None:
            return self.hours + self.parent.generate_hours()
        else:
            return self.hours

    def generate_successors(self, state_space):
        """c
        """
        # iterate over domain --> course_combos
        # if len(course_combo.intersect(classes_taken) == 0:
        #   instantiate ClassState object --> state
        #   child = create_successor(state)
        #   self.successors.append(child)
        if self.successors:
            return
        # Finalize state space format first


    def create_successor(self, state):
        """c
        """
        pass


class CourseAgent(Agent):
    """c
    """

    def generate_solutions_dict(self, solution_node):
        """c
        """
        pass

    def generate_start_node(self):
        """c
        """
        pass

    def has_reached_goal(self, current_node):
        """c
        """
        pass

    def add_to_visited_states(self, state):
        """c
        """
        pass


    # Don't overwrite search function. Modify to fit CSP. Add to list
    # of search names.
    def __init__(self, search_file, state_space=None):
        """c
        """
        super(CourseAgent, self).__init__(search_file, state_space)
        self.data = {}
        # Initialize Variables:
        self.courses = {}
        ## The following variables are populated from the file:
        ### Number of Courses
        self.N = 0
        ### Minimum number of credits that can be taken
        self.CMin = 0
        ### Maximum number of credits that can be taken
        self.CMax = 0
        ### Set of interesting courses to be taken
        self.interesting = set()
        ### The budget of MC --> the student
        self.B = 0
        # Populate the variables with the correct values as they are
        # read in from the input file:
        self.read_search_file()
        self.domain = self.generate_domain()


    def generate_domain(self):
        """c
        """
        course_combos = []
        courses = self.courses.values()
        # Create base combinations of courses
        for i in range(len(courses)):
            combos = combinations(courses, i + 1)
            for combo in combos:
                course_combos.append(combo)
        # Iterate through combinations to weed out inconsistent ones:
        #   > CMax
        #   < CMin
        #   Prerequisites in same semester
        clean_course_combos = []
        for course_combo in course_combos:
            dummy = CourseState(course_combo)
            if (dummy.is_locally_valid(self) and \
                    (course_combo not in clean_course_combos)):
                    # Preserve commutativity
                clean_course_combos.append(course_combo)
        return clean_course_combos

    def read_search_file(self):
        """c
        """
        search_file = self.search_file
        # Read lines into an array
        f = open(search_file, 'r')
        array = f.read().splitlines()
        f.close()
        # Split lines by spaces
        for line_number in range(len(array)):
            array[line_number] = array[line_number].split(' ')
            # The elements in each line are still strings. Convert to
            # integers
            for element in range(len(array[line_number])):
                array[line_number][element] = \
                    int(array[line_number][element])
        # Consume each line of the array and record relevant data.
        array = self.consume_first_line(array)
        array = self.consume_n_course_lines(array)
        array = self.consume_n_prereq_lines(array)
        array = self.consume_interesting_courses_line(array)
        self.consume_last_line(array)


    def consume_first_line(self, array):
        """c
        """
        # Process first line:
        first_line = array[0]
        ## Assign values to: N, CMin, CMax
        ## Remove first line from array
        self.N = first_line[0]
        self.CMin = first_line[1]
        self.CMax = first_line[2]
        array.pop(0)
        return array


    def consume_n_course_lines(self, array):
        """c
        """
        # Process next N lines:
        ## Assign values to: identity FP, SP, H
        ## Create Course objects with assigned values.
        ### Add these courses to the course dictionary indexed by
        ###     their identity.
        ## Remove N from the array
        for line_number in range(self.N):
            line = array[line_number]
            # Course identities start @ 1, whereas line_number starts
            # @ 0
            identity = line_number + 1
            FP = line[0]
            SP = line[1]
            H = line[2]
            course = Course(identity, FP, SP, H)
            self.courses[identity] = course
        array = array[self.N:]
        return array


    def consume_n_prereq_lines(self, array):
        """c
        """
        # Process next N lines:
        ## Set prerequisites on existing courses
        ## Remove N lines from the array
        for line_number in range(self.N):
            line = array[line_number]
            identity = line_number + 1
            # Check to see if there are any prerequisites at all
            if line[0] == 0:
                continue
            course = self.courses[identity]
            # Split list of pre-reqs, skipping first entry as it only
            # indicates the number of prerequisites.
            course.set_prereqs(self.courses, line[1:])
        array = array[self.N:]
        return array


    def consume_interesting_courses_line(self, array):
        """c
        """
        # Process next line:
        ## Set interesting courses list
        ## Remove line
        interesting_line = array[0]
        # Split list of interesting courses, skipping first entry as
        # it only indicates the number of iteresting courses.
        interesting = interesting_line[1:]
        for course_id in interesting:
            self.interesting.update(self.courses[course_id])
        array.pop(0)
        return array


    def consume_last_line(self, array):
        """c
        """
        # Process last line:
        ## Assign Value to: B
        ## return function
        last_line = array[0]
        self.B = last_line[0]
        return


class Course(object):
    """c
    """
    def __init__(self, identity, FP, SP, H):
        """c
        """
        # The line number the course falls in
        self.identity = identity
        # Fall semester price
        self.FP = FP
        # Spring semester price
        self.SP = SP
        # Credit hours of course
        self.H = H
        # List of identity numbers indicateing the pre-requisite
        # courses for this course
        self.prereqs = set()
        # Has the student taken this class? Defaults to False.
        self.is_taken = False


    def set_prereqs(self, prereq_ids, courses):
        """c
        """
        # No need to set pre-prerequisites, because by keeping track
        # of already taken classes, semesters are either valid or
        # invalid if the pre-req courses are already taken.
        prereqs = set()
        for identity in prereq_ids:
            prereqs.update(courses[identity])
        self.prereqs = prereqs










