#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

import json
import sys
sys.path.insert(0, '/home/equinney/github/web-scraping')
import web_crawler_main_class as webs


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


def main():
    cn_data = read_json('cn_old.json')
    url_list = extract_keyword(cn_data, "charityNavigatorURL")
    print(url_list)

    import asyncio
    import aiohttp

    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as client_session:
        cn_loader = webs.URLoader(url_list[0], client_session)
        cn_scraper = webs.PageScraper(url_list[0], 'www.charitynavigator.org/index.cfm?bay', '(orgid|ein)=[0-9]*',
                                      queue=url_list)
        PrimaryScraper = webs.MainScraper(cn_loader, cn_scraper, 'cn_corpus.html')
        loop.run_until_complete(PrimaryScraper.main())

    loop.close()


if __name__ == '__main__':
    main()
