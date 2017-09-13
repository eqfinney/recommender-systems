#
# PLAYING AROUND WITH PYTEST
# Author: Emily Quinn Finney
#

import pytest
import pandas as pd
import numpy as np
import charities_toyscript as ct


def test_calculate_similarity_samevec():
    result = ct.calculate_similarity([5, 72, 599999], [5, 72, 599999])
    assert abs(result-1.) < 0.0001


def test_calculate_similarity_diffvec():
    result = ct.calculate_similarity([1, 1, 1], [0, 1, 0])
    assert abs(result-0.577) < 0.001


def test_find_best_value():
    result = ct.find_best_match([0, 1, 0], ct.Data('charities_toydata.txt'))
    assert result == "Cancer Institute"


def test_user_preference():
    result = ct.user_preference(["Animals 4Eva", "Dog Rescue Fund"], ct.Data('charities_toydata.txt'))
    expected_result = np.array([4.5, 83.5, 423789])
    assert np.array_equal(result, expected_result)


#def test_data_normalize_norm(data=ct.Data('charities_toydata.txt')):
#    result = data.normalize()
#    assert result[0].data


def test_data_normalize_min(data=ct.Data('charities_toydata.txt')):
    result = data.normalize()
    assert result[1] == [2, 68, 183111]


def test_data_normalize_max(data=ct.Data('charities_toydata.txt')):
    result = data.normalize()
    assert result[2] == [5, 97, 23893298]


#def test_data_standardize_norm(data=ct.Data('charities_toydata.txt')):
#    result = data.normalize()
#    assert result[0].data


def test_data_standardize_min(data=ct.Data('charities_toydata.txt')):
    result = data.normalize()
    assert result[1] == [2, 68, 183111]


def test_data_standardize_max(data=ct.Data('charities_toydata.txt')):
    result = data.normalize()
    assert result[2] == [5, 97, 23893298]


def test_user_normalize_norm(user=ct.User([5, 95, 100000])):
    result = user.normalize([0, 0, 0], [5, 100, 10000000]).vector
    expected_result = np.array([1.0, 0.95, 0.01])
    assert np.array_equal(result, expected_result)


def test_user_standardize_norm(user=ct.User([5, 65, 100000])):
    result = user.standardize([3, 80, 100000], [1, 15, 10000]).vector
    expected_result = np.array([2., -1., 0.])
    assert np.array_equal(result, expected_result)

# test_data_configuration
# test_user_configuration
