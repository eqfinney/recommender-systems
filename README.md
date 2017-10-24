## Recommender Systems
Author: Emily Quinn Finney

This is my exploration of recommender systems while attending the Recurse 
Center (https://www.recurse.com/). The original code was written with the 
intent of being tested on toy databases (charities_toydata.txt and 
cat_food.txt). In the future, it will be implemented using data obtained
from Charity Navigator (https://www.charitynavigator.org/). The package 
includes:

* api.py: code I used to access the Charity Navigator server using its API and 
Python's requests package.
* charities_realdeal.ipynb (not yet implemented): a Jupyter notebook 
containing a brief analysis of data obtained from Charity Navigator. 
* charities_toyscript.py: an implementation of a content-based recommender 
system, primarily using toy databases. 
* test_api.py: a pytest module that tests the api.py module.

The package also includes a directory of tests written for the 
charities_toyscript.py module. I used this project as a means of exploring 
several test frameworks in Python, so the test directory contains tests written
for Python's unittest, pytest, doctest, and hypothesis libraries. 

Last edited 10/24/2017