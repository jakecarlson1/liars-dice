#!/usr/bin/env python
# Liars Dice
# By: Jake Carlson
# 2016-10-20

# This is the main driver for the liars dice game. The main driver creates a
# game, initializes the game (using command line arguments if provided) and then
# runs the game.

# imports
import sys
import random
import classes.game as game

# main driver
def main(argv):
    # game is created
    _game = game.Game()

    # game initialization
    if len(argv) > 1:
        _game.initialize_game_cmd_line(argv)
    else:
        _game.initialize_game()

    # game loop
    _game.run_game()


if __name__ == '__main__':
    main(sys.argv)
