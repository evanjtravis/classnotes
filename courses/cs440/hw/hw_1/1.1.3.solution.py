#!/usr/bin/env python
"""c
"""
from a_search_with_multiple_dots import DotAgent


def main():
    """c
    """
    search_files = [
        'small_search.txt',
        'tricky_search.txt',
        'medium_search.txt',
        'big_search.txt'
    ]
    for search_file in search_files:
        agent = DotAgent(search_file)
        agent.search()


if __name__ == '__main__':
    main()
