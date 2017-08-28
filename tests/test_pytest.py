#
# PLAYING AROUND WITH PYTEST
# Author: Emily Quinn Finney
#

import pytest
import pandas as pd
import charities_toyscript as ct


def test_calculate_similarity():
    result = ct.calculate_similarity([5, 72, 599999], [5, 72, 599999])
    assert abs(result-1.) < 0.0001

def test_find_best_value():
    result = ct.find_best_match([5,72,5999999], pd.DataFrame(pd.Series([5, 78, 523456]),
                                                             pd.Series([2, 68, 23893298]),
                                                             pd.Series([5, 97, 183111]),
                                                             pd.Series([4, 89, 324122]),
                                                             pd.Series([3, 91, 230948])))
    assert result == "Animals 4Eva"
