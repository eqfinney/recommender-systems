#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

import sys
import pandas as pd
import re
import time
import bs4


# TODO: make this function more generalizable, also should probably live somewhere else
def scrape_website(url_list):

    import asyncio
    import aiohttp
    sys.path.insert(0, '/home/equinney/github/web-scraping')
    import web_crawler_main_class as webs

    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as client_session:
        cn_loader = webs.URLoader(url_list[0], client_session)
        cn_scraper = webs.PageScraper(url_list[0], 'www.charitynavigator.org/index.cfm?bay', '(orgid|ein)=[0-9]*',
                                      queue=url_list)
        PrimaryScraper = webs.MainScraper(cn_loader, cn_scraper, 'cn_corpus.html')
        loop.run_until_complete(PrimaryScraper.main())

    loop.close()


# TODO: write test
def locate_tags(structured_page, tag_pattern, contains):
    """
    Given a page structured in a Beautiful Soup format, returns all tags matching a tag pattern
    :param structured_page: a web page, structured in Beautiful Soup format
    :param tag_pattern: string, the HTML tag pattern for which to search
    :param contains: a regular expression that should be included in the tag name
    :yield: tag, a bs4.element.Tag object
    """
    # identify all descriptions on web page matching the pattern in the PageScraper object
    tags = structured_page.find_all('div', class_=re.compile(tag_pattern))
    for tag in tags:
        if contains in tag.text:
            yield tag


# TODO: write test
def locate_charity_info(tag, tag_names):
    """
    Given a Beautiful Soup tag, extracts the header, URL, and/or contents from that tag.
    :param tag: a bs4.element.Tag object which may contain a header, URL, and/or contents
    :param tag_names: the HTML tags denoting a header and/or contents (URL parsed separately)
    :return: header, url, text - the label, URL, and text on the page. If none, returns ''
    """

    header = ''
    url = ''
    text = ''
    header_tags = tag_names[0]
    content_tags = tag_names[1]
    # locate mission info
    queue = list(tag.children)
    while len(queue) != 0:
        element = queue.pop(0)
        if type(element) == bs4.element.Tag:
            if element.name in header_tags:
                # obtains the header title
                print(element.string.strip())
                # recursive function, return or recurse
            elif element.name in content_tags:
                # obtains the contents
                if element.string:
                    header = element.string.strip()
                # obtains the URL, if relevant
                elif element.find_all(id="orgSiteLink"):
                    url = element.a['href'].strip()
                # obtains the text within a tag
                else:
                    text = element.text.strip()
            else:
                for sublist in list(element.children):
                    queue.append(sublist)

    return header, url, text


# TODO: this is really ugly and might not work generally, make it general
# TODO: check out kjam's contact info parsing library
def parse_contact_info(contact_info_tag):
    """
    Parses contact info in a Beautiful Soup tag into its composite parts
    :param contact_info_tag: a string containing contact information
    :return: parsed contact information
    """
    info = {}
    lines = contact_info_tag.split('\n')
    lines = [ x.strip() for x in lines if x.strip() != '' ]
    info['name'] = lines[0]
    info['address'] = lines[1]
    info['city'] = lines[2][:-1]
    state, zip_code = lines[3].split()
    info['state'] = state
    info['zip'] = zip_code
    info['phone'] = lines[4][5:]
    info['fax'] = lines[5][5:]
    info['ein'] = lines[7][2:]
    print(info)

    return info


if __name__ == '__main__':

    # TODO: turn this into an actual function
    # read the file into beautiful soup format
    sys.path.insert(0, '/home/equinney/github/verbal-infusions')
    from hteaml_parser import read_soup

    pages = read_soup('cn_working.html')

    for page in pages:

        # get tags for the contact info and mission statement
        contact_info_generator = locate_tags(page, '(^rating$)', 'Charity Contact Info')
        mission_generator = locate_tags(page, '(^summaryBox cn-accordion-rating$)', 'Mission')
        contact_info_tag = next(contact_info_generator)
        mission_tag = next(mission_generator)

        # use the tags to get the text
        contact_label, charity_website, contact_info = locate_charity_info(contact_info_tag, ('h1', 'p'))
        mission_label, mission_website, mission_info = locate_charity_info(mission_tag, ('h1', 'p'))
        info_df = parse_contact_info(contact_info)

        # get info from the website tables, put into data frame
        df_list = pd.read_html(str(page))
        for index, frame in enumerate(df_list):
            print("Frame: ", index)
            print(frame)


    # TODO: parse all the tables produced by Pandas HTML function, squish into one
    # TODO: put all the data frames into one giant data frame that does what I want it to
    # namely, has columns for each relevant field and puts the info into those columns
    # then I want it to store that tuple into my postgres database which should have matching columns

    # append to the existing table 'charities'
    # don't write data frame index as a column
    #giant_data_frame.to_sql('charities', if_exists='append', index=False)

    # note: I need to create a SQLite table for this with columns for each relevant parameter
    # CREATE TABLE "tablename" ("col1", "dtype", "col2", "dtype", etc);
