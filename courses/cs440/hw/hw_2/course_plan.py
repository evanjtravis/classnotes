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
import copy
from csp import CSP
from itertools import combinations

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


class CourseAssignment(CSP):
    """Representative of a node.
    """
    def __init__(self, course_file):
        """c
        """
        self.next_semester = None
        # Initialize Variables:
        self.courses = {}
        ## The following variables are populated from the input file:
        self.N = 0 # Number of Courses
        self.CMin = 0 # Min number of credits per semester
        self.CMax = 0 # Max number of credits per semester
        self.interesting = set() # Set of interesting courses
        self.B = 0 # The budget of MC --> the student
        #-------------------------------------------------------------
        # Populate the variables with the correct values as they are
        # read in from the input file:
        parser = CourseFileParser(course_file)
        data = parser.read_search_file()
        self.set_vars(data)
        #-------------------------------------------------------------
        self.domain = self.generate_domain()
    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
    def add(self, value, current_node):
        """Value not used, next_semester, which is derived from value
        is used instead.
        """
        next_semester = copy.copy(self.next_semester)
        next_node = CourseAssignmentNode(next_semester,
                                         current_node)
        return next_node


    def assignment_is_complete(self, current_node):
        """c
        """
        complete = True
        courses_taken = current_node.courses_taken
        if self.interesting.issubset(courses_taken):
            pass
        else:
            complete = False
        return complete


    def get_start_node(self):
        """c
        """
        semester = Semester([], semester=None)
        start_node = CourseAssignmentNode(semester=semester,
                                          parent=None)
        return start_node


    def is_within_constraints(self, current_node, value):
        """Value is a set of courses not yet taken.
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
            pass
        else:
            valid = False
        #-------------------------------------------------------------
        return valid


    def order_domain_values(self, var, current_node):
        """c
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
            return set(new_domain)


    def remove(self, value, current_node):
        """c
        """
        parent = current_node.parent
        parent.bad_combos.append(value)
        return parent


    def select_unassigned_variable(self, current_node):
        """c
        """
        return None
    #=================================================================


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
            dummy = Semester(course_combo)
            if (dummy.is_locally_valid(self) and \
                    #-------------------------------------------------
                    # Preserve commutativity
                    (course_combo not in clean_course_combos)):
                    #-------------------------------------------------
                clean_course_combos.append(course_combo)
        return clean_course_combos


    def set_vars(self, data):
        """c
        """
        self.courses = data['courses']
        self.N = data['N']
        self.CMin = data['CMin']
        self.CMax = data['CMax']
        for identity in data['interesting']:
            self.interesting.update(self.courses[identity])
        self.B = data['B']


class CourseAssignmentNode(object):
    """c
    """
    def __init__(self, semester, parent):
        """c
        """
        self.semester = semester
        self.parent = parent
        self.semesters = self.get_semesters()
        self.courses_taken = None
        self.courses_taken = self.get_courses_taken()
        self.bad_combos = []

    def get_semesters(self):
        """
        """
        semesters = [self.semester]
        if self.parent == None:
            return semesters
        else:
            return semesters + self.parent.semesters


    def get_courses_taken(self):
        """c
        """
        if self.courses_taken:
            return self.courses_taken
        courses_taken = set()
        for semester in self.semesters:
            courses_taken.update(semester.courses)
        return courses_taken


    def get_next_semester(self):
        """c
        """
        if self.semester.semester == 'F':
            return 'S'
        else:
            return 'F'


class Semester(object):
    """Represents a semester.
    """
    def __init__(self, courses, semester='F'):
        """c
        """
        self.courses = set(courses)
        self.course_ids = None
        self.semester = semester
        self.cost = None
        self.hours = None
        self.prereqs = None
        self._generate_None_vars()


    def _generate_None_vars(self):
        """c
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


    def is_locally_valid(self, course_sort):
        """c
        """
        CMin = course_sort.CMin
        CMax = course_sort.CMax
        prereqs = self.prereqs
        if (self.hours < CMin) or (self.hours > CMax):
            return False
        # Compare courses set and each course's prerequisite courses
        # to see if they intersect.
        intersection = prereqs.intersection(self.courses)
        if len(intersection) > 0:
            return False
        return True




class CourseFileParser(object):
    """c
    """
    def __init__(self, course_file):
        """c
        """
        self.course_file = course_file
        self.data = {}
        self.data['courses'] = {}
        self.data['interesting'] = set()


    def read_search_file(self):
        """c
        """
        course_file = self.course_file
        # Read lines into an array
        f = open(course_file, 'r')
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
        # Consume each line of the array and store relevant data.
        array = self.consume_first_line(array)
        array = self.consume_n_course_lines(array)
        array = self.consume_n_prereq_lines(array)
        array = self.consume_interesting_courses_line(array)
        self.consume_last_line(array)
        return self.data


    def consume_first_line(self, array):
        """c
        """
        # Process first line:
        first_line = array[0]
        ## Assign values to: N, CMin, CMax
        self.data['N'] = first_line[0]
        self.data['CMin'] = first_line[1]
        self.data['CMax'] = first_line[2]
        ## Remove first line from array
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
        ## Slice N lines from the array
        for line_number in range(self.data['N']):
            line = array[line_number]
            # Course identities start @ 1, whereas line_number starts
            # @ 0
            identity = line_number + 1
            FP = line[0]
            SP = line[1]
            H = line[2]
            course = Course(identity, FP, SP, H)
            self.data['courses'][identity] = course
        array = array[self.data['N']:]
        return array


    def consume_n_prereq_lines(self, array):
        """c
        """
        # Process next N lines:
        ## Set prerequisites on existing courses
        ## Slice N lines from the array
        for line_number in range(self.data['N']):
            line = array[line_number]
            identity = line_number + 1
            # Check to see if there are any prerequisites at all
            if line[0] == 0:
                continue
            course = self.data['courses'][identity]
            # Split list of pre-reqs, skipping first entry as it only
            # indicates the number of prerequisites.
            course.set_prereqs(self.data['courses'], line[1:])
        array = array[self.data['N']:]
        return array


    def consume_interesting_courses_line(self, array):
        """c
        """
        # Process next line:
        ## Update interesting courses set
        ## Remove line
        interesting_line = array[0]
        # Split list of interesting courses, skipping first entry as
        # it only indicates the number of iteresting courses.
        interesting = interesting_line[1:]
        for course_id in interesting:
            self.data['interesting'].update(course_id)
        array.pop(0)
        return array


    def consume_last_line(self, array):
        """c
        """
        # Process last line:
        ## Assign Value to: B
        ## return function
        last_line = array[0]
        self.data['B'] = last_line[0]
        return
