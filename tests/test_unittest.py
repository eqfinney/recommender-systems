#
# PLAYING AROUND WITH UNITTEST
# Author: Emily Quinn Finney
#

import unittest
import charities_toyscript as ct

class TestToyRecommenderSystem(unittest.TestCase):
    """
    A test class for the functions in charities-toyscript.py
    """

    def setUp(self):
        self.test_user = [5, 72, 599999]
        self.test_data = ct.Data('charities-toydata.txt')

    def test_calculate_similarity(self):
        observed_score = ct.calculate_similarity(self.test_user, self.test_data.data.iloc[0])
        self.assertAlmostEqual(observed_score, 0.5, "failure in test_calculate_similarity()")

    def test_find_best_match(self):
        observed_match = ct.find_best_match(self.test_user, self.test_data.data)
        self.assertEquals(observed_match, "Animals 4Eva", "failure in find_best_match()")