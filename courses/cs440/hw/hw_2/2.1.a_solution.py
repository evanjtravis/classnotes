#!/usr/bin/env python
#=====================================================================
# Imports
#---------------------------------------------------------------------
import os
from csp import BacktrackingAgent
from course_plan import CourseAssignmentStrategy
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
        strategy = CourseAssignmentStrategy(course_file)
        agent = BacktrackingAgent(strategy)
        agent.search(toprint=True)


if __name__ == "__main__":
    main()
