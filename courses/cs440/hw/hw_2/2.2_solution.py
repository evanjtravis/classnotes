#!/usr/bin/env python
#=====================================================================
# Imports
#---------------------------------------------------------------------
import os
#=====================================================================

def main():
    """c
    """
    boards_dir = 'game_boards'
    board_files = []
    directory = os.listdir(boards_dir)
    for element in directory:
        filename = os.path.join(boards_dir, element)
        if (os.path.isfile(filename) and\
                os.path.splitext(filename)[1] == '.txt'):
            board_files.append(filename)

    for board_file in board_files:
        # RUN THE GAMES HERE


if __name__ == "__main__":
    main()
