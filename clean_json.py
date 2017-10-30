#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

import json


# TODO: better to just extract individual URLs?
# this isn't a great way to do this but not sure if there's a better alternative
def read_json(json_file):
    """
    Reads a JSON file and retains the data
    Might need to start worrying about whether this will fit in memory.
    :param json_file: a file containing JSON data
    :return: data, a dictionary of data
    """
    with open(json_file, 'r') as f:
        list_of_strings = list()
        for line in f:
            list_of_strings = line.split('"organization":')
        list_of_json = list()
        exception_count = 0
        for index, value in enumerate(list_of_strings[1:]):
            value = ''.join(['{"organization":', value])
            value = value[:len(value)-3]
            if value[-1] != '}':
                value = ''.join([value, '}'])
            print(value)
            print(index)
            try:
                list_of_json.append(json.loads(value))
            # TODO: specify the type of exception
            except:
                exception_count += 1
        print(exception_count)

        return list_of_json


def extract_keyword(json_list, keyword):
    """
    Given a dictionary, returns all values associated with a given keyword as a list
    :param json_list: a list of JSON data
    :param keyword: string, a keyword in the dictionary
    :return: keyword_list, a list of all values matching the keyword
    """
    keyword_list = list()
    for index, value in enumerate(json_list):
        keyword_list.append(json_list[index]["organization"][keyword])
    print(keyword_list)

    return keyword_list
