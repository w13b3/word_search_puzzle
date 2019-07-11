#!/usr/bin/env python3

import os
import tkinter as tk
from itertools import cycle

import numpy as np
import pandas as pd


class WordSearchPuzzle:

    def __init__(self, puzzle_file: str, word_list_file: str = None):
        assert os.path.isfile(str(puzzle_file))
        if word_list_file is not None:
            assert os.path.exists(str(word_list_file))

        self.puzzle_df = self.__create_puzzle_dataframe(puzzle_file)
        self.position_df = self.__create_position_dataframe(self.puzzle_df)

    def __get_puzzle_size(self, puzzle_file: str) -> tuple:
        with open(puzzle_file, "r") as open_file:
            width = 0
            for height, line in enumerate(open_file, start=1):
                len_line = len(str(line).replace(os.linesep, ""))
                width = len_line if len_line > width else width

            # print("height: %s width: %s" % (height, width))
            return int(width), int(height)

    def __create_puzzle_dataframe(self, puzzle_file) -> pd.DataFrame:
        """ create a square data frame that fits the puzzle """
        width, height = self.__get_puzzle_size(puzzle_file)
        max_size = max(width, height)
        puzzle_df = pd.DataFrame(  # create the frame including the empty characters
            [[" " for x in np.arange(max_size)] for y in np.arange(max_size)])

        # add the letters onto the dataframe
        with open(puzzle_file, "r") as open_file:
            for y, line in enumerate(open_file):
                line = str(line).replace(os.linesep, "")
                for x, letter in enumerate(line):
                    puzzle_df[x][y] = letter.strip().lower()

        puzzle_df.replace(r'^\s*$', ' ', regex=True, inplace=True)
        return puzzle_df  # -> pd.Dataframe

    def __create_position_dataframe(self, dataframe) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        height, width = dataframe.shape[:2]
        return pd.DataFrame(  # create the frame including the empty characters
            [[(row, column) for row in np.arange(height)] for column in np.arange(width)])

    def create_word_set(self, word_file: str) -> set:
        word_set = set()
        with open(word_file, "r") as open_file:
            for line in open_file:
                line = line.strip().replace(os.linesep, "")
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
        dataframe = pd.concat(obj_tuple)
        dataframe.reset_index(drop=True, inplace=True)  # really necessary!
        return dataframe


if __name__ == '__main__':
    print("start\n")
    puzzle_file = "woordzoeker.txt"
    puzzle_possibilities = "woordenlijst.txt"

    ws = WordSearchPuzzle(puzzle_file)
    word_set = ws.create_word_set(puzzle_possibilities)

    # # # Word Searching # # #

    # DataFrame[column][row]
    puzzle_df = ws.get_all_posibilities(ws.puzzle_df)
    position_df = ws.get_all_posibilities(ws.position_df)

    # create a list of strings of all the puzzle possibilities
    list_of_strings = puzzle_df.to_string(
        header=False, index=False, sparsify=False).replace(' ', '').split(os.linesep)

    # find the word in the list of strings
    findings = []
    for word in word_set:
        # enumerate the line number starting at 0
        for line_number, line in enumerate(list_of_strings):
            # go to the next line of the length of the line is lower than the length of the word
            if len(line) < len(word):
                continue

            # found -> start position in line; not found -> -1
            start_pos = line.find(word)
            if start_pos != -1:
                end_pos = start_pos + len(word)

                # DataFrame[column][row]
                positions = position_df.iloc[line_number, start_pos:end_pos]
                findings.append((word, tuple(positions)))
                continue

    # # # Tkinter # # #

    color = cycle(["black", "red", "green", "blue", "cyan", "yellow", "magenta"])

    height, width = ws.puzzle_df.shape
    height, width = int(height*25+25), int(width*25+25)

    root = tk.Tk()
    root.geometry("%sx%s" % (width, height))
    canvas = tk.Canvas(root, width=width, height=height)

    for row, line in ws.puzzle_df.iterrows():
        line = line.replace(os.linesep, "")
        for column, letter in enumerate(line):
            canvas.create_text(int(column * 25 + 25),
                               int(row * 25 + 25),
                               text=str(letter),
                               font="Times 20")

    for word, pos in findings:
        # print(word)
        min_col = min(p[0] for p in pos) * 25 + 25
        max_col = max(p[0] for p in pos) * 25 + 25
        min_row = min(p[1] for p in pos) * 25 + 25
        max_row = max(p[1] for p in pos) * 25 + 25
        canvas.create_line(min_col, min_row,
                           max_col, max_row,
                           width=2, fill=next(color))

    canvas.pack(fill=tk.BOTH)
    canvas.update()

    root.mainloop()


