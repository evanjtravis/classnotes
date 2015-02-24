#!/usr/bin/env python
"""c
"""
from a_search_with_multiple_dots import DotAgent


def main():
    """c
    """
    search_files = [
        ('test_search.txt', False),
        ('big_search.txt', True),
    ]
    for entry in search_files:
        search_file = entry[0]
        check_loops = entry[1]
        agent = DotAgent(search_file, check_loops=check_loops)
        agent.search(do_not_print=False)


if __name__ == '__main__':
    main()
