#
# api
# Author: Emily Quinn Finney
# Trying to figure out how http requests work!!!!!!!!!!!!
# Also experimenting with test-driven development
#
# to fix:
# - I still need to read up on different kinds of testing, when to use, etc, and implement
#   - unittests: https://docs.python.org/3/library/unittest.html
#   - unittest mocks: https://docs.python.org/3/library/unittest.mock.html
#   - doctests: https://docs.python.org/2/library/doctest.html
# - I have no idea how to get the Charity Navigator thing to work correctly.
# - I'm still doing doctests wrong.
#

import requests


def http_request(url, params={}):
    """
    Pings the server with an HTTP request, records the status code, and unpacks data
    :param url: server from which to request data

    >>> http_request("http://api.open-notify.org/astros.json")[0]
    200
    >>> type(http_request("http://api.open-notify.org/astros.json"))[1]
    <class 'dict'>
    >>> http_request("http://api.open-notify.org/astros.json")[1]!= {}
    True
    >>> http_request("https://projects.propublica.org/nonprofits/api/v2/search.json")[0]
    200
    >>> http_request("http://api.charitynavigator.org/api/v1/search", params=parameters)[0]
    200
    >>> type(http_request("http://api.open-notify.org/astros.json"))[1]
    <class 'dict'>
    >>> http_request("http://api.open-notify.org/astros.json")[1]!= {}
    True

    :param params: the parameters of the http request, dictionary
    :return: status code, int, which tells you if the request succeeded
             data, which should be in the form of a Python dictionary
    """
    response = requests.get(url, params)
    print(type(response.status_code))
    if response.status_code == 200:
        return response.status_code, response.json()
    else:
        return response.status_code, {}


def test_http_request():
    """
    Tests the HTTP request function
    :param url: the URL of the website to test
    :param params: the parameters of the http request, dictionary
    :return:
    """
    parameters = {'app_key': '7bbd24b88b0526256feaa4c3cf00ba8f', 'app_id': '1e71a304', 'term': 'cats', 'format': 'json'}
    status_code, dictionary = http_request("http://api.charitynavigator.org/api/v1/search", params=parameters)
    assert status_code == 200, "The server has returned an unsuccessful status code: " + str(status_code)
    assert dictionary != {}, "The server has returned no data"
    assert isinstance(dictionary, type({})), "The data are in the wrong format"
    return

if __name__ == "__main__":
    import doctest
    doctest.testmod()