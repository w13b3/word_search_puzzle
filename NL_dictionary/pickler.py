#!/usr/bin/env python3

import os
import pickle
from pprint import pprint

def dump_pickle(pickle_file_path: str, obj: object = None) -> str:
    """ create a pickle file from an object """
    real_file_path = os.path.realpath(str(pickle_file_path))
    real_dir_path = os.path.dirname(real_file_path)
    assert os.path.exists(real_dir_path), \
        'give a path to a directory that exists, given: %s' % real_file_path

    with open(real_file_path, 'wb') as pickle_in:
        pickle.dump(obj, pickle_in)

    assert os.path.isfile(real_file_path), 'somehow the pickle file is not made'
    return real_file_path


def load_pickle(pickle_file_path: str) -> object:
    """ create an object from a pickle file """
    real_file_path = os.path.realpath(str(pickle_file_path))
    assert os.path.exists(real_file_path), \
        'give a path that exists, given: %s' % real_file_path

    with open(real_file_path, 'rb') as pickle_out:
        return pickle.load(pickle_out)


if __name__ == '__main__':
    file_path = 'NL_dictionary_set.pkl'
    NL_words_set = load_pickle(file_path)
    pprint(len(NL_words_set))
    # pprint(NL_words_set)
