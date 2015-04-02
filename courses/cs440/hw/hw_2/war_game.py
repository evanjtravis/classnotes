#!/usr/bin/env python

#=====================================================================
# Imports
#---------------------------------------------------------------------
from csp import AdvesarialCSP
from copy import deepcopy
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

class Player(AdvesarialCSP):
    """c
    """
    def __init__(self, csp, name, board, agency=None):
        """c
        """
        super(Player, self).__init__(csp, agency)
        self.board = board
        self.name = name
        self.score = 0


    def go(self, board):
        """c
        """
        self.search()


    def commando_para_drop(self, cell):
        """c
        """
        score = 0
        if cell.owner == None:
            cell.owner = self
            score += cell.value
        return score

    def m1_death_blitz(self, from_cell, to_cell):
        """c
        """
        score = 0
        if from_cell.owner == self:
            if to_cell.owner == None:
                to_cell.owner = self
                adjacent_cells = to_cell.get_adjacent_cells()
                for cell in adjacent_cells:
                    if cell.owner != None:
                        cell.owner = self
                        score += cell.value
        return score

    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
    def clean_solution_node(self, solution_node):
        return solution_node

    def generate_successor(self, node, action):
        successor = Node(node, action)
        return successor

    def generate_solution_dict(self, solution_node):
        pass

    def get_node_actions(self, node):
        actions = node.get_actions()
        return actions

    def get_node_from_value(self, value, terminal_nodes):
        pass

    def get_start_node(self):
        player = self
        command = None
        board = self.board
        to_cell_coords = None
        from_cell_coords = None
        parent = None
        action = Action(
            player,
            command,
            board,
            to_cell_coords,
            from_cell_coords
        )
        start_node = Node(parent, action)
        return start_node

    def get_utility_of(self, node):
        utility = node.get_utility()
        return utility
    #=================================================================

class Node(object):
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.depth = None
        self.depth = self.get_depth()

    def get_utility(self):
        utility = self.action.get_score()
        return utility

    def get_depth(self):
        if self.depth:
            return self.depth

        depth = 0
        if self.parent == None:
            return depth
        else:
            depth = 1
            depth += self.parent.get_depth()
            return depth



class Action(object):
    def __init__(
            self,
            player,
            command,
            board,
            to_cell_coords,
            from_cell_coords=None):
        self.command = command
        self.board = deepcopy(board)
        self.to_cell = self.board.get_cell(to_cell_coords)
        self.from_cell = self.board.get_cell(from_cell_coords)
        self.player = player
        self.score = self.execute_action()

    def execute_action(self):
        score = 0
        if self.command == "blitz":
            score = self.player.m1_death_blitz(self.from_cell, self.to_cell)
        elif self.command == "drop":
            score = self.player.commando_para_drop(self.to_cell)
        return score


    def get_score(self):
        return self.score


