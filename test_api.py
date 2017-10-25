#
# tests the api.py module
# author: Emily Quinn Finney
#

import api

url = "https://api.data.charitynavigator.org/Organizations/"


@pytest.fixture
def parameters():
    with open('cn.keys', 'r') as f:
        d = f.readlines()
        api_id = d[0].strip()
        api_key = d[1].strip()

    return {'app_key': api_key, 'app_id': api_id, 'pageNum': 1, 'pageSize': 1000, 'rated': True}


@pytest.fixture
def filename():
    file_name = 'test_file.txt'
    with open(file_name, 'w') as f:
        f.write('abc')
    yield file_name
    print("commence filename teardown")
    if os.path.isfile(file_name):
        os.remove(file_name)


def test_http_request_generator(url, parameters):
    # TODO: this should be a mock, not an actual request
    api.http_request_generator(url, parameters)
    url_set = {'https://api.data.charitynavigator.org/Organizations/?'}
    for key, value in parameters:
        url_set.add(''.join([key, '=', value]))
    split_url = response.url.split('&')
    assert split_url == url_set


def test_find_and_replace(filename, to_find='abc', to_replace='xyz'):
    api.find_and_replace(filename, to_find, to_replace)
    with open(filename, 'r') as f:
        data = f.readlines()
        assert to_find not in data
        assert to_replace in data


def test_complete_http_request_generators(filename, parameters, url):
    """
    Tests the main function
    :return: nothing, but should write the data from the HTTP request to file
    """
    api.complete_http_request_generators(filename, url, parameters)
