#
# charities-toyscript
# Author: Emily Quinn Finney
# A very toy implementation of a content-based recommender system
#
# Current fixes:
# - implement normalization so that similarity scores mean something
# - fix the for loops so that they're more efficient
# - fix the for loop in find_best_match so that the function always
#   returns something

import copy
import pandas as pd
import numpy as np


def normalize_data(filename):
    """
    Reads the data set into a Pandas data frame, and normalizes vectors.
    :return: A Pandas data frame with a set of intact, normalized data.
    """
    data = pd.read_csv(filename, sep='\s+', index_col=0, comment='#')
    datanorm = copy.deepcopy(data.select_dtypes(include=['int', 'float']))

    # determines which are the feature vectors
    # for every column that contains integer datatypes, normalize
    for column in data.select_dtypes(include=['int', 'float']):
        avg_value = np.mean(data[column])
        std_value = np.std(data[column])
        colnorm = (data[column]-avg_value)/std_value
        datanorm[column] = colnorm
    return datanorm


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
    :return: The row in the data frame that best matches user
             preferences.
    """
    score = -10.
    for row in range(len(item_matrix.index)):
        new_score = calculate_similarity(user_vec, item_matrix.iloc[row])
        if new_score >= score:
            score = new_score
            best = item_matrix.iloc[row]
    return best, score

new_data = normalize_data('charities-toydata.txt')
data = pd.read_csv('charities-toydata.txt', index_col=0, sep='\s+', comment='#')
data = data.select_dtypes(include=['int', 'float'])
my_user = pd.Series(data=[5, 95, 111111])
print "We recommend: \n", find_best_match(my_user, data)
