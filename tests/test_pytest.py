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
    result = ct.find_best_match([5,78,523456], ct.Data('charities-toydata.txt'))
    assert result == "Animals 4Eva"

def test_user_preference():
    result = ct.user_preference(["Animals 4Eva", "Dog Rescue Fund"], ct.Data('charities-toydata.txt'))
    expected_result = np.array([4.5, 83.5, 423789])
    assert np.array_equal(result, expected_result)
