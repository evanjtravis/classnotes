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
        self.cells, self.board, self.array = self.generate_board()

    def get_cell(self, coords):
        """c
        """
        if coords in self.board:
            return self.board[coords]
        else:
            return None


    def generate_board(self, board_file=None):
        """c
        Do all functions look like ducks?
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
                array[line][element] = board[coords]
        return cells, board, array

    def stringify(self):
        # TODO include original ints for output before and after
        msg = '\t'
        array = self.array
        for row in range(len(array)):
            for col in range(len(row)):
                cell = array[row][col]
                letter = cell.owner.name[0].upper()
                msg += "%s\t" %(letter)
            msg += "\n\t"
        return msg



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
        self.previous_player = self.green
        self.action_log = []


    def play(self, toprint=True):
        """c
        """
        board = None
        while self.moves_left():
            self.give_control_of_board_to_current_player()
            board = self.make_player_go()
            self.board = board
            winning = self.update_scores()
            self.next_player()
        self.winner = winning
        if toprint==True:
            self.winner.print_solution()
        self.current_player.clear()
        self.previous_player.clear()

    def give_control_of_board_to_current_player(self):
        self.current_player.strategy.set_board(self.board)
        self.previous_player.strategy.set_board(None)

    def make_player_go(self):
        """c
        """
        player = self.current_player
        start_node = player.get_start_node()
        player.search(start_node)
        solution_node = player.get_solution_node()
        action, board = solution_node.resolve_round()
        self.update_action_log(action)
        return board

    def update_action_log(self, action):
        self.action_log.append(action)

    def moves_left(self):
        """c
        """
        moves_left = False
        cells = self.board.cells
        for cell in cells:
            if cell.is_empty():
                moves_left = True
                break
        return moves_left

    def next_player(self):
        """c
        """
        if self.current_player == self.green:
            self.current_player = self.blue
            self.previous_player = self.green
        else:
            self.current_player = self.green
            self.previous_player = self.blue

    def update_scores(self):
        """c
        This function also looks like a duck, only it has eyes
        AND a "tie" around its neck.
        """
        green_score = 0
        blue_score = 0
        blue = self.blue.strategy
        green = self.green.strategy
        cells = self.board.cells
        winner = "tie"
        for cell in cells:
            value = cell.value
            if green.owns(cell):
                green_score += value
            elif blue.owns(cell):
                blue_score += value
        green.set_score(green_score)
        blue.set_score(blue_score)
        if green_score > blue_score:
            winner = self.green
        elif blue_score > green_score:
            winner = self.blue
        return winner


class PlayerStrategy(AdvesarialStrategy):
    """c
    """
    def __init__(self, name, board):
        """c
        """
        self.board = board
        self.name = name
        self.score = 0

    def generate_solution_dict(self, solution_node):
        action, board = solution_node.reslove_round()
        solution_dict = {
            'Board:': board.stringify()
        }
        return solution_dict


    def set_score(self, score):
        self.score = score

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

    #=================================================================
    # CSP Interface Functions
    #-----------------------------------------------------------------
    def generate_successor(self, node, action):
        successor = Node(node, action)
        return successor

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

    def resolve_round(self):
        action = self.action
        board = action.get_board()
        return action, board

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

    def get_board(self):
        board = self.board
        return board

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
        strategy, # --> A PlayerStrategy
        depth,
        maximum=True, # --> Alpha Pruning
        agency=None):
        super(AlphaPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )

class BetaPlayer(AlphaAgent):
    def __init__(
        self,
        strategy, # --> A PlayerStrategy
        depth,
        maximum=False, # --> Beta Pruning
        agency=None):
        super(BetaPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )

class MaxiPlayer(MinimaxAgent):
    def __init__(
        self,
        strategy, # --> A PlayerStrategy
        depth,
        maximum=True, # --> Max
        agency=None):
        super(MaxiPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )

class MiniPlayer(MinimaxAgent):
    def __init__(
        self,
        strategy, # --> A PlayerStrategy
        depth,
        maximum=False, # --> Min
        agency=None):
        super(MiniPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )




