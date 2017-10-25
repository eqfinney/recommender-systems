#
# api
# Author: Emily Quinn Finney
# Trying to figure out how http requests work!!!!!!!!!!!!
# Also experimenting with test-driven development

#

import json
import time
import string
import difflib
import requests


def http_request(url, params=None):
    """
    Pings the server with an HTTP request, records the status code, and unpacks data
    :param url: server from which to request data
    :param params: the parameters of the http request, dictionary
    :return: response.status code, int, which tells you if the request succeeded
             response, which should be in the form of a requests response
    """
    if params is None:
        params = {}
    return requests.get(url, params)


def http_request_generator(url, params=None, new_params=None):
    """
    Completes an HTTP request as a generator.
    :param url: the base URL from which to make the HTTP request.
    :param params: the parameters with which to modify the HTTP request
    :param new_params: the updated parameters with which to modify the HTTP request
    :return: a generator object that, when next() is called on it, gives a new page of data
    """
    if params is None:
        params = {}
    if new_params is None:
        new_params = {}
    while True:
        # make the HTTP request
        response = http_request(url, params)
        # make sure the response isn't failing weirdly
        response.raise_for_status()
        # give the response back to the function
        yield response
        # now update parameters
        params['pageNum'], new_params['pageNum'] = new_params['pageNum'], new_params['pageNum'] + 1


def find_and_replace(filename, to_find='][', to_replace=', '):
    """
    Finds and replaces strings to turn the pseudo-JSON into an actual JSON.
    :param filename: the name of the possible JSON
    :param to_find: the string to find
    :param to_replace: the string to replace
    :return: an actual JSON file
    """
    with open(filename, 'r+') as f:
        d = f.readlines()
        f.seek(0)
        for line in d:
            newline = line.replace(to_find, to_replace)
            assert to_find not in newline
            f.write(newline)
        f.close()


def complete_http_request_generators(filename, url, params=None):
    """
    The main function, dumps all the pages of a successful HTTP request into a JSON file
    :param filename: the name of the file into which to dump the JSON material
    :param url: the base URL from which to make the HTTP request
    :param params: the parameters with which to modify the HTTP request
    :return: Nothing, but should produce a JSON file
    """
    if params is None:
        params = {}

    page = 0
    params['pageNum'] = 0
    new_params = params
    new_params['pageNum'] = params['pageNum'] + 1
    gen = http_request_generator(url, params, new_params)

    # keep requesting pages and write results to file
    while page < 10:
        print(' '.join(["Iteration number is:", str(page)]))
        response = next(gen)
        with open(filename, 'a') as f:
            print(response.json())
            json.dump(response.json(), f, ensure_ascii=False)
            f.close()
        time.sleep(1)
        page += 1

    # should occur after all the pages have been downloaded
    find_and_replace('cn.json', '][', ']|[')
    print(' '.join(["Finished! Check results in", filename]))
