#
# PLAYING AROUND WITH HYPOTHESIS
# Author: Emily Quinn Finney
#

import pandas as pd
from hypothesis import given
from hypothesis import strategies as st


import charities_toyscript as ct

@given(st.lists, st.lists)
def test_calculate_similarity(x, y):
    result = ct.calculate_similarity(x, y)
    result = ct.calculate_similarity(y, x)
    assert result1 == result2

@given(st.lists, st.from_type(pd.DataFrame()))
def test_find_best_value(x, y):
    result = ct.find_best_match(x, y)
    assert result.isinstance(pd.Series)
