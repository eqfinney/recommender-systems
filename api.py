#
# api
# Author: Emily Quinn Finney
# Trying to figure out how http requests work!!!!!!!!!!!!
# Also experimenting with test-driven development

"""
to fix:
- I still need to read up on different kinds of testing, when to use, etc, and implement
  - unittests: https://docs.python.org/3/library/unittest.html
  - unittest mocks: https://docs.python.org/3/library/unittest.mock.html
  - doctests: https://docs.python.org/2/library/doctest.html
- Make sure that the JSON dumping isn't clobbering the original file
- Actually test the JSON dumping function
- Refactor the JSON dumping function so that it's not a giant for loop maybe
- Add certificate verification and figure out how that even works...
"""

import requests
import json
import time


def http_request(url, params={}):
    """
    Pings the server with an HTTP request, records the status code, and unpacks data
    :param url: server from which to request data

    >>> http_request("http://api.open-notify.org/astros.json")[0]
    <class 'int'>
    200
    >>> http_request("https://projects.propublica.org/nonprofits/api/v2/search.json")[0]
    <class 'int'>
    200
    >>> parameters = {'app_key': '7bbd24b88b0526256feaa4c3cf00ba8f', 'app_id': '1e71a304', 'format': 'json', 'page': '7'}
    >>> http_request("https://api.data.charitynavigator.org/api/v1/search", params=parameters)[0]
    <class 'int'>
    200

    :param params: the parameters of the http request, dictionary
    :return: response.status code, int, which tells you if the request succeeded
             response, which should be in the form of a requests response
    """
    response = requests.get(url, params, verify=False)
    return response.status_code, response


def http_request_generator(url, params={}, new_params={}):
    """
    Completes an HTTP request as a generator. WHO KNOWS IF THIS WILL WORK.
    :param url: the base URL from which to make the HTTP request.
    :param params: the parameters with which to modify the HTTP request
    :return: a generator object that, when next() is called on it, gives a new page of data
    """
    while True:
        # make the HTTP request
        response = requests.get(url, params)
        # make sure the response isn't failing weirdly
        assert response.status_code == 200, "There is a status code failure".join(str(response.status_code))
        # give the response back to the function
        yield response
        # now update parameters
        params['page'], new_params['page'] = new_params['page'], new_params['page'] + 1


def complete_http_request_generators(filename, url, params={}):
    """
    The main function, dumps all the pages of a successful HTTP request into a JSON file
    :param filename: the name of the file into which to dump the JSON material
    :param url: the base URL from which to make the HTTP request
    :param params: the parameters with which to modify the HTTP request
    :return: Nothing, but should produce a JSON file
    """
    params['page'] = 0
    new_params = params
    new_params['page'] = params['page'] + 1
    gen = http_request_generator(url, params, new_params)

    # I want this function to keep requesting pages and writing them into a file
    while True:
        response = next(gen)
        with open(filename, 'a') as f:
            json.dump(response.json(), f, ensure_ascii=False)
            f.close()
        time.sleep(1)

    # should occur after all the pages have been downloaded
    print(' '.join(["Finished! Check results in", filename]))


def test_http_request():
    """
    Tests the HTTP request function
    :return:
    """
    parameters = {'app_key': '7bbd24b88b0526256feaa4c3cf00ba8f', 'app_id': '1e71a304'}
    object = complete_http_request_generators('cn.json', "https://api.data.charitynavigator.org/Organizations/",
                                              params=parameters)
    time.sleep(1)
    # with object as ...
    return


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    parameters = {'app_key': '7bbd24b88b0526256feaa4c3cf00ba8f', 'app_id': '1e71a304', 'format': 'json', 'page': 0}
    response = http_request("https://api.data.charitynavigator.org/api/v1/search", params=parameters)[0]
    print(response)
    #test_http_request()