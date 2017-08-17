#
# charities-toyscript
# Author: Emily Quinn Finney
# A very toy implementation of a content-based recommender system
#
# Current fixes:
# - improve standardization function for reuse
# - fix the for loop so code is more efficient
# - do you need to/should you normalize discrete variables
# - make sure the code actually does what it's supposed to do

import copy
import pandas as pd
import numpy as np


def normalize_data(filename, config={}, scaling='normalize'):
    """
    Reads the data set into a Pandas data frame, and normalizes vectors.
    :return: A Pandas data frame with a set of intact, normalized data.
    """
    # so first, run the configuration options
    data = pd.read_csv(filename, sep='\s+', index_col=0, comment='#')
    if config != {}:
        for colname in config:
            data[colname] = config[colname](data[colname])
    datanorm = copy.deepcopy(data.select_dtypes(include=['int', 'float']))

    """
    A better way? 
    Calculate the average value, std in each column
    Put them in another table equal in size
    Do elementwise computations on the two tables
    (This may not actually avoid the for loop?)
    
    configuration function/class would help generalize kinda
    """
    # second, standardize or normalize each of the configured columns
    if scaling == 'normalize':
        min_table = []
        max_table = []
        for column in data.select_dtypes(include=['int', 'float']):
            min_value = np.min(data[column])
            max_value = np.max(data[column])
            colnorm = (data[column] - min_value) / (max_value - min_value)
            datanorm[column] = colnorm
            min_table += min_value
            max_table += max_value
        return datanorm, min_table, max_table
    elif scaling == 'standardize':
        avg_table = []
        std_table = []
        for column in data.select_dtypes(include=['int', 'float']):
            avg_value = np.mean(data[column])
            std_value = np.std(data[column])
            colnorm = (data[column] - avg_value) / std_value
            datanorm[column] = colnorm
            avg_table.append(avg_value)
            std_table.append(std_value)
        return datanorm, avg_table, std_table
    else:
        datanorm = data
        return datanorm, 1., 1.


def normalize_user(user_vec, value_tuple, scaling='normalize'):
    """
    Scales the user vector to match with the scaling of the data
    :param user_vec: A vector of features of the user (series).
    :param value_tuple: A tuple containing values with which to scale.
    :param scaling: Which type of scaling (string, Normalize or Standardize or None)
    :return: Normalize user vector.
    """
    if scaling == 'normalize':
        min_value = value_tuple[0]
        max_value = value_tuple[1]
        user_vec = (user_vec - min_value) / (max_value - min_value)
        return user_vec
    elif scaling == 'standardize':
        avg_value = value_tuple[0]
        std_value = value_tuple[1]
        user_vec = (user_vec - avg_value) / std_value
        return user_vec
    else:
        return user_vec


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
    score = similarity_scores.min()
    best_name = similarity_scores.idxmin()

    assert isinstance(score, float)
    return best_name, score


def test_find_best_match():
    """
    Creating a first test!
    :return: exception or exit code
    """
    # preprocess/clean data set
    configuration_file = {'CEO_Salary': np.log10}
    test_data, avg_table, std_table = normalize_data('charities-toydata.txt',
                                                     configuration_file, scaling='standardize')
    # create a user
    user_vec = [0, 0, 22132891]
    test_user = [normalize_user(x, (y, z), scaling='standardize')
                 for x, y, z in (user_vec, avg_table, std_table)]
    # determine expected result
    expected_result = 'Cancer Institute'
    # run find_best_match()
    observed_result, score = find_best_match(test_user, test_data)
    assert observed_result == expected_result, \
        "Observed result " + observed_result + " did not equal expected result " + expected_result

test_find_best_match()
