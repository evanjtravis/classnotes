#!/usr/bin/env python
#=====================================================================
# Imports
#---------------------------------------------------------------------
import os
from csp import CSPAgent
from course_plan import CourseAssignmentCSP
#=====================================================================

def main():
    """c
    """
    grad_dir = 'graduation_instances'
    course_files = []
    directory = os.listdir(grad_dir)
    for element in directory:
        filename = os.path.join(grad_dir, element)
        if (os.path.isfile(filename) and\
                os.path.splitext(filename)[1] == '.txt'):
            course_files.append(filename)

    for course_file in course_files:
        csp = CourseAssignmentCSP(course_file)
        agent = CSPAgent(csp)
        agent.search(toprint=True)


if __name__ == "__main__":
    main()
