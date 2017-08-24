#
# charities-toyscript
# Author: Emily Quinn Finney
# A very toy implementation of a content-based recommender system
#
# Current fixes:
# - fix the for loop so code is more efficient and/or use generators? Yay playing with new ideas!
# - make sure the code actually does what it's supposed to do
# - figure out what makes the classes work the way I want them to, refactor as needed

import copy
import pandas as pd
import numpy as np


class Data:

    def __init__(self, filename, config_file=None):
        if filename.split('.')[-1] == '.json':
            # mkay so my big problem is that the file isn't actually JSON
            # each request I make to the server gets a JSON file, but they don't combine just by appending
            # I could do a Python-level find-and-replace, make all '][' become ', ' instead.
            # and there are likely other, even faster, methods
            self.data = json.load(filename)
        else:
            self.data = pd.read_csv(filename, sep='\s+', index_col=0, comment='#')
        self.configuration = config_file

    def configure(self):
        for column in self.data:
            self.data[column] = config_file[column](self.data[column])

    def normalize(self):
        for column in self.data.select_dtypes(include=['int', 'float']):
            min_value = np.min(self.data[column])
            max_value = np.max(self.data[column])
            colnorm = (self.data[column] - min_value) / (max_value - min_value)
            self.data[column] = colnorm
            min_list.append(min_value)
            max_list.append(max_value)
        return min_list, max_list

    def standardize(self):
        for column in self.data.select_dtypes(include=['int', 'float']):
            avg_value = np.mean(self.data[column])
            std_value = np.std(self.data[column])
            colnorm = (self.data[column] - avg_value) / std_value
            self.data[column] = colnorm
            avg_table.append(avg_value)
            std_table.append(std_value)
        return avg_list, std_list


class User:

    def __init__(self, user_vec, config_user):
        self.vector = user_vec
        self.configuration = config_user

    def normalize(self, min_list, max_list):
        for idx, value in enumerate(self.vector):
            min_value = min_list[idx]
            max_value = max_list[idx]
            self.vector[idx] = (value - min_value) / (max_value - min_value)

    def standardize(self, avg_list, std_list):
        for idx, value in enumerate(self.vector):
            avg_value = avg_list[idx]
            std_value = std_list[idx]
            self.vector[idx] = (value - avg_value) / std_value


def calculate_similarity(vec1, vec2):
    """
    Determines the cosine distance between two vectors.
    :param vec1: A vector of features in the data set (series).
    :param vec2: Another vector of features in the data set (series).
    :return: The cosine distance, a float.
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
    """

    # a smaller similarity score corresponds to a smaller difference from user
    similarity_scores = item_matrix.apply(lambda x: calculate_similarity(user_vec, x),
                                          axis=1)
    best_name = similarity_scores.idxmin()

    return best_name


class TestToyRecommenderSystem:
    pass

    def __init__(self, data_vector, user_vector, expected_result):
        self.vec1 = data_vector
        self.vec2 = user_vector
        self.expected = expected_result

    def test_calculate_similarity(self, vec1, vec2):
        observed_score = calculate_similarity(self.vec1, self.vec2)

    def test_find_best_match(self, test_case):
        observed_match = find_best_match(test_user, test_data)
        self.assertTrue(observed_match == self.expected)


#base_test_case = Data('cn.json', {'CEO_Salary': np.log10})
#user_test_case = User([5, 78, 523456], {})

base_test_case = Data('cn.json')
