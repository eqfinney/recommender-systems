#
# charities-toyscript
# Author: Emily Quinn Finney
# A very toy implementation of a content-based recommender system
#
# Current fixes:
# - improve standardization function for reuse
# - fix the for loop so code is more efficient

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

    """
    A better way? 
    Calculate the average value, std in each column
    Put them in another table equal in size
    Do elementwise computations on the two tables
    (This may not actually avoid the for loop?)
    
    Oh and it turns out scikit-learn has functions that do this.
    """
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
    :return: The row in the data frame that best matches user preferences.
    """

    # a smaller similarity score corresponds to a smaller difference from user
    similarity_scores = item_matrix.apply(lambda x: calculate_similarity(user_vec, x),
                                          axis=1)
    score = similarity_scores.min()
    best_name = similarity_scores.idxmin()

    return best_name, score


def test_find_best_match():
    """
    Creating a first test!
    :return: exception or exit code
    """
    # create a data set
    test_data = pd.read_csv('charities-toydata.txt', index_col=0, sep='\s+', comment='#')
    # preprocess/clean data set
    test_data = test_data.select_dtypes(include=['int', 'float'])
    test_data['log_CEO_Salary'] = np.log10(test_data['CEO_Salary'])
    del test_data['CEO_Salary']
    # create a user
    test_user = pd.Series(data=[5, 95, 111111])
    # determine expected result
    expected_result_name = 'Epilepsy Foundation'
    # run find_best_match()
    observed_result, score = find_best_match(test_user, test_data)
    assert observed_result == expected_result_name, "Observed result did not equal expected result."


test_find_best_match()