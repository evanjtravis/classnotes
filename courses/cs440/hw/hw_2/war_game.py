#!/usr/bin/env python

#=====================================================================
# Imports
#---------------------------------------------------------------------
from csp import AdvesarialStrategy, AlphaAgent, MinimaxAgent
from copy import deepcopy
#=====================================================================
#=====================================================================
# Globals
#---------------------------------------------------------------------
LEGAL_MOVES = set([
    'blitz',
    'drop'
])
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

    def is_empty(self):
        """c
        """
        empty = False
        if self.owner == None:
            empty = True
        return empty

    def is_full(self):
        full = not self.is_empty()
        return full

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
            if cell.is_empty():
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


class PlayerStrategy(AdvesarialStrategy):
    """c
    """
    def __init__(self, name, board):
        """c
        """
        self.board = board
        self.name = name
        self.score = 0

    def owns_this(self, cell):
        owns = False
        if cell.owner == self:
            owns = True
        return owns

    def owns_these(self, cells):
        owns = False
        for cell in cells:
            if not self.owns_this(cell):
                return owns
        owns = True
        return owns

    def owns_which(self, cells):
        owns = []
        for cell in cells:
            if self.owns_this(cell):
                owns.append(cell)
        return owns

    def go(self):
        pass
    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
    def generate_successor(self, node, action):
        successor = Node(node, action)
        return successor

    def generate_solution_dict(self, solution_node):
        solution_dict = {}
        return solution_dict

    def get_node_actions(self, node):
        actions = node.get_actions()
        return actions

    def get_start_node(self):
        player = self
        command = None
        to_cell_coords = None
        from_cell_coords = None
        parent = None
        action = Action(
            player,
            command,
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

    def get_actions(self):
        actions = self.action.get_further_actions()
        return actions

    def get_utility(self):
        utility = 0
        utility += self.action.get_score()
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
            dst_cell_coords,
            src_cell_coords=None):
        self.command = command
        self.legal_moves = set([
            'blitz',
            'drop'
        ])
        if self.legal_moves != LEGAL_MOVES:
            raise Exception("Non-matching legal moves.")
        self.board = deepcopy(player.board)
        self.dst_cell = self.board.get_cell(dst_cell_coords)
        self.src_cell = self.board.get_cell(src_cell_coords)
        self.player = player
        self.score = self.execute_action()

    def execute_action(self):
        score = 0
        if self.command == "blitz":
            score = self.m1_death_blitz(self.src_cell, self.dst_cell)
        elif self.command == "drop":
            score = self.commando_para_drop(self.dst_cell)
        return score


    def commando_para_drop(self, dst_cell):
        """c
        """
        score = 0
        if dst_cell.is_empty():
            dst_cell.owner = self.player
            score += dst_cell.value
        return score


    def m1_death_blitz(self, src_cell, dst_cell):
        """c
        """
        score = 0
        if src_cell.owner == self.player:
            if dst_cell.is_empty():
                dst_cell.owner = self.player
                adjacent_cells = dst_cell.get_adjacent_cells()
                for cell in adjacent_cells:
                    if cell.owner != None:
                        cell.owner = self.player
                        score += cell.value
        return score


    def get_further_actions(self):
        """Bonus: This source code looks like a duck with a
        lightsaber (at least with my .vimrc).
        """
        cells = self.board.cells
        actions = []
        action = None
        command = None
        valid_blitz = False
        valid_drop = False
        player = self.player
        dst_coords = None
        src_coords = None
        for dst_cell in cells:
            dst_coords = dst_cell.coords
            valid_drop = self.check_valid_drop(dst_cell)
            valid_blitz, src_coordss = \
                self.check_valid_blitz(dst_cell)
            if valid_blitz:
                command = "blitz"
                for src_coords in src_coordss:
                    action = Action(
                        player,
                        command,
                        dst_coords,
                        src_coords
                    )
                    actions.append(action)
                continue # Skip paradrop action, blitz is mandatory
            if valid_drop:
                command = "drop"
                action = Action(
                    player,
                    command,
                    dst_coords
                )
                actions.append(action)
        return actions

    def check_valid_drop(self, cell):
        valid = False
        if cell.is_empty():
            valid = True
        return valid


    def check_valid_blitz(self, cell):
        valid = False
        owned_coords = []
        if cell.is_empty():
            adjacent_cells = cell.get_adjacent_cells()
            owned_cells = self.player.owns_which(adjacent_cells)
            if owned_cells:
                valid = True
                for owned_cell in owned_cells:
                    owned_coords.append(owned_cell.coords)
        return valid, owned_coords



    def get_score(self):
        score = self.score
        return score


class AlphaPlayer(AlphaAgent):
    def __init__(
        self,
        strategy,
        depth,
        player,
        maximum=True,
        agency=None):
        super(AlphaPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )
        self.player = player

class MiniPlayer(MinimaxAgent):
    def __init__(
        self,
        strategy,
        depth,
        player,
        maximum=True,
        agency=None):
        super(MiniPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )
        self.player = player




