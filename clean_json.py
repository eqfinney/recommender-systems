#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

#from webscraping import web_crawler_main_class as webs
import json


def read_json(json_file):
    """
    Reads a JSON file and retains the data
    Might need to start worrying about whether this will fit in memory.
    :param json_file: a file containing JSON data
    :return: data, a dictionary of data
    """
    data = {}
    with open(json_file) as f:
        import ipdb
        #ipdb.set_trace()
        with open(json_file, 'r') as f:
            for line in f:
                list_of_strings = line.split(',')
                for value in list_of_strings:
                    # each of the values should be in JSON
                    print(value)
                    data += json.loads(value)

    return data


def extract_keyword(json_dict, keyword):
    """
    Given a dictionary, returns all values associated with a given keyword as a list
    :param json_dict: a dictionary of data
    :param keyword: string, a keyword in the dictionary
    :return: keyword_list, a list of all values matching the keyword
    """
    keyword_list = json_dict[keyword]
    print(keyword_list)

    return keyword_list


if __name__ == '__main__':
    cn_data = read_json('cn.json')
    url_list = extract_keyword(cn_data, "charityNavigatorURL")
    print(url_list)
