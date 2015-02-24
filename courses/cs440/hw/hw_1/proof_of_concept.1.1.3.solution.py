#!/usr/bin/env python
"""c
"""
from a_search_with_multiple_dots import DotAgent


def main():
    """c
    """
    search_files = [
        'big_search.txt'
    ]
    for search_file in search_files:
        agent = DotAgent(search_file)
        agent.search(do_not_print=False)


if __name__ == '__main__':
    main()
