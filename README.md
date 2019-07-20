# word_search_puzzle
Solver for [word search](https://en.wikipedia.org/wiki/Word_search) puzzles

## In action
![this is a gif](https://i.imgur.com/eqJWtqt.gif)

---
### How to use this

###### Assumed you have pulled word-search-puzzle and installed the required files.

1. Find a word search puzzle.  [example](puzzles/apple-word-search_picture.png)
2. Recreate the puzzle in a text file.  [example](puzzles/apple_word_search_puzzle.txt)
3. write the words to find, sperated with spaces of new-lines, in a seperate file. [example](puzzles/apple_word_search_set.txt)
4. run: python3 [word_search_puzzle/main.py](word_search_puzzle/main.py) --help
5. read the instructions.

### What is used to create this
#### Used Python 3.6.7

##### Required modules:
- numpy  (used 1.16.4)
- pandas (used 0.24.2)

##### Optional mocules:
- tkinter
- itertools.cycle

### known issues:
- [Palindrome](https://en.wikipedia.org/wiki/Palindrome) words are founds twice.
- - example: racecar, reviver, kayak,.. etc.
- [Augmentative](https://en.wikipedia.org/wiki/Augmentative) base words are found twice if both are given.
- - example: 'grand' and 'grandmaster' -> 'grand' will be found twice.
