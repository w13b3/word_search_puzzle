#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call

import pandas as pd
from pandas.util.testing import assert_frame_equal

from main.word_search_solver import WordSearchPuzzle


class WordSearchPuzzleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.word_search_puzzle = r"puzzles/test_word_search_puzzle.txt"
        cls.word_search_set = r"puzzles/test_word_search_set.txt"

        # initiate the class for the whole test
        cls.ws = WordSearchPuzzle(cls.word_search_puzzle, cls.word_search_set)

    def test_get_puzzle_size(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._get_puzzle_size('/not/a/path.txt')

        # Return a tuple
        result = self.ws._get_puzzle_size(self.word_search_puzzle)  # -> (14, 14)
        self.assertIs(type(result), tuple)

        width, height = result
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

    def test_create_empty_dataframe(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._create_empty_dataframe('/not/a/path.txt')

        # create a DataFrame
        result = self.ws._create_empty_dataframe(self.word_search_puzzle)
        self.assertIs(type(result), pd.DataFrame)

        # DataFrame should have the size of the puzzle
        width, height = result.shape[:2]
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

        for index, row in result.iterrows():
            for cell in row:
                # every cell should contain a space character
                self.assertEqual(cell, chr(32), 'DataFrame cell should contain a "space" character')

    def test_create_puzzle_dataframe(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._get_puzzle_size('/not/a/path.txt')

        # create a DataFrame
        result = self.ws._create_puzzle_dataframe(self.word_search_puzzle)
        self.assertIs(type(result), pd.DataFrame)

        # DataFrame should have the size of the puzzle
        width, height = result.shape[:2]
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

        # comprehension list creates 2d-list of the puzzle file
        with open(self.word_search_puzzle) as file:
            puzzle_file = file.readline()
            line_2d_list = [[letter for letter in line] for line in puzzle_file.split('\n') if line]

        for line_list, (index, row) in zip(line_2d_list, result.iterrows()):
            # line and row should be the same
            self.assertEqual(line_list, row.tolist())
            for line_letter, row_letter in zip(line_list, row):
                # checking if the letter on the line and the letter on the row is the same
                self.assertEqual(line_letter, row_letter)

    def test_create_position_dataframe(self):

        # should get an error when an invalid object is given
        with self.assertRaises(AssertionError):
            self.ws._create_position_dataframe('puzzle_df')

        # create a DataFrame
        result = self.ws._create_position_dataframe(self.ws.puzzle_df)
        self.assertIs(type(result), pd.DataFrame)

        # DataFrame should have the size of the puzzle
        width, height = result.shape[:2]
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

        # comprehension list creates 2d-list of the puzzle file
        with open(self.word_search_puzzle) as file:
            puzzle_file = file.readline()
            pos_2d_list = [[(x, y) for x, _ in enumerate(_)] for y, _ in enumerate(puzzle_file.split('\n')) if _]

        for pos_list, (index, row) in zip(pos_2d_list, result.iterrows()):
            # pos_list and row should be the same
            self.assertEqual(pos_list, row.tolist())
            for list_pos, row_pos in zip(pos_list, row):
                # checking if the position on the row is a tuple
                self.assertIs(type(row_pos), tuple)
                # checking if the position on the row is indeed made up of an (x, y) formation
                self.assertEqual(list_pos, row_pos)

    def test_create_word_set(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._create_word_set('/not/a/path.txt')

        with open(self.word_search_set) as file:
            lenght_file = len(file.readlines())

        # create a set
        result = self.ws._create_word_set(self.word_search_set)
        self.assertIs(type(result), set)

        # 33 words are given in the word_search_list
        # len(word_search_list) == 28
        # method should parse the different data correctly
        self.assertGreater(len(result), lenght_file)
        self.assertEqual(35, len(result))

    def test_get_turned_DataFrame(self):

        # should get an error when an invalid type is given to DataFrame
        with self.assertRaises(AssertionError):
            self.ws.get_turned_dataframe(dataframe='dataframe', times=2)

        # should get an error when an invalid type is given to times
        with self.assertRaises(AssertionError):
            self.ws.get_turned_dataframe(dataframe=pd.DataFrame, times='2')

        # get data to test
        # DataFrame[column][row]
        dataframe = self.ws.puzzle_df.copy()
        top_right = dataframe[13][0]    # -> '+'
        bottom_left = dataframe[0][13]  # -> '-'

        # DataFrame turns counter clockwise, so 0 -> 90 -> 180 -> 270 -> 360
        dataframe_0deg = self.ws.get_turned_dataframe(dataframe, times=0)
        dataframe_90deg = self.ws.get_turned_dataframe(dataframe, times=1)
        dataframe_180deg = self.ws.get_turned_dataframe(dataframe, times=2)
        dataframe_270deg = self.ws.get_turned_dataframe(dataframe, times=3)
        dataframe_360deg = self.ws.get_turned_dataframe(dataframe, times=4)

        # should return a pandas.DataFrame
        self.assertIs(type(dataframe_0deg), pd.DataFrame)
        self.assertIs(type(dataframe_90deg), pd.DataFrame)
        self.assertIs(type(dataframe_180deg), pd.DataFrame)
        self.assertIs(type(dataframe_270deg), pd.DataFrame)
        self.assertIs(type(dataframe_360deg), pd.DataFrame)

        # test the data
        self.assertIsNone(assert_frame_equal(dataframe, dataframe_0deg))  # times=0
        self.assertIsNone(assert_frame_equal(dataframe, dataframe_360deg))  # times=4

        self.assertEqual(top_right, dataframe_0deg[13][0])      # -> '+'
        self.assertEqual(bottom_left, dataframe_0deg[0][13])    # -> '-'

        self.assertEqual(top_right, dataframe_360deg[13][0])    # -> '+'
        self.assertEqual(bottom_left, dataframe_360deg[0][13])  # -> '-'

        self.assertEqual(top_right, dataframe_90deg[0][0])      # -> '+'
        self.assertEqual(bottom_left, dataframe_90deg[13][13])  # -> '-'

        self.assertEqual(top_right, dataframe_180deg[0][13])    # -> '+'
        self.assertEqual(bottom_left, dataframe_180deg[13][0])  # -> '-'

        self.assertEqual(top_right, dataframe_270deg[13][13])   # -> '+'
        self.assertEqual(bottom_left, dataframe_270deg[0][0])   # -> '-'

    def test_get_diagonal_dataframe(self):

        # should get an error when an invalid type is given to DataFrame
        with self.assertRaises(AssertionError):
            self.ws.get_diagonal_dataframe(dataframe='dataframe')

        # get data to test
        # DataFrame[column][row]
        dataframe = self.ws.puzzle_df.copy()
        top_right = dataframe[13][0]      # -> '+'
        top_left = dataframe[0][0]        # -> 'a'
        bottom_left = dataframe[0][13]    # -> '-'
        bottom_right = dataframe[13][13]  # -> 'z'

        dataframe_0deg = self.ws.get_turned_dataframe(dataframe, times=0)
        dataframe_90deg = self.ws.get_turned_dataframe(dataframe, times=1)
        dataframe_180deg = self.ws.get_turned_dataframe(dataframe, times=2)
        dataframe_270deg = self.ws.get_turned_dataframe(dataframe, times=3)
        # dataframe_360deg = self.ws.get_turned_dataframe(dataframe, times=4)

        # assuming 0/360 degrees is facing north
        dataframe_315deg = self.ws.get_diagonal_dataframe(dataframe_0deg)
        dataframe_45deg = self.ws.get_diagonal_dataframe(dataframe_90deg)
        dataframe_135deg = self.ws.get_diagonal_dataframe(dataframe_180deg)
        dataframe_225deg = self.ws.get_diagonal_dataframe(dataframe_270deg)

        # should return a pandas.DataFrame
        self.assertIs(type(dataframe_315deg), pd.DataFrame)
        self.assertIs(type(dataframe_45deg), pd.DataFrame)
        self.assertIs(type(dataframe_135deg), pd.DataFrame)
        self.assertIs(type(dataframe_225deg), pd.DataFrame)

        # face 0deg, slice at 315deg (bottom left to top right)
        self.assertEqual(bottom_left, dataframe_315deg[0][0])     # -> '-'
        self.assertEqual(top_left, dataframe_315deg[0][13])       # -> 'a'
        self.assertEqual(bottom_right, dataframe_315deg[13][13])  # -> 'z'
        self.assertEqual(top_right, dataframe_315deg[0][26])      # -> '+'

        # face at 90deg, slice at 45deg (bottom left to top right)
        self.assertEqual(top_left, dataframe_45deg[0][0])         # -> 'a'
        self.assertEqual(top_right, dataframe_45deg[0][13])       # -> '+'
        self.assertEqual(bottom_left, dataframe_45deg[13][13])    # -> '-'
        self.assertEqual(bottom_right, dataframe_45deg[0][26])    # -> 'z'

        # face at 180deg, slice at 135deg (bottom left to top right)
        self.assertEqual(top_right, dataframe_135deg[0][0])       # -> '+'
        self.assertEqual(bottom_right, dataframe_135deg[0][13])   # -> 'z'
        self.assertEqual(top_left, dataframe_135deg[13][13])      # -> 'a'
        self.assertEqual(bottom_left, dataframe_135deg[0][26])    # -> '-'

        # face at 270deg, slice at 225deg (bottom left to top right)
        self.assertEqual(bottom_right, dataframe_225deg[0][0])    # -> 'z'
        self.assertEqual(bottom_left, dataframe_225deg[0][13])    # -> '-'
        self.assertEqual(top_right, dataframe_225deg[13][13])     # -> '+'
        self.assertEqual(top_left, dataframe_225deg[0][26])       # -> 'a'

    def test_get_all_posibilities(self):

        # should get an error when an invalid type is given to dataframe
        with self.assertRaises(AssertionError):
            self.ws.get_all_possibilities(dataframe='dataframe')

        dataframe = self.ws.puzzle_df.copy()
        result = self.ws.get_all_possibilities(dataframe=dataframe)

        # should return a pandas.DataFrame
        self.assertIs(type(result), pd.DataFrame)

        height, width = result.shape

        # 0deg, 90deg, 180deg, 270deg -> height 14
        # 45deg, 135deg, 225deg, 315deg - height 27 ( height + width - 1 )
        # combined = 8 DataFrame's
        # 4 * 14(height) + 4 * 27 =  164
        # the total of rows of the result should be 164
        # the total of columns should be 14

        self.assertEqual(width, 14)    # total columns
        self.assertEqual(height, 164)  # total rows

    def test_dataframe_letter_position_pair(self):

        dataframe = self.ws.puzzle_df.copy()
        positionframe = self.ws.position_df.copy()

        data_height, data_width = dataframe.shape
        pos_height, pos_width = positionframe.shape

        self.assertEqual(pos_height, data_height)  # 14 == 14
        self.assertEqual(pos_width, data_width)  # 14 == 14

        combined_data = self.ws.get_all_possibilities(dataframe)
        combined_positions = self.ws.get_all_possibilities(positionframe)

        data_height, data_width = combined_data.shape
        pos_height, pos_width = combined_positions.shape

        self.assertEqual(pos_height, data_height)  # 164 == 164
        self.assertEqual(pos_width, data_width)  # 14 == 14

        # assuming the combined_data and the combined_positions are made the same
        # the position of certain letter could be traced back to the original puzzle_df
        #
        # example:
        # combined_data[column 3][row 101] -> 's'
        #   L-> combined_positions[column 3][row 101] -> (4, 6)
        #       L-> puzzle_df[column 4][row 6] -> 's'

        for row, row_values in combined_data.iterrows():  # row: int
            for column, _ in enumerate(row_values):       # column: int

                letter = combined_data[column][row]  # letter of combined
                self.assertIs(type(letter), str)
                if len(letter.strip()) == 0:
                    continue

                position = combined_positions[column][row]  # position of combined
                self.assertIs(type(position), tuple)
                pos_x, pos_y = position

                puzzle_letter = self.ws.puzzle_df[pos_x][pos_y]  # letter of position
                self.assertIs(type(puzzle_letter), str)
                self.assertEqual(letter, puzzle_letter)
                # print(f'{letter} == {puzzle_letter} puzzle coordinates: {position}')

    def test_find_word_with_coordinates(self):

        dataframe = self.ws.puzzle_df.copy()

        # should get an error when an invalid type is given to DataFrame
        with self.assertRaises(AssertionError):
            self.ws.find_word_with_coordinates(dataframe='dataframe', coordinates=pd.Series())

        # should get an error when an invalid type is given to coordinates
        with self.assertRaises(AssertionError):
            self.ws.find_word_with_coordinates(dataframe=pd.DataFrame(), coordinates='coordinates')

        # should get an error when an invalid series of coordinates is given to coordinates
        with self.assertRaises(AssertionError):
            wrond_data = pd.Series(((0, 1), (2, 3), (4, 5, 6)))  # coordinates are not all of lenght: 2
            self.ws.find_word_with_coordinates(dataframe=pd.DataFrame(), coordinates=wrond_data)

        # should get an error when an invalid series of coordinates is given to coordinates
        with self.assertRaises(AssertionError):
            wrond_data = pd.Series(((1, ), (2, 3), (4, 5)))  # coordinates are not all of lenght: 2
            self.ws.find_word_with_coordinates(dataframe=pd.DataFrame(), coordinates=wrond_data)

        # should return None if the given value is out of range of the puzzle DataFrame
        with unittest.mock.patch('builtins.print') as mocked_print:
            diagonal = pd.Series(((0, 0), (99, 99)))
            result = self.ws.find_word_with_coordinates(dataframe, diagonal)
            self.assertFalse(result)
            self.assertIn(call('KeyError: value 99 of range'), mocked_print.mock_calls)

        diagonal = pd.Series(((3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (9, 6), (10, 7)))
        result = self.ws.find_word_with_coordinates(dataframe, diagonal)
        self.assertEqual(result, 'diagonal')

        wrong = pd.Series(((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)))
        result = self.ws.find_word_with_coordinates(dataframe, wrong)
        self.assertNotEqual(result, 'diagonal')

    def test_find_words_in_puzzle(self):

        # if a search_list is not given to the class instance
        # and a word_set is not given to the method
        # assetion error should occur
        copy = self.ws.word_set.copy()  # create a copy of the word_set
        with self.assertRaises(AssertionError):
            self.ws.word_set = None  # set the current word_set to None
            self.ws.find_words_in_puzzle()  # check if assertion happens

        self.ws.word_set = copy  # replace the word_set its old value

        # method only takes: set, list or tuple
        self.assertRaises(AssertionError, self.ws.find_words_in_puzzle, str())
        self.assertRaises(AssertionError, self.ws.find_words_in_puzzle, int())
        self.assertRaises(AssertionError, self.ws.find_words_in_puzzle, float())
        self.assertRaises(AssertionError, self.ws.find_words_in_puzzle, dict())

        # only strings should be in the given set
        with self.assertRaises(AssertionError):
            wrong_set = {"str", 1, 1.2}
            self.ws.find_words_in_puzzle(wrong_set)

        # given minimum length should be either a tuple or an int
        self.assertRaises(AssertionError, self.ws.find_words_in_puzzle, set(), "str")

        # test if words are found
        # and the returned set contains tuples
        # and if 'not_found' is not found
        with unittest.mock.patch('builtins.print') as mocked_print:
            result = self.ws.find_words_in_puzzle()
            self.assertIs(type(result), set)
            self.assertGreater(len(result), 0)
            self.assertIs(type(result.pop()), tuple)
            self.assertIn(call('not_found is not found'), mocked_print.mock_calls)


if __name__ == '__main__':
    unittest.main()
