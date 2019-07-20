#!/usr/bin/env python3

import os
import sys
import argparse
import word_search_solver

if __name__ == '__main__':

    """
    $ python3 main.py --help
    
    Script to solve word search puzzles Running this code returns the left over
    letters of the puzzle
    
    optional arguments:
      -h, --help            show this help message and exit
      -p [word search puzzle file path], --puzzle [word search puzzle file path]
                            The representation of the word search puzzle
      -s [word search set file path], --set [word search set file path]
                            A file containing the words to search for
      -w [word to search for [word to search for ...]], --word [word to search for [word to search for ...]]
                            A word to search for
      --show [show the solution in a tkinter window]

    """

    try:  # Module pandas and numpy are required
        import pandas as pd
        import numpy as np
    except ImportError:
        sys.stdout.write("Modules 'pandas' and 'nummpy' are required\n")
        sys.exit(1)

    def str_to_bool(value: str) -> bool:
        return True if str(value).lower() in ('yes', 'true', 't', 'y', '1') else False

    parser = argparse.ArgumentParser(description='Script to solve word search puzzles\n'
                                                 'running this code returns the left over letters of the puzzle')
    parser.add_argument('-p', '--puzzle', required=True, type=str,
                        help='The representation of the word search puzzle',
                        dest='puzzle_file',
                        metavar='word search puzzle file path',
                        nargs='?')
    parser.add_argument('-s', '--set', required=False, type=str,
                        help='A file containing the words to search for',
                        dest='word_set_file',
                        metavar='word search set file path',
                        nargs='?')
    parser.add_argument('-w', '--word', required=False, type=str,
                        help='A word to search for',
                        dest='words',
                        metavar='word to search for',
                        nargs='*')
    parser.add_argument('--show', type=str_to_bool, nargs='?', const=True, default=False,
                        metavar='show the solution in a tkinter window',)
    args = parser.parse_args()

    # check the file path of the word search puzzle file
    abs_puzzle_path = os.path.abspath(args.puzzle_file)
    if not os.path.exists(abs_puzzle_path):
        message = 'Puzzle file path given doesn\'t exist\n'
        sys.stdout.write(message)
        sys.exit(1)

    # check the word search set file path if a it's given
    if args.word_set_file is not None:
        abs_word_set_path = os.path.abspath(args.word_set_file)
        if not os.path.exists(abs_puzzle_path):
            message = 'Word set file path given doesn\'t exist\n'
            sys.stdout.write(message)
            sys.exit(1)

    # assure one of the options is given
    if all(word is None for word in (args.word_set_file, args.words)):
        message = ('expected [-s [word search set file path]]\n'
                   'or [-w [word to search for [word to search for ...]]]\n')
        sys.stdout.write(message)
        sys.exit(1)

    # call the class with the arguments
    ws = word_search_solver.WordSearchPuzzle(word_search_puzzle=args.puzzle_file,
                                             word_search_set_file=args.word_set_file)

    # assure one of both is chosen, if word_Set_file is available, set arg.words to None
    args.words = args.words if args.word_set_file is None else None

    # get the solution coordinates
    coordinates_set = ws.find_words_in_puzzle(args.words)

    # if the word_set_file is given, show the left over letters
    if args.word_set_file is not None:
        sys.stdout.write(str(ws.get_left_over_letters()) + "\n")

    # if some word(s) is given show the word with the respectful coordinates
    if args.words is not None and coordinates_set:
        for coordinates in coordinates_set:
            word = ws.find_word_with_coordinates(ws.puzzle_df, coordinates)
            sys.stdout.write("%s - coordinates: %s\n" % (str(word), str(coordinates)))

    # if --show is given and there are words found, show them in a tkinter window
    if bool(args.show) and coordinates_set:
        try:  # Module tkinter is required
            import tkinter as tk
        except ImportError:
            sys.stdout.write("Modules 'tkinter' is required for visualization\n")
            sys.exit(1)
        else:
            ws.visualize_solution()
