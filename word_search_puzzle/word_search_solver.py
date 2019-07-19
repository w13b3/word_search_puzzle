#!/usr/bin/env python3

import os

import numpy as np
import pandas as pd

# print up to  `given`  rows
pd.options.display.max_rows = 10000


class WordSearchPuzzle:
    """ Word search puzzle solver

        word_search_puzzle is required
        file given should look like the puzzle to solve
        this includes any leading, trailing or open spaces
        example:

            foo
            bar
            ate
            zst

        if word_search_set_file given it should contain the words to search for
        example:

            foo
            bar
            baz

        if no word_search_set_file is given
        find_words_in_puzzle needs to be called with a set() containing words to search for

        set of tuple(coordinates) of the found words are returned
        example:

            {((0, 0), (1, 0)  (2, 0)),
             ((0, 1), (1, 1)  (2, 1)),
             ((0, 1), (1, 1)  (1, 2))}

        to show the solution visualize_solution can be called
        this requires tkinter to work
    """

    def __init__(self, word_search_puzzle: str, word_search_set_file: str = None, get_solution: bool = True):
        """
        init

        :param word_search_puzzle:  required - A path to the word search puzzle file
        :param word_search_set_file:  optional - A path to the file containing words to search for
        :param get_solution:  If word_search_set_file is given and this set to True find_words_in_puzzle is called
        """
        self.puzzle_df = self._create_puzzle_dataframe(word_search_puzzle)
        self.position_df = self._create_position_dataframe(self.puzzle_df)

        self.solution_coordinates = None  # set made in find_words_in_puzzle used in visualize_solution

        if word_search_set_file is not None:
            self.word_set = self._create_word_set(word_search_set_file)
            if get_solution:
                self.find_words_in_puzzle()

    def _get_puzzle_size(self, word_search_puzzle: str) -> tuple:
        """
        Get the size of the puzzle
        This is including any leading or trailing spaces

        :param puzzle_file:  A text file containing the puzzle
        :return tuple:  width and height of the puzzle
        """
        word_search_puzzle = os.path.realpath(str(word_search_puzzle))
        assert os.path.isfile(word_search_puzzle), 'given: %s' % word_search_puzzle

        with open(word_search_puzzle, 'r') as open_file:
            width, height = 0, 0
            for height, line in enumerate(open_file, start=1):
                len_line = len(str(line).replace('\n', ''))
                width = len_line if len_line > width else width

            return int(width), int(height)

    def _create_empty_dataframe(self, word_search_puzzle: str) -> pd.DataFrame:
        """
        Create an DataFrame containing only spaces

        :param puzzle_file:  A text file containing the puzzle
        :return pandas.DataFrame:  An empty DataFrame containing only spaces in the size of the puzzle
        """
        word_search_puzzle = os.path.realpath(str(word_search_puzzle))
        assert os.path.isfile(word_search_puzzle), 'given: %s' % word_search_puzzle

        width, height = self._get_puzzle_size(word_search_puzzle)  # -> tuple
        max_size = max(width, height)
        dataframe = pd.DataFrame([[chr(32) for x in np.arange(max_size)] for y in np.arange(max_size)])
        return dataframe  # -> pd.Dataframe

    def _create_puzzle_dataframe(self, word_search_puzzle: str) -> pd.DataFrame:
        """
        Create a DataFrame containing the letters and spaces of the puzzle file

        :param puzzle_file:  A text file containing the puzzle
        :return pandas.DataFrame:  A DataFrame containing the puzzle
        """
        word_search_puzzle = os.path.realpath(str(word_search_puzzle))
        assert os.path.isfile(word_search_puzzle), 'given: %s' % word_search_puzzle

        puzzle_df = self._create_empty_dataframe(word_search_puzzle)

        # add the letters onto the DataFrame
        with open(word_search_puzzle, 'r') as open_file:
            for y, line in enumerate(open_file):
                line = str(line).replace('\n', '')
                for x, letter in enumerate(line):
                    puzzle_df[x][y] = letter.strip().lower()

        puzzle_df.replace(r'^\s*$', ' ', regex=True, inplace=True)
        return puzzle_df  # -> pd.Dataframe

    def _create_word_set(self, word_search_set_file: str) -> set:
        """
        Create a set out of the file of words given.
        The file of words should be seperated by new-lines, spaces, comma's or semicolons.

        :param word_list_file:  A file containing the set of words to seek in the puzzle
        :return set:  A set of words from the file
        """
        word_search_set_file = os.path.realpath(str(word_search_set_file))
        assert os.path.exists(word_search_set_file), 'given: %s' % word_search_set_file

        word_set = set()
        with open(word_search_set_file, 'r') as open_file:
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

    def _create_position_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Create a DataFrame containing the coordinates in tuples of the frame

        :param dataframe: A DataFrame of the puzzle
        :return pandas.DataFrame: A DataFrame containing the coordinate of the frame
        """
        assert isinstance(dataframe, pd.DataFrame)
        height, width = dataframe.shape[:2]
        position_df = pd.DataFrame(  # create the frame including the empty characters
            [[(row, column) for row in np.arange(height)] for column in np.arange(width)])
        return position_df  # -> pd.Dataframe

    def get_turned_dataframe(self, dataframe: pd.DataFrame, times: int = 1) -> pd.DataFrame:
        """
        Get a turned DataFrame from the given DataFrame
        The rotation is in 90degrees clockwise per turn.

        :param dataframe:  A DataFrame of the puzzle
        :param times:  How many times the puzzle needs to be turned
        :return pandas.DataFrame:  A turned DataFrame of the puzzle
        """
        assert isinstance(dataframe, pd.DataFrame)
        assert isinstance(times, int)

        if int(times) <= 0:
            return dataframe
        turned_frame = pd.DataFrame(data=np.rot90(m=dataframe, k=int(times)))

        return turned_frame  # -> pd.DataFrame

    def get_diagonal_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Get a DataFrame that is diagonal with respect to the given DataFrame
        The given DataFrame is `read` from the bottom left to the top right
        This is projected to another DataFrame

        :param dataframe:  A DataFrame of the puzzle
        :return pandas.DataFrame:  The diagonally projected DataFrame
        """
        assert isinstance(dataframe, pd.DataFrame)

        rows = []
        for i in range(-int(dataframe.shape[0] - 1), int(dataframe.shape[1])):
            diagonal_list = np.diagonal(dataframe, offset=i).tolist()
            rows.append(diagonal_list)

        dataframe = pd.DataFrame(data=rows)  # create a dataframe
        dataframe.fillna(value=' ', inplace=True)  # remove NoneType
        dataframe.replace(r'^\s*$', ' ', inplace=True)  # fill blank spaces with single spaces

        return dataframe  # -> pd.DataFrame

    def get_all_possibilities(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        This creates all angles of the DataFrame and concatenate those to one DataFrame

        :param dataframe:  A DataFrame of the puzzle
        :return pandas.DataFrame:  A concatenated DataFrame of all the angles of the given DataFrame
        """
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

        return dataframe  # -> pd.DataFrame

    def find_word_with_coordinates(self, dataframe: pd.DataFrame, coordinates: pd.Series) -> str:
        """
        This wil find the word in the given DataFrame with the given coordinates

        :param dataframe:  A DataFrame of the puzzle
        :param coordinates:  A pandas.Series of a tuple containing (x, y) coordinates
        :return str:  The word found in the puzzle by the given coordinates
        """
        if isinstance(coordinates, tuple):
            coordinates = pd.Series(coordinates)
        assert isinstance(dataframe, pd.DataFrame)
        assert isinstance(coordinates, pd.Series)
        assert all(2 == len(c) for c in coordinates)

        # each coordinate: (column, row)
        # should represent a coordinate on the puzzle DataFrame
        # all the coordinates should spell out a word
        word = ''
        try:
            word_list = [dataframe[column][row] for column, row in coordinates]
        except KeyError as e:
            print('KeyError: value %s of range' % e)
        else:
            word = ''.join(word_list)
        finally:
            return word  # -> str

    def find_words_in_puzzle(self, word_set: set = None, min_length: int = 0) -> set:
        """
        Finds the words in the puzzle and returns its coordinates

        :param word_set:  A set('words', ...) to find in the
                          If None is given the word_search_set_file will be chosen
        :param min_length:  minimal length of the word to search for
        :return set:  A set of coordinates that correspond with letters of the found words in the puzzle
        """
        assert word_set or self.word_set, 'needs a set of words to search for'

        if word_set is not None:
            assert type(word_set) in [set, list, tuple]
            assert all(str == type(word) for word in set(word_set))
        else:
            word_set = self.word_set

        assert type(min_length) in [int, tuple]
        min_length = int(min_length) if int(min_length) >= 0 else 0  # negative numbers becomes 0

        combined_puzzle_df = self.get_all_possibilities(self.puzzle_df)
        combined_position_df = self.get_all_possibilities(self.position_df)

        # make a list of strings
        # a list that keeps the empty spaces that might be in the DataFrame
        list_of_strings = [''.join(row.to_list()) for _, row in combined_puzzle_df.iterrows()]

        found_word_positions_set = set()
        for word in word_set:
            # if the word is smaller than the given minimal length continue to the next word
            # or the word is a False == ''
            if len(word) < min_length or not bool(word):
                continue

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
                found = bool(found_word == word)  # sets found to True if words match

                if found:  # if the word matches, add the tuple of coordinates to the set
                    found_word_positions_set.add(tuple(coordinates))

            if not found:
                print('%s is not found' % word)

        self.solution_coordinates = found_word_positions_set
        return found_word_positions_set  # -> set

    def get_left_over_coordinates(self) -> pd.Series:
        """

        :return str: letters that are left over if the puzzle's solution is found.
        """
        if self.solution_coordinates is None:
            self.find_words_in_puzzle()

        position_df = self.position_df.copy()  # save the original
        for coordinates in self.solution_coordinates:
            for column, row in coordinates:
                position_df[column][row] = ''

        left_over = pd.Series(pos for _, row in position_df.iterrows() for pos in row if pos)
        return left_over

    def get_left_over_letters(self) -> str:
        left_over = self.get_left_over_coordinates()
        letters = self.find_word_with_coordinates(self.puzzle_df, left_over)
        return letters.replace(' ', '')


    def visualize_solution(self):
        """
        Visualize the solution of the found words in the puzzle
        Opens an tkinter window with a representation of the given puzzle
        In the window words found are crossed in different colors
        """
        assert self.solution_coordinates is not None

        from itertools import cycle
        try:
            import tkinter as tk
        except ImportError:
            # Linux: sudo apt install python-tk
            print("Tkinter is needed for visualization")
            exit(1)

        color_cycle = cycle(['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta'])

        height, width = self.puzzle_df.shape
        height, width = int(height * 25 + 25), int(width * 25 + 25)

        root = tk.Tk()
        root.title("Solution")
        root.geometry('%sx%s' % (width, height))
        canvas = tk.Canvas(root, width=width, height=height)

        for row, line in self.puzzle_df.iterrows():
            line = line.replace('\n', '')
            for column, letter in enumerate(line):
                canvas.create_text(int(column * 25 + 25), int(row * 25 + 25), text=str(letter), font='Times 20')

        canvas.pack(fill=tk.BOTH)
        canvas.update()

        for coordinates in self.solution_coordinates:
            prev_column, prev_row = None, None
            color = next(color_cycle)
            for column, row in coordinates:
                column = column * 25 + 25
                row = row * 25 + 25
                if prev_column is None and prev_row is None:
                    prev_column, prev_row = column, row
                    continue
                else:
                    canvas.create_line(prev_column, prev_row, column, row, width=5, fill=color)
                    prev_column, prev_row = column, row

        root.mainloop()


if __name__ == '__main__':
    print('start\n')

    # puzzle_file = r'../puzzles/apple_word_search_puzzle.txt'
    # puzzle_possibilities = r'../puzzles/apple_word_search_set.txt'

    puzzle_file = r'../puzzles/baseball_word_search_puzzle.txt'
    puzzle_possibilities = r'../puzzles/baseball_word_search_set.txt'

    # puzzle_file = r'../puzzles/housing_word_search_puzzle.txt'
    # puzzle_possibilities = r'../puzzles/housing_word_search_set.txt'

    ws = WordSearchPuzzle(puzzle_file, puzzle_possibilities)
    # ws.visualize_solution()
    print(ws.get_left_over_letters())
