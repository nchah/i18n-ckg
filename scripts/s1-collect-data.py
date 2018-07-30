#!/usr/bin/env python3
# 
# Get strucuted data from web sources and output triples
# Usage:
# $ python3 s1-*.py
# 
# Note: Download the latest web driver at https://www.seleniumhq.org/download/
# May be necessary to add to path:
# $ export PATH=$PATH:/Users/nc/Code/nchah/i18n-ckg/geckodriver

import datetime
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


# Timestamp
utc_datetime0 = datetime.datetime.utcnow()
utc_datetime = utc_datetime0.strftime("%Y-%m-%d %H:%M:%S")
time_now = utc_datetime0.strftime("%Y-%m-%d_%H-%M-%S")

# Paths
geckodriver_path = open('webdriver-path.txt').read()


"""
# select1 = Select(driver.find_element_by_name('level'))
# select1.select_by_value('BLOCK')
# driver.find_element_by_id('button1').click()
# driver.implicitly_wait(10)  # Wait time in seconds
"""


def search_google(query):
    """ 
    return: final_dict: dict - key:values of structured data """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    url = 'https://www.google.com'
    driver.get(url)
    time.sleep(1.5)

    # Navigate to page and enter query
    input_query = driver.find_element_by_id('lst-ib')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)
    time.sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Properties have class attribute: w8qArf
    props = soup.findAll('span', {'class': 'w8qArf'})
    # Values have class attribute: LrzXr kno-fv
    vals = soup.findAll('span', {'class': 'LrzXr kno-fv'})

    # Create dict of property: values, preserving order
    final_dict = {}
    for p, v in zip(props, vals):
        prop = p.get_text().strip().replace(u'\xa0', u' ')
        prop = url[8:] + '/' + prop[:len(prop)-2]
        val = v.get_text().strip().replace(u'\xa0', u' ')
        final_dict[prop] = val
    # Done
    time.sleep(1.5)
    driver.close()
    return final_dict


def search_naver(query):
    """ 
    return: final_dict: dict - key:values of structured data """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    url = 'https://www.naver.com'
    driver.get(url)
    time.sleep(1.5)

    # Navigate to page and enter query
    input_query = driver.find_element_by_id('query')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)
    time.sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll('dl', {'class': 'detail_profile'})

    # Properties have tag: <dd>, excluding first one about description
    props = data[0].findAll('dt')
    # Values have tag: <dt>
    vals = data[0].findAll('dd')[1:]

    # Create dict of property: values, preserving order
    final_dict = {}
    for p, v in zip(props, vals):
        prop = url[8:] + '/' + p.get_text().replace(u'\xa0', u' ')
        val = v.get_text().replace(u'\xa0', u' ')
        final_dict[prop] = val
    # Done
    time.sleep(1.5)
    driver.close()
    return final_dict


def search_yandex(query):
    """ 
    return: final_dict: dict - key:values of structured data """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    # It's possible to set a URL paramete for RU language with &lang=ru
    # yet, it displays structured data in EN
    url = 'https://www.yandex.ru'
    driver.get(url)
    time.sleep(1.5)

    # Navigate to page and enter query
    input_query = driver.find_element_by_id('text')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)
    time.sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Properties have class attribute: 
    props = soup.findAll('b', {'class': 'key-value__item-title'})
    # Values have class attribute:
    vals = soup.findAll('span', {'class': 'key-value__item-value'})

    # Create dict of property: values, preserving order
    final_dict = {}
    for p, v in zip(props, vals):
        prop = p.get_text().replace(u'\xa0', u' ')
        prop = url[8:] + '/' + prop[:len(prop)-2]
        val = v.get_text().replace(u'\xa0', u' ')
        final_dict[prop] = val
    # Done
    time.sleep(1.5)
    driver.close()
    return final_dict


