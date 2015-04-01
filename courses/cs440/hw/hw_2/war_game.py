#!/usr/bin/env python

#=====================================================================
# Imports
#---------------------------------------------------------------------
from csp import AdvesarialCSP
#=====================================================================

#=====================================================================
# Model Classes
#---------------------------------------------------------------------
class Board(object):
    """c
    """
    def __init__(self, board_file):
        """c
        """
        self.board_file = board_file
        self.cells, self.board = self.generate_board()

    def get_cell(self, coords):
        """c
        """
        if coords in self.board:
            return self.board[coords]
        else:
            return None


    def generate_board(self, board_file=None):
        """c
        """
        cells = []
        board = {}
        if board_file == None:
            board_file = self.board_file
        # Lines to array
        f = open(board_file, 'r')
        array = f.read().splitlines()
        # Each section from strings to ints
        for line in range(len(array)):
            array[line] = array[line].split('\t')
            for element in range(len(array[line])):
                # Create cells
                value = int(array[line][element])
                coords = (line, element)
                cell = Cell(self, coords, value)
                board[coords] = cell
                cells.append(board[coords])
        return cells, board


class Cell(object):
    """c
    """
    def __init__(self, board, coords, value):
        """c
        """
        self.adjacent_cells = None
        self.board = board
        self.coords = coords
        self.value = value
        self.owner = None

    def get_adjacent_cells(self):
        """c
        """
        if self.adjacent_cells:
            return self.adjacent_cells
        board = self.board
        adjacent = []
        x, y = self.coords
        adjacent_coords = [
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y)
        ]
        for coords in adjacent_coords:
            adjacent_cell = board.get_cell(coords)
            if adjacent_cell == None:
                continue
            adjacent.append(adjacent_cell)
        self.adjacent_cells = adjacent
        return adjacent


class Game(object):
    """c
    """
    def __init__(self, board, players):
        """c
        """
        self.board = board
        self.green = None
        self.blue = None
        self.winner = None
        for player in players:
            if player.name == 'green':
                self.green = player
            elif player.name == 'blue':
                self.blue = player
        self.current_player = self.blue


    def play(self):
        """c
        """
        board = self.board
        while self.moves_left():
            self.current_player.go(board)
            winning = self.update_scores()
            self.next_player()
        self.winner = winning


    def moves_left(self):
        """c
        """
        moves_left = False
        cells = self.board.cells
        for cell in cells:
            if cell.owner == None:
                moves_left = True
        return moves_left

    def next_player(self):
        """c
        """
        if self.current_player == self.green:
            self.current_player = self.blue
        else:
            self.current_player = self.green

    def update_scores(self):
        """c
        """
        green_score = 0
        blue_score = 0
        cells = self.board.cells
        for cell in cells:
            value = cell.value
            if cell.owner == self.green:
                green_score += value
            elif cell.owner == self.blue:
                blue_score += value
        self.green.score = green_score
        self.blue.score = blue_score
        if green_score > blue_score:
            return self.green
        elif blue_score > green_score:
            return self.blue
        elif blue_score == green_score:
            return "tie"

class Player(object):
    """c
    """
    def __init__(self, name, agent):
        """c
        """
        self.agent = agent # Forward CSP related functions to this
        self.name = name
        self.score = 0


    def go(self, board):
        """c
        """
        pass

    def commando_para_drop(self, cell):
        """c
        """
        if cell.owner == None:
            cell.owner = self
        else:
            raise Exception("Illegal Move, bad commando para-drop.")


    def m1_death_blitz(self, from_cell, to_cell):
        """c
        """
        if from_cell.owner == self:
            if to_cell.owner == None:
                to_cell.owner = self
                adjacent_cells = to_cell.get_adjacent_cells()
                for cell in adjacent_cells:
                    cell.owner = self
            else:
                raise Exception("Cannot blitz non-neutral cell.")
        else:
            raise Exception("Cannot blitz from non-owned cell.")

#=====================================================================

#=====================================================================
# AI Implementation
#---------------------------------------------------------------------
class WargameCSP(AdvesarialCSP):
    pass
