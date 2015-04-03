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
        self.empty_cells = []

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
        result = ''
        board_name = 'BOARD NAME: %s\n\t' %(self.board_file)
        first_message_part = 'ORIGINGAL BOARD:\n\n\t'
        second_message_part = 'RESULTING BOARD:\n\n\t'
        msg = None
        array = self.array
        green_score = 0
        blue_score = 0
        for row in range(len(array)):
            for col in range(len(array[row])):
                cell = array[row][col]
                letter = cell.owner.name[0].upper()
                value = cell.value
                if letter == 'B':
                    blue_score += value
                else:
                    green_score += value
                first_message_part += "%s\t" %(value)
                second_message_part += "%s\t" %(letter)
            first_message_part += "\n\t"
            second_message_part += "\n\t"
        msg = board_name + first_message_part + second_message_part
        if blue_score == green_score:
            result = "IT'S A TIE!\n"
        elif blue_score > green_score:
            result = "BLUE WINS!\n"
        else:
            result = "GREEN WINS!\n" + msg
        result += "\tBlue Score: %d\tGreen Score %d\n\t" %\
            (blue_score, green_score)
        msg = result + msg
        return msg

    def get_empty_cells(self):
        if self.empty_cells:
            return self.empty_cells
        cells = []
        for cell in self.cells:
            if cell.owner == None:
                cells.append(cell)
        self.empty_cells = cells
        return cells

class BoardBoard(Board):
    def __init__(self, board):
        template = deepcopy(board)
        self.board_file = template.board_file
        self.cells = template.cells
        self.board = template.board
        self.array = template.array
        self.empty_cells = []

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
    def __init__(self, board, players, matchup):
        """c
        """
        self.board = board
        self.green = None
        self.blue = None
        self.winner = None
        self.loser = None
        self.tie = False
        self.matchup = matchup
        for player in players:
            if player.strategy.name.lower() == 'green':
                self.green = player
            elif player.strategy.name.lower() == 'blue':
                self.blue = player
        self.current_player = self.green # switched right away
        self.previous_player = self.blue
        self.action_log = []


    def play(self, toprint=True):
        """c
        """
        board = None
        while self.moves_left():
            self.next_player()
            board = self.make_player_go()
            self.board = board
        self.determine_winner()
        if toprint == True:
            self.print_game_stats()
        self.current_player.clear()
        self.previous_player.clear()

    def print_game_stats(self):
        print "<game_results>"
        print "%s as BLUE VS. %s as GREEN" %\
            (str(self.matchup[0]), str(self.matchup[1]))
        self.winner.print_solution()
        self.loser.print_solution(
            suppress_solution=True
        )
        print "</game_results>"

    def make_player_go(self):
        """c
        """
        board = self.board
        player = self.current_player
        start_node = player.get_start_node()
        player.search(start_node)
        solution_node = player.get_solution_node()
        if solution_node:
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
        self.current_player.strategy.set_board(self.board)
        self.previous_player.strategy.set_board(None)

    def determine_winner(self):
        """c
        """
        green_score = 0
        blue_score = 0
        green = self.green.strategy
        blue = self.blue.strategy
        for cell in self.board.cells:
            if green.owns_this(cell):
                green_score += cell.value
            elif blue.owns_this(cell):
                blue_score += cell.value
        green.set_score(green_score)
        blue.set_score(blue_score)
        if green_score > blue_score:
            self.winner = self.green
            self.loser = self.blue
        elif green_score < blue_score:
            self.winner = self.blue
            self.loser = self.green
        elif green_score == blue_score:
            self.tie = True


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
        _, board = solution_node.resolve_round()
        solution_dict = {
            'Board:': board.stringify()
        }
        return solution_dict

    def set_score(self, score):
        self.score = score

    def opponent_owns_this(self, cell):
        opponent_owns = False
        if not self.owns_this(cell):
            if not cell.is_empty():
                opponent_owns = True
        return opponent_owns

    def opponent_owns_these(self, cells):
        opponent_owns = False
        for cell in cells:
            if cell.is_empty():
                return opponent_owns
            if self.owns_this(cell):
                return opponent_owns
        opponent_owns = True
        return opponent_owns

    def opponent_owns_which(self, cells):
        opponent_owns = []
        for cell in cells:
            if self.opponent_owns_this(cell):
                opponent_owns.append(cell)
        return opponent_owns

    def owns_this(self, cell):
        owns = False
        if cell.is_empty():
            return owns
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


    def set_board(self, board):
        self.board = board

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
# TODO INHERIT FROM BASE CSP NODE
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

    def get_action(self):
        return self.action

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

    def is_locally_terminal(self):
        terminal = True
        empty_cells = self.action.board.get_empty_cells()
        if empty_cells:
            terminal = False
        return terminal


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
        self.board = BoardBoard(player.board)
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
        cells = self.board.get_empty_cells()
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
            if valid_drop: # Valid blitz is also a valid drop
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
                else:
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
        adjacent_cells = cell.get_adjacent_cells()
        owned_cells = self.player.owns_which(adjacent_cells)
        opponent_owned_cells =\
            self.player.opponent_owns_which(adjacent_cells)
        if owned_cells and opponent_owned_cells:
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

class MinimaxPlayer(MinimaxAgent):
    def __init__(
        self,
        strategy, # --> A PlayerStrategy
        depth,
        maximum=True, # --> Max
        agency=None):
        super(MinimaxPlayer, self).__init__(
            strategy,
            depth,
            maximum=maximum,
            agency=agency
        )