def search_baidu(query):
    """ 
    return: final_dict: dict - key:values of structured data """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    url = 'https://www.baidu.com'
    driver.get(url)
    time.sleep(1.5)

    # Navigate to page and enter query
    input_query = driver.find_element_by_id('kw')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)
    time.sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Properties and values are concatenated strings
    data = soup.findAll('div', {'class': 'c-span18 c-span-last'})
    data = data[0].findAll('p')

    # Create dict of property: values, preserving order
    final_dict = {}
    for prop_val in data:
        # Note the unicode character "：" != ":" 
        if '：' in prop_val.get_text():
            prop_val = prop_val.get_text().strip().split('：')
            prop = url[8:] + '/' + prop_val[0]
            val = prop_val[1]
            final_dict[prop] = val
    # Done
    time.sleep(1.5)
    driver.close()
    return final_dict


def search_wiki(query, url='https://en.wikipedia.org/'):
    """ This is a stop-gap measure in cases where static datasets
    are not able to cover more recent infobox data 
    (e.g. last DBpedia release was 2016-10).
    return: final_dict: dict - key:values of structured data """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    # url = ''
    driver.get(url)
    time.sleep(1.5)

    # Navigate to page and enter query
    input_query = driver.find_element_by_id('searchInput')
    input_query.send_keys(query)
    input_query.send_keys(Keys.ENTER)
    time.sleep(1.5)
    # Navigates to search results page
    top_result = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[3]/div/ul/li[1]/div[1]/a')
    top_result.click()
    time.sleep(1.5) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    """
    # * v1 method
    # Properties and values 
    data = soup.findAll('table', {'class': 'infobox biography vcard'})
    props = data[0].findAll('th')
    vals = data[0].findAll('td')

    # Create dict of property: values, preserving order
    final_dict = {}
    for p, v in zip(props, vals):
        prop = p.get_text().strip().replace(u'\xa0', u' ')
        prop = url[8:] + '/' + prop[:len(prop)-2]
        val = v.get_text().strip().replace(u'\xa0', u' ')
        final_dict[prop] = val
    """
    # * v2 method
    # future methods may just parse WP source, or adapt other extraction frameworks
    data = soup.findAll('table', {'class': 'infobox biography vcard'})
    tr = data[0].findAll('tr')

    final_dict = {}
    for i in range(1, len(tr)):  # Skip first
        if tr[i]:  # only non-blank 'key' in pair
            try:
                prop = tr[i].th.get_text()
                val  = tr[i].td.get_text()
                final_dict[prop] = val
            except AttributeError:
                pass
    # Done
    time.sleep(1.5)
    driver.close()
    return final_dict


def write_triples(filename, write_data):
    """ Create triples (S, P, O) and write to file
    return: None """
    with open(filename, 'a') as f1:
        f1.write(write_data)


def main():
    """ Main script operations
    return: None """
    # Setting empty default dicts
    final_google, final_naver, final_yandex, final_baidu = {}, {}, {}, {}

    # Parse query text file
    queries = open('test-query.csv').readlines()
    for q in queries:
        entity = q.split(',')[0]
        site = q.split(',')[1].strip()
        # Each search site requires a custom approach
        if site == 'google.com':
            final_google = search_google(entity)
            final_wiki_en = search_wiki(entity, 'https://en.wikipedia.org/')
        if site == 'naver.com':
            final_naver  = search_naver(entity)
            final_wiki_ko = search_wiki(entity, 'https://ko.wikipedia.org/')
        if site == 'yandex.ru':
            final_yandex = search_yandex(entity)
            final_wiki_ru = search_wiki(entity, 'https://ru.wikipedia.org/')
        if site == "baidu.com":
            final_baidu  = search_baidu(entity)
            final_wiki_zh = search_wiki(entity, 'https://zh.wikipedia.org/')

    # Create triples (S, P, O) and write to file
    output_file = 'output-' + time_now
    # Iterate over the datasets and within each dataset
    final_sets = [final_google, final_naver, final_yandex, final_baidu
                  final_wiki_en, final_wiki_ko, final_wiki_ru, final_wiki_zh]
    for final_set in final_sets:
        for prop in final_set:
            # Subject portion is hardcoded for current implementation
            triple = 'Rain_(entertainer)' + '\t' + prop + '\t' + final_set[prop] + '\n'
            write_triples(output_file, triple)
    # Done


if __name__ == "__main__":
    main()
