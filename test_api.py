#
# tests the api.py module
# author: Emily Quinn Finney
#

# TODO: add tests for other functions, cause there's no unit testing here
# might need to include patches with pytest mock objects

import api

def test_complete_http_request_generators(filename='cn.json',
                                          url="https://api.data.charitynavigator.org/Organizations/"):
    """
    Tests the main function
    :return: nothing, but should write the data from the HTTP request to file
    """
    with open('cn.keys', 'r') as f:
        d = f.readlines()
        api_id = d[0].strip()
        api_key = d[1].strip()

    parameters = {'app_key': api_key, 'app_id': api_id, 'pageSize': 1000,
                  'pageNum': 1}
    api.complete_http_request_generators(filename, url, params=parameters)
    return
