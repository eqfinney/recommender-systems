#
# charities_realdeal
# Author: Emily Quinn Finney
# A not-very-toy implementation of a content-based recommender system
#
# Current fixes:
# - clean the data
# - feature extraction

import pandas as pd
import numpy as np
import charities_toyscript as ct

try:
    import psyco
    psyco.full()
except ImportError:
    pass
