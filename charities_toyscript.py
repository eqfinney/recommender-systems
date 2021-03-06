#
# charities-toyscript
# Author: Emily Quinn Finney
# A very toy implementation of a content-based recommender system
#
# Current fixes:
# - write tests for every part of this code, probably using pytest

import pandas as pd
import numpy as np

try:
    import psyco
    psyco.full()
except ImportError:
    pass

__all__ = ['Data', 'User', 'calculate_similarity', 'find_best_match']


def test_decorator(function):
    """
    Testing a decorator that prints all args and kwargs for a function.
    """

    def function_wrapper(*args, **kwargs):
        for value in args, kwargs:
            print(value)
        return function(*args, **kwargs)

    return function_wrapper

class Data:

    def __init__(self, filename, config_file=None):

        if filename.split('.')[-1] == '.json':
            self.data = pd.DataFrame(json.load(filename))
        else:
            self.data = pd.read_csv(filename, sep='\s+', index_col=0, comment='#')
        if config_file:
            self.configure()
            self.configuration = config_file

    def configure(self):
        for column in self.data:
            self.data[column] = config_file[column](self.data[column])

    def normalize(self):
        min_list = []
        max_list = []
        for column in self.data.select_dtypes(include=['int', 'float']):
            min_value = np.min(self.data[column])
            max_value = np.max(self.data[column])
            colnorm = (self.data[column] - min_value) / (max_value - min_value)
            self.data[column] = colnorm
            min_list.append(min_value)
            max_list.append(max_value)
        return self, min_list, max_list

    def standardize(self):
        avg_list = []
        std_list = []
        for column in self.data.select_dtypes(include=['int', 'float']):
            avg_value = np.mean(self.data[column])
            std_value = np.std(self.data[column])
            colnorm = (self.data[column] - avg_value) / std_value
            self.data[column] = colnorm
            avg_list.append(avg_value)
            std_list.append(std_value)
        return self, avg_list, std_list


class User:

    def __init__(self, user_vec, config_user=None):
        self.vector = np.array(user_vec, dtype=float)
        if config_user:
            self.configure()
            self.configuration = config_user

    def normalize(self, min_list, max_list):
        for idx, value in enumerate(self.vector):
            min_value = min_list[idx]
            max_value = max_list[idx]
            new_value = (value - min_value) / (max_value - min_value)
            self.vector[idx] = new_value

        return self

    def standardize(self, avg_list, std_list):
        for idx, value in enumerate(self.vector):
            avg_value = avg_list[idx]
            std_value = std_list[idx]
            new_value = (value - avg_value) / std_value
            self.vector[idx] = new_value

        return self


def user_preference(charity_list, database):
    """
    Determines the user's preference vector, based on other charities the user prefers.
    :param charity_list: a list of charities the user likes, list of strings.
                         (future: add weights)
    :param database: the data from which to obtain the user's preferred charity
    :return: user_preference, a vector that conveys the user's interests
    """

    user_vec = np.zeros(len(database.data.T[charity_list[0]]))
    for charity in charity_list:
        new_charity = np.array(database.data.T[charity])
        user_vec = np.add(user_vec, new_charity)

    user_vec = user_vec / len(charity_list)

    return user_vec


def calculate_similarity(vec1, vec2):
    """
    Determines the cosine distance between two vectors.
    :param vec1: A vector of features in the data set (series).
    :param vec2: Another vector of features in the data set (series).
    :return: The cosine distance, a float.
    >>> calculate_similarity([5,78,523456], [5,78,523456])
    1.0
    >>> calculate_similarity([1, 1, 1], [0, 1, 0])
    0.57735026918962584
    >>> calculate_similarity([5,70,523456], [5,78,523456])
    0.99999999988321431
    """
    vec1 = np.asarray(vec1)
    vec2 = np.asarray(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1)*np.linalg.norm(vec2)
    return dot_product/norm_product


def find_best_match(user_vec, item_matrix):
    """
    Determines the row in the data set that best matches the user's
    preferences.
    :param user_vec: A vector of preferred user features (series).
    :param item_matrix: A data frame containing item features.
    :return: The row in the data frame that best matches user preferences.
    >>> find_best_match([0, 1, 0], Data('charities_toydata.txt'))
    Cancer Institute
    >>> find_best_match([0.5,0.5,1,0.5,0.5,0.5,0], Data('cat_food.txt'))
    Feed the Feline Chicken
    """

    # a smaller similarity score corresponds to a smaller difference from user
    similarity_scores = item_matrix.data.apply(lambda x: calculate_similarity(user_vec, x), axis=1)
    best_name = similarity_scores.idxmax()

    return best_name


if __name__ == '__main__':
    import doctest
    doctest.testmod()
