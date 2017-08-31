#
# PLAYING AROUND WITH HYPOTHESIS
# Author: Emily Quinn Finney
#

import pandas as pd
from hypothesis import given, assume
from hypothesis import strategies as st


import charities_toyscript as ct

keyword = st.lists(st.floats(allow_nan=False, min_value=1.e-50, max_value=1.e50), min_size=1)
df_keyword = st.from_type(pd.DataFrame())

@given(keyword, keyword)
def test_calculate_similarity(x, y):
    assume(len(x) == len(y))
    result1 = ct.calculate_similarity(x, y)
    result2 = ct.calculate_similarity(y, x)
    assert result1 == result2

@given(keyword, st.from_type(pd.DataFrame()))
def test_find_best_value(x, y):
    result = ct.find_best_match(x, y)
    assert result.isinstance(pd.Series)
