#!/usr/bin/env python3

import os
import sys
import argparse
import word_search_solver

if __name__ == '__main__':

    try:  # Module pandas and numpy are required
        import pandas as pd
        import numpy as np
    except ImportError:
        sys.stdout.write("Modules 'pandas' and 'nummpy' are required\n")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Script to solve word search puzzles\n'
                                                 'Running this code returns the left over letters of the puzzle')
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
    args = parser.parse_args()

    abs_puzzle_path = os.path.abspath(args.puzzle_file)
    assert os.path.exists(abs_puzzle_path),\
        getattr(sys, 'stdout.write', '\nPuzzle file path given doesnt exist\n')

    if args.word_set_file is not None:
        abs_word_set_path = os.path.abspath(args.word_set_file)
        assert os.path.exists(abs_word_set_path),\
            getattr(sys, 'stdout.write', '\nWord set file path given doesnt exist\n')

    if all(word is None for word in (args.word_set_file, args.words)):
        sys.stdout.write("expected [-s [word search set file path]]\n"
                         "or [-w [word to search for [word to search for ...]]]\n")
        sys.exit(1)

    args.words = args.words if args.word_set_file is None else None

    ws = word_search_solver.WordSearchPuzzle(word_search_puzzle=args.puzzle_file,
                                             word_search_set_file=args.word_set_file)
    result = ws.find_words_in_puzzle(args.words)
    ws.get_left_over_letters()

    # print the left over letters in the console
    sys.stdout.write(str(ws.get_left_over_letters()) + "\n")
