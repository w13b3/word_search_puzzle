#!/usr/bin/env python3

import os
import unittest
from tempfile import NamedTemporaryFile

import pandas as pd
from pandas.util.testing import assert_frame_equal

from word_search_solver import WordSearchPuzzle

word_search_list = [
    'abcdefghijklm;nopqrstuvwxyz', '\n', 'eazy,welcome,aan', 'diagonal vertical horizontal',
    'golfpijp', ' keuken', 'nifty ', ' level ', 'program', 'ook', 'oma', 'foto', 'python',
    'hot', 'oogbal', 'yahoo', 'netjes', 'hoog', 'koen', 'nothing', 'debug', 'vet',
    'mensen', 'bier', 'neef', 'set', 'weg', 'google', 'zero']

# triple quote multi lines create a larger size when written to a file in Windows OS
puzzle_file = ('abcdefghijklm+\n'
               'qhorizontalaan\n'
               'bierxazghrycko\n'
               'wegiocgolfpijp\n'
               'jgoogleotestmq\n'
               'programtnwgror\n'
               'yahooiiomayews\n'
               'tqazwsxfpolvet\n'
               'hkedclekuekcxu\n'
               'oogbaledvlelev\n'
               'netjesbehtjoew\n'
               'dnesnemafpaczx\n'
               'lkjemnbuonifty\n'
               '-nothingfeorez')


class WordSearchPuzzleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a temporary file to test against
        with NamedTemporaryFile(mode='w', delete=False) as temp_word_puzzle:
            temp_word_puzzle.writelines(puzzle_file)
            cls.word_puzzle = temp_word_puzzle.name

        # create a temporary file to test against
        with NamedTemporaryFile(mode='w', delete=False) as temp_word_search_list:
            for line in word_search_list:
                temp_word_search_list.write(line if line.endswith('\n') else line + '\n')
            cls.word_search_list = temp_word_search_list.name

        # initiate the class for the whole test
        cls.ws = WordSearchPuzzle(cls.word_puzzle, cls.word_search_list)

    @classmethod
    def tearDownClass(cls):
        # try to remove the files created in the setUpClass
        try: os.unlink(cls.word_puzzle)
        except: pass
        try: os.unlink(cls.word_search_list)
        except: pass

    def test_get_puzzle_size(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._get_puzzle_size('/not/a/path.txt')

        # Return a tuple
        result = self.ws._get_puzzle_size(self.word_puzzle)  # -> (14, 14)
        self.assertIs(type(result), tuple)

        width, height = result
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

    def test_create_empty_dataframe(self):

        # should get an error when an invalid file path is given
        with self.assertRaises(AssertionError):
            self.ws._create_empty_dataframe('/not/a/path.txt')

        # create a DataFrame
        result = self.ws._create_empty_dataframe(self.word_puzzle)
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
        result = self.ws._create_puzzle_dataframe(self.word_puzzle)
        self.assertIs(type(result), pd.DataFrame)

        # DataFrame should have the size of the puzzle
        width, height = result.shape[:2]
        self.assertEqual(width, 14)
        self.assertEqual(height, 14)

        # comprehension list creates 2d-list of the puzzle file
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
            self.ws.create_word_set('/not/a/path.txt')

        # create a set
        result = self.ws.create_word_set(self.word_search_list)
        self.assertIs(type(result), set)

        # 33 words are given in the word_search_list
        # len(word_search_list) == 28
        # method should parse the different data correctly
        self.assertGreater(len(result), len(word_search_list))
        self.assertEqual(33, len(result))

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
            self.ws.get_all_posibilities(dataframe='dataframe')

        dataframe = self.ws.puzzle_df.copy()
        result = self.ws.get_all_posibilities(dataframe=dataframe)

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

        combined_data = self.ws.get_all_posibilities(dataframe)
        combined_positions = self.ws.get_all_posibilities(positionframe)

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
        diagonal = pd.Series(((0, 0), (99, 99)))
        result = self.ws.find_word_with_coordinates(dataframe, diagonal)
        self.assertIsNone(result)

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

        with self.assertRaises(AssertionError):
            self.ws.find_words_in_puzzle("")



if __name__ == '__main__':
    unittest.main()
