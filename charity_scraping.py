#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

import sys
#sys.path.insert(0, '/home/equinney/github/web-scraping')
#import web_crawler_main_class as webs
sys.path.insert(0, '/home/equinney/github/verbal-infusions')
from hteaml_parser import read_soup
import pandas as pd
import re
import time
import bs4


def scrape_website(url_list):

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


def locate_tags(structured_page, tag_pattern, contains):
    """
    Given a page structured in a Beautiful Soup format, returns all descriptive text on page
    :param structured_page: list of web pages, structured in Beautiful Soup format
    :param tag_pattern: string, the HTML tag pattern for which to search
    :param tag_names: tuple of strings, the names of the relevant HTML tags to write
    :param filename: string, the name of the file to which to write the text
    :return: nothing, but should write a corpus of text to file
    """
        # identify all descriptions on web page matching the pattern in the PageScraper object
    tags = structured_page.find_all('div', class_=re.compile(tag_pattern))
    #print(len(tags))
    #import pprint
    for i, tag in enumerate(tags):
        if contains in tag.text:
            #print(i)
            #pprint.pprint(tag)
            yield tag

def locate_charity_info(tag, tag_names):
    # locate mission info
    queue = list(tag.children)
    while len(queue) != 0:
        element = queue.pop(0)
        if type(element) == bs4.element.Tag:
            if element.name in tag_names[0]:
                # header title
                print(element.string.strip())
            elif element.name in tag_names[1]:
                # contents
                if element.string:
                    print(element.string.strip())
                elif element.find_all(id="orgSiteLink"):
                    print(element.a['href'].strip())
                else:
                    print(element.text.strip())
            else:
                for sublist in list(element.children):
                    queue.append(sublist)



if __name__ == '__main__':
    #scrape_website(['https://www.charitynavigator.org/index.cfm?bay=search.alpha'])
    """with open('cn_working.html', 'r') as f:
        new_file = f.read()
    df = pd.read_html(new_file)#, re.compile('(cn-appear*|accordion-item-bd*)'))
    for frame in df:
        print("next frame is:")
        print(frame)
        """
    page = read_soup('cn_working.html')
    contact_info_generator = locate_tags(page[0], '(^rating$)', 'Charity Contact Info')
    mission_generator = locate_tags(page[0], '(^summaryBox cn-accordion-rating$)', 'Mission')
    contact_info_tag = next(contact_info_generator)
    mission_tag = next(mission_generator)
    locate_charity_info(contact_info_tag, ('h1', 'p'))