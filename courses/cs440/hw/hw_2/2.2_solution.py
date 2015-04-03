#!/usr/bin/env python
#=====================================================================
# Imports
#---------------------------------------------------------------------
import os
import war_game
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
    # Test only one file
    board_files = ['game_boards/00_2x2Test.txt']

    minimax_depth = 3
    alpha_beta_depth = 4
    matchups = [
        [
            (war_game.MinimaxPlayer, minimax_depth),
            (war_game.MinimaxPlayer, minimax_depth)
        ],
#        [
#            (war_game.AlphaPlayer, alpha_beta_depth),
#            (war_game.AlphaPlayer, alpha_beta_depth)
#        ],
#        [
#            (war_game.MinimaxPlayer, minimax_depth),
#            (war_game.AlphaPlayer, alpha_beta_depth)
#        ],
#        [
#            (war_game.AlphaPlayer, alpha_beta_depth),
#            (war_game.MinimaxPlayer, minimax_depth)
#        ]
    ]
    for board_file in board_files:
        board = war_game.Board(board_file)
        for matchup in matchups:
            player_one_class = matchup[0][0]
            player_one_depth = matchup[0][1]
            player_two_class = matchup[1][0]
            player_two_depth = matchup[1][1]
            game_matchup = (player_one_class, player_two_class)

            player_one_strategy =\
                war_game.PlayerStrategy('blue', board)
            player_two_strategy =\
                war_game.PlayerStrategy('green', board)
            player_one = player_one_class(
                player_one_strategy,
                player_one_depth
            )
            player_two = player_two_class(
                player_two_strategy,
                player_two_depth
            )
            game_players = (player_one, player_two)
            game = war_game.Game(board, game_players, game_matchup)
            game.play()


if __name__ == "__main__":
    main()
