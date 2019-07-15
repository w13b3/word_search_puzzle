#!/usr/bin/env python3

import os
import tkinter as tk
from itertools import cycle
from pprint import pprint

import numpy as np
import pandas as pd

# print up to  `given`  rows
pd.options.display.max_rows = 10000


class WordSearchPuzzle:

    def __init__(self, puzzle_file: str, word_list_file: str = None):
        if word_list_file is not None:
            self.create_word_set(word_list_file)

        self.puzzle_df = self._create_puzzle_dataframe(puzzle_file)
        self.position_df = self._create_position_dataframe(self.puzzle_df)

    def _get_puzzle_size(self, puzzle_file: str) -> tuple:
        puzzle_file = os.path.realpath(str(puzzle_file))
        assert os.path.isfile(puzzle_file), "given: %s" % puzzle_file
        with open(puzzle_file, "r") as open_file:
            width = 0
            for height, line in enumerate(open_file, start=1):
                len_line = len(str(line).replace(os.linesep, ""))
                width = len_line if len_line > width else width

            # print("height: %s width: %s" % (height, width))
            return int(width), int(height)

    def _create_empty_dataframe(self, puzzle_file) -> pd.DataFrame:
        """ creates a DataFrame with only empty characters """
        puzzle_file = os.path.realpath(str(puzzle_file))
        assert os.path.isfile(puzzle_file), "given: %s" % puzzle_file

        width, height = self._get_puzzle_size(puzzle_file)  # -> tuple
        max_size = max(width, height)

        return pd.DataFrame([[chr(32) for x in np.arange(max_size)] for y in np.arange(max_size)])  # -> pd.Dataframe

    def _create_puzzle_dataframe(self, puzzle_file) -> pd.DataFrame:
        """ create a square data frame that fits the puzzle """
        puzzle_df = self._create_empty_dataframe(puzzle_file)

        # add the letters onto the dataframe
        with open(puzzle_file, "r") as open_file:
            for y, line in enumerate(open_file):
                line = str(line).replace(os.linesep, "")
                for x, letter in enumerate(line):
                    puzzle_df[x][y] = letter.strip().lower()

        puzzle_df.replace(r'^\s*$', ' ', regex=True, inplace=True)
        return puzzle_df  # -> pd.Dataframe

    def _create_position_dataframe(self, dataframe) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        height, width = dataframe.shape[:2]
        return pd.DataFrame(  # create the frame including the empty characters
            [[(row, column) for row in np.arange(height)] for column in np.arange(width)])

    def create_word_set(self, word_list_file: str) -> set:
        word_list_file = os.path.realpath(str(word_list_file))
        assert os.path.exists(word_list_file), "given: %s" % word_list_file

        word_set = set()
        with open(os.path.realpath(word_list_file), "r") as open_file:
            for line in open_file:
                line = line.replace('\n', '').strip()
                if not line:  # if the length of the line is 0 go to the next word
                    continue
                line = line if ' ' not in line else line.split(' ')
                line = line if ',' not in line else line.split(',')
                line = line if ';' not in line else line.split(';')
                if isinstance(line, list):
                    word_set.update(set(line))
                    continue
                word_set.add(line)
        return word_set  # -> set

    def get_turned_dataframe(self, dataframe, times=1) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        assert isinstance(times, int)
        if int(times) == 0:
            return dataframe
        return pd.DataFrame(data=np.rot90(m=dataframe, k=int(times)))

    def get_diagonal_dataframe(self, dataframe) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        rows = []
        for i in range(-int(dataframe.shape[0] - 1), int(dataframe.shape[1])):
            diagonal_list = np.diagonal(dataframe, offset=i).tolist()
            rows.append(diagonal_list)

        dataframe = pd.DataFrame(data=rows)  # create a dataframe
        dataframe.fillna(value=' ', inplace=True)  # remove NoneType
        dataframe.replace(r'^\s*$', ' ', inplace=True)  # fill blank spaces with single spaces
        return dataframe  # -> pd.DataFrame

    def get_all_posibilities(self, dataframe) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        assert dataframe.shape[0] == dataframe.shape[1]
        deg0    = self.get_turned_dataframe(dataframe, times=0)
        deg90   = self.get_turned_dataframe(dataframe, times=1)
        deg180  = self.get_turned_dataframe(dataframe, times=2)
        deg270  = self.get_turned_dataframe(dataframe, times=3)
        diag0   = self.get_diagonal_dataframe(deg0)
        diag90  = self.get_diagonal_dataframe(deg90)
        diag180 = self.get_diagonal_dataframe(deg180)
        diag270 = self.get_diagonal_dataframe(deg270)
        obj_tuple = (deg0, deg90, deg180, deg270, diag0, diag90, diag180, diag270)
        dataframe = pd.concat(obj_tuple, ignore_index=True)
        dataframe.reset_index(drop=True, inplace=True)  # really necessary!
        return dataframe


