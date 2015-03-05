#!/usr/bin/env python

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
        self.prereqs = []


class CourseSort(object):
    """c
    """
    def __init__(self, search_file):
        """c
        """
        # Initialize Variables:
        self.search_file = search_file
        self.courses = {}
        ## The following variables are populated from the file:
        ### Number of Courses
        self.N = 0
        ### Maximum number of credits that can be taken
        self.CMax = 0
        ### Minimum number of credits that can be taken
        self.CMin = 0
        ### List of interesting courses to be taken
        self.interesting = []
        ### The budget of MC --> the student
        self.B = 0

        # Populate the variables with the correct values as they are
        # read in from the input file:
        self.read_search_file()

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
            course.prereqs = line[:]
        array = array[self.N]
        return array

    def consume_interesting_courses_line(self, array):
        """c
        """
        # Process next line:
        ## Set interesting courses list
        ## Remove line
        interesting_line = array[0]
        self.interesting = interesting_line[:]
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












