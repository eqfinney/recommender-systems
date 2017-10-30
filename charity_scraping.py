#
# Cleans the JSON file and scrapes the CN website for HTML data
#  Author: Emily Quinn Finney
#

import sys
sys.path.insert(0, '/home/equinney/github/web-scraping')
import web_crawler_main_class as webs
sys.path.insert(0, '/home/eqfinney/github/verbal-infusions')
#from hteaml_parser import read_soup


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


def locate_descriptive_text(structured_page, tag_pattern, tag_names, filename):
    """
    Given a page structured in a Beautiful Soup format, returns all descriptive text on page
    :param structured_page: list of web pages, structured in Beautiful Soup format
    :param tag_pattern: string, the HTML tag pattern for which to search
    :param tag_names: tuple of strings, the names of the relevant HTML tags to write
    :param filename: string, the name of the file to which to write the text
    :return: nothing, but should write a corpus of text to file
    """
    with open(filename, 'a') as f:
        # identify all descriptions on web page matching the pattern in the PageScraper object
        prod_description = structured_page.find_all('div', class_=re.compile(tag_pattern))
        # then go through them
        # this method is going to depend on the structure of the web page
        # so I'm not sure how I would generalize it
        for prod in prod_description:
            if prod['class'][0] == tag_names[0]:
                for element in prod:
                    if element.string:
                        f.write(element.string)
            elif prod['class'][0] == tag_names[1]:
                if prod.ul:
                    for child in prod.ul.children:
                        if child:
                            if child.string:
                                f.write(child.string)
            else:
                pass


if __name__ == '__main__':
    scrape_website(['https://www.charitynavigator.org/index.cfm?bay=search.alpha'])