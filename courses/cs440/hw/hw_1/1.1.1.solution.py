#!/usr/bin/env python

from basic_pathfinding import Agent


def main():
    """c
    """
    search_files = [
        'small_maze.txt',
        'medium_maze.txt',
        'big_maze.txt',
    ]
    search_types = [
        'bfs',
        'dfs',
        'gbfs',
        'a*'
    ]

    for search_file in search_files:
        agent = Agent(search_file)
        for search_type in search_types:
            agent.search(search_type, do_not_print=False)


if __name__ == '__main__':
    main()
