#!/usr/bin/env python3

import os
import tkinter as tk
from itertools import cycle

import numpy as np
import pandas as pd

# print up to  `given`  rows
pd.options.display.max_rows = 10000


class WordSearchPuzzle:

    def __init__(self, puzzle_file: str, word_list_file: str = None):
        if word_list_file is not None:
            self.word_set = self.create_word_set(word_list_file)

        self.puzzle_df = self._create_puzzle_dataframe(puzzle_file)
        self.position_df = self._create_position_dataframe(self.puzzle_df)

    def _get_puzzle_size(self, puzzle_file: str) -> tuple:
        puzzle_file = os.path.realpath(str(puzzle_file))
        assert os.path.isfile(puzzle_file), 'given: %s' % puzzle_file

        with open(puzzle_file, 'r') as open_file:
            width, height = 0, 0
            for height, line in enumerate(open_file, start=1):
                len_line = len(str(line).replace('\n', ''))
                width = len_line if len_line > width else width

            return int(width), int(height)

    def _create_empty_dataframe(self, puzzle_file) -> pd.DataFrame:
        """ creates a DataFrame with only empty characters """
        puzzle_file = os.path.realpath(str(puzzle_file))
        assert os.path.isfile(puzzle_file), 'given: %s' % puzzle_file

        width, height = self._get_puzzle_size(puzzle_file)  # -> tuple
        max_size = max(width, height)
        dataframe = pd.DataFrame([[chr(32) for x in np.arange(max_size)] for y in np.arange(max_size)])
        return dataframe  # -> pd.Dataframe

    def _create_puzzle_dataframe(self, puzzle_file) -> pd.DataFrame:
        """ create a square data frame that fits the puzzle """
        puzzle_df = self._create_empty_dataframe(puzzle_file)

        # add the letters onto the DataFrame
        with open(puzzle_file, 'r') as open_file:
            for y, line in enumerate(open_file):
                line = str(line).replace('\n', '')
                for x, letter in enumerate(line):
                    puzzle_df[x][y] = letter.strip().lower()

        puzzle_df.replace(r'^\s*$', ' ', regex=True, inplace=True)
        return puzzle_df  # -> pd.Dataframe

    def _create_position_dataframe(self, dataframe) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        height, width = dataframe.shape[:2]
        position_df = pd.DataFrame(  # create the frame including the empty characters
            [[(row, column) for row in np.arange(height)] for column in np.arange(width)])
        return position_df  # -> pd.Dataframe

    def create_word_set(self, word_list_file: str) -> set:
        word_list_file = os.path.realpath(str(word_list_file))
        assert os.path.exists(word_list_file), 'given: %s' % word_list_file

        word_set = set()
        with open(os.path.realpath(word_list_file), 'r') as open_file:
            for line in open_file:
                line = line.replace('\n', '').strip()
                if not line:  # if the length of the line is 0 go to the next word
                    continue
                line = line if ' ' not in line else line.split(' ')
                line = line if ',' not in line else line.split(',')
                line = line if ';' not in line else line.split(';')
                if isinstance(line, list):
                    line_list = [word.strip() for word in line]
                    word_set.update(set(line_list))
                    continue
                word_set.add(line.strip())
        return word_set  # -> set

    def get_turned_dataframe(self, dataframe, times=1) -> pd.DataFrame:
        assert isinstance(dataframe, pd.DataFrame)
        assert isinstance(times, int)

        if int(times) == 0:
            return dataframe
        turned_frame = pd.DataFrame(data=np.rot90(m=dataframe, k=int(times)))

        return turned_frame  # -> pd.DataFrame

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

    def find_word_with_coordinates(self, dataframe: pd.DataFrame, coordinates: pd.Series) -> str:
        if isinstance(coordinates, tuple):
            coordinates = pd.Series(coordinates)
        assert isinstance(dataframe, pd.DataFrame)
        assert isinstance(coordinates, pd.Series)
        assert all(2 == len(c) for c in coordinates)

        # each coordinate: (column, row)
        # should represent a coordinate on the puzzle DataFrame
        # all the coordinates should spell out a word
        word = None
        try:
            word_list = [dataframe[column][row] for column, row in coordinates]
        except KeyError as e:
            print('KeyError: value %s of range' % e)
        else:
            word = ''.join(word_list)
        finally:
            return word

    def find_words_in_puzzle(self, word_set: set = None) -> set:
        assert word_set or self.word_set, 'needs a set of words to search for'

        if word_set is not None:
            assert type(word_set) in [set, list, tuple]
            assert all(str == type(word) for word in set(word_set))
        else:
            word_set = self.word_set

        combined_puzzle_df = ws.get_all_posibilities(self.puzzle_df)
        combined_position_df = ws.get_all_posibilities(self.position_df)

        # create a list of strings of all the puzzle possibilities
        list_of_strings = combined_puzzle_df.to_string(
            header=False, index=False, sparsify=False).replace(' ', '').split('\n')

        print(list_of_strings)

        found_word_positions_set = set()
        for word in word_set:
            found = False

            for line_number, string in enumerate(list_of_strings):
                try:  # find the word in the string and return the 1st letter
                    start_pos = string.index(word)
                except ValueError:  # word not found in string
                    continue
                # get the end pos of the list where the word should be located
                end_pos = start_pos + len(word)

                # get the coordinates in the positions DataFrame of the word in the puzzle DataFrame
                coordinates = combined_position_df.iloc[line_number, start_pos:end_pos]

                # check if the found word in the puzzle DataFrame matches the word that was searched
                found_word = self.find_word_with_coordinates(self.puzzle_df, coordinates)
                found = bool(found_word == word)

                if found:  # if the word matches, add the tuple of coordinates to the set
                    found_word_positions_set.add(tuple(coordinates))

                # print(f"it's {found}, {word} is found")

            if not found:
                print('%s is not found' % word)

        return found_word_positions_set  # -> set


if __name__ == '__main__':
    print('start\n')
    puzzle_file = r'..\puzzles\apple_word_search_puzzle.txt'
    puzzle_possibilities = r'..\puzzles\apple_word_search_set.txt'
    ws = WordSearchPuzzle(puzzle_file, puzzle_possibilities)
    word_set = ws.word_set
    # DataFrame[column][row]
    puzzle_df = ws.get_all_posibilities(ws.puzzle_df)
    position_df = ws.get_all_posibilities(ws.position_df)

    coordinate_set = ws.find_words_in_puzzle()

    # # # Tkinter # # #

    color_cycle = cycle(['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta'])

    height, width = ws.puzzle_df.shape
    height, width = int(height*25+25), int(width*25+25)

    root = tk.Tk()
    root.geometry('%sx%s' % (width, height))
    canvas = tk.Canvas(root, width=width, height=height)

    for row, line in ws.puzzle_df.iterrows():
        line = line.replace('\n', '')
        for column, letter in enumerate(line):
            canvas.create_text(int(column * 25 + 25),
                               int(row * 25 + 25),
                               text=str(letter),
                               font='Times 20')

    canvas.pack(fill=tk.BOTH)
    canvas.update()
    iterator = (i for i in coordinate_set)
    for coordinates in coordinate_set:
        prev_column, prev_row = None, None
        color = next(color_cycle)
        for column, row in coordinates:
            column = column * 25 + 25
            row = row * 25 + 25
            if prev_column is None and prev_row is None:
                prev_column, prev_row = column, row
                continue
            else:
                canvas.create_line(prev_column, prev_row, column, row,
                                   width=2, fill=color)
                column1, row1 = column, row

    root.mainloop()
