#!/bin/env/python

from classNotes.conf import settings
from optparse import OptionParser
import shutil
import os

# determine if looking for new chapter or new lecture
# look for files with lec.## naming convention in pwd
# find file w/ largest suffix number
# copy over template


_ARGS = {
    'COPY_LECTURE': True,
    'COPY_CHAPTER': False,
    'COURSE': None
}
TEMPLATE = os.path.join(settings['DIRS']['templates'], 'notes.template')
COURSES_DIR = os.listdir(settings['DIRS']['courses'])

#####################################################################
# Module Specific Definitions
#####################################################################
def copy_new_notes():
    """Copy over notes template to desired course.
    """

def is_not_a_boolean(arg):
    """Returns true if arg is not a boolean value.
    """
    if (arg != False) and (arg != True):
        return True
    else:
        return False


class _EMPTY():
    """Class whose members can be accessed in the same way as the
    options object in the OptionParser object.
    """
    pass


def _validate(options, args):
    """Determine validity of the passed options and arguments.
    """
    _validate_args(args)
    _validate_options(options)


def _validate_args(args):
    """Determine the validity of the passed arguments.
    """
    # No arguments passed for this program thus far.
    pass


def _validate_options(options):
    """Determine the validity of the passed options.
    """
    def validate_copy_chapter(copy_chapter):
        """Determine the validity o the copy_chapter option.
        """
        if is_not_a_boolean(copy_chapter):
            raise Exception(
                "Expected boolean copy_chapter option. Got: %s" % copy_chapter)
    def validate_copy_lecture(copy_lecture):
        """Determine the validity of the copy_lecture option.
        """
        if is_not_a_boolean(copy_lecture):
            raise Exception(
                "Expected boolean copy_lecture option. Got: %s" % copy_lecture)

    def validate_course(course):
        """Determine the validity of the course option.
        If course is unspecified:
            If current working directory is a level below COURSES_DIR:
                set COURSE to pwd
            Else
                error
        elif course in COURSES_DIR
            set COURSE to COURSE
        else
            error
        """
        pass

    validate_copy_chapter(options.copy_chapter)
    validate_copy_lecture(options.copy_lecture)
    validate_course(options.course)


def new_note(
        course=None,
        copy_lecture=_ARGS['COPY_LECTURE'],
        copy_chapter=_ARGS['COPY_CHAPTER']):
    """Create a new note. Specifying the course is optional, but choosing
    whether or not to copy a new lecture note or a new chapter note is
    mandadory. This command is invoked by a python program.
    """
    options = _EMPTY()
    #############################
    options.copy_chapter = copy_chapter
    options.copy_lecture = copy_lecture
    options.course = course
    #############################
    args = []
    _finish(options, args)

def main():
    """Create a new note. Specifying the course is optional, but choosing
    whether or not to copy a new lecture note or a new chapter note is
    mandadory. This command is invoked by the command line.
    """
    parser = OptionParser()
    parser.add_option(
        '-c',
        '--course',
        action='store',
        type='string',
        dest='course',
        default=_ARGS['COURSE'],
        help='Redirect copied template to chosen course within class notes.'
    )
    parser.add_option(
        '-l',
        '--lecture',
        action='store_true',
        dest='copy_lecture',
        default=_ARGS['COPY_LECTURE'],
        help="Direct program to copy new lecture notes from a template.",
    )
    parser.add_option(
        '-h',
        '--chapter',
        action='store_true',
        dest='copy_chapter',
        default=_ARGS['COPY_CHAPTER'],
        help="Direct program to copy new chapter notes from a template.",
    )
    (options, args) = parser.parse_args()
    _finish(options, args)


def _finish(options, args):
    """Execute the steps that the command line invoked and program invoked
    functions have in common.
    """
    _validate(options, args)
    copy_new_notes()


if __name__ == '__main__':
    main()
