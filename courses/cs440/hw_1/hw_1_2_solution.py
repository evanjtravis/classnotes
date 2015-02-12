#!/usr/bin/env python

from basic_pathfinding import Search


def main():
    """c
    """
    search_files = [
        'designed_map_1.txt',
    #    'designed_map_2.txt',
    ]
    search_types = [
        'gbfs',
        'a*'
    ]
    
    for search_file in search_files:
        search = Search(search_file)
        for search_type in search_types:
            search.search(search_type)


if __name__ == '__main__':
    main()