if __name__ == '__main__':
    print("start\n")
    # puzzle_file = "woord_easy"
    # puzzle_file = "woordzoeker.txt"
    # puzzle_possibilities = "word_easy_list"
    # puzzle_possibilities = "woordenlijst.txt"

    puzzle_file = "tests/word_puzzle.txt"
    puzzle_possibilities = "tests/word_puzzle_word_list.txt"

    ws = WordSearchPuzzle(puzzle_file)

    # # print the puzzle
    # for row, row_values in ws.puzzle_df.iterrows():
    #     for column, _ in enumerate(row_values):
    #         print(ws.puzzle_df[column][row], end="")
    #     print()

    # pprint(diag_135deg[0][26])

    # # # Word Searching # # #

    # DataFrame[column][row]
    # puzzle_df = ws.get_all_posibilities(ws.puzzle_df)
    # position_df = ws.get_all_posibilities(ws.position_df)

    # # create a list of strings of all the puzzle possibilities
    # list_of_strings = puzzle_df.to_string(
    #     header=False, index=False, sparsify=False).replace(' ', '').split(os.linesep)
    #
    # # find the word in the list of strings
    # findings = []
    # for word in word_set:
    #     # enumerate the line number starting at 0
    #     for line_number, line in enumerate(list_of_strings):
    #         # go to the next line of the length of the line is lower than the length of the word
    #         if len(line) < len(word):
    #             continue
    #
    #         # found -> start position in line; not found -> -1
    #         start_pos = line.find(word)
    #         if start_pos != -1:
    #             end_pos = start_pos + len(word)
    #
    #             # DataFrame[column][row]
    #             positions = position_df.iloc[line_number, start_pos:end_pos]
    #             findings.append((word, tuple(positions)))
    #             continue
    #
    # # # # Tkinter # # #
    #
    # color = cycle(["black", "red", "green", "blue", "cyan", "yellow", "magenta"])
    #
    # height, width = ws.puzzle_df.shape
    # height, width = int(height*25+25), int(width*25+25)
    #
    # root = tk.Tk()
    # root.geometry("%sx%s" % (width, height))
    # canvas = tk.Canvas(root, width=width, height=height)
    #
    # for row, line in ws.puzzle_df.iterrows():
    #     line = line.replace(os.linesep, "")
    #     for column, letter in enumerate(line):
    #         canvas.create_text(int(column * 25 + 25),
    #                            int(row * 25 + 25),
    #                            text=str(letter),
    #                            font="Times 20")
    #
    # def with_space(event, iterator):
    #     # for word, pos in findings:
    #     print("space")
    #     word, pos = next(iterator)    # print(word)
    #     print(word, pos)
    #     min_col = min(p[0] for p in pos) * 25 + 25
    #     max_col = max(p[0] for p in pos) * 25 + 25
    #     min_row = min(p[1] for p in pos) * 25 + 25
    #     max_row = max(p[1] for p in pos) * 25 + 25
    #     canvas.create_line(min_col, min_row,
    #                        max_col, max_row,
    #                        width=2, fill=next(color))
    #     canvas.update()
    #
    # canvas.pack(fill=tk.BOTH)
    # canvas.update()
    # iterator = (i for i in findings)
    # root.bind("<space>", func=lambda x: with_space(x, iterator))
    # root.mainloop()


