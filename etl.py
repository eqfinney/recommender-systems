# normalizing HTML tables!

# normalize
# drop irrelevant data
# feed the result into Pandas

from selenium import webdriver
import pandas as pd

def process(url="https://www.charitynavigator.org/index.cfm?bay=search.summary&orgid=16012"):

    # page is HTML

    driver = webdriver.Firefox()
    driver.get(url)
    processed_page = driver.page_source

    return processed_page
# and then that processed page gets piped to charity_scraping module

if __name__ == '__main__':
    page = process()
    print(page)
    df_list = pd.read_html(str(page))
    #for index, frame in enumerate(df_list):
    #    print("Frame: ", index)
    #    print(frame)
