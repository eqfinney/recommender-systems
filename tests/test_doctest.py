#
# PLAYING AROUND WITH DOCTEST
# Author: Emily Quinn Finney
#

import doctest

import sys
sys.path.insert(0, '/home/equinney/github/recommender-systems/')
from charities_toyscript import *

doctest.testfile('../charities_toyscript.py')

"""
Tests:
calculate_similarity
find_best_match
"""