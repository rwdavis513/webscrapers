import pandas as pd
import os
import requests
import unittest
from collections import OrderedDict
from bs4 import BeautifulSoup


def create_save_dir(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def scrape_page(url, save_folder='websites/'):

    items_to_find = [['a', ('data-tn-element', 'jobTitle')],
                     # ['a', ('data-tn-element', 'companyName')],
                     ['span', ('class', 'company')],
                     ['span', ('class', 'location')],
                     ['span', ('class', 'summary')]]

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    create_save_dir(save_folder)
    save_path = os.path.join(save_folder, os.path.basename(url))
    print(save_path)
    with open(save_path, 'w') as f:
        f.write(r.text)
    page_data = parse_page_info(soup, items_to_find=items_to_find)
    page_data.to_csv('job_list.csv')
    return page_data


def load_html_file(file_path):
    with open(file_path, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def find_items(section, element_type, *args, **kwargs):
    item = section.find(element_type, *args, **kwargs)
    if item:
        return item.get_text().strip()


def parse_page_info(soup, items_to_find=None):
    element_type, (tag, value) = 'div', ('class', 'result')
    info = []
    results = soup.find_all(element_type, {tag: value})
    if results:
        for section in results:
            job_block = section
            job_info = {}
            for element_type, (tag, value) in items_to_find:
                item = find_items(job_block, element_type, {tag: value})
                if item is None:
                    print(tag, value)
                    print(job_block)
                    print("\n\n----------------\n\n")
                job_info[value] = item
            info.append(job_info)
    return pd.DataFrame(info)


def download_job_links():
    # url = 'http://www.indeed.com/q-Data-Scientist-jobs.html'
    url = 'http://www.indeed.com/jobs?q=Data+Scientist&start=10&pp='
    df = scrape_page('http://www.indeed.com/jobs?q=Data+Scientist&start=20')
    print(df)


def compare_intersect(x, y):
    return frozenset(x).intersection(y)


class TestParsePage(unittest.TestCase):

    def setUp(self):
        self.items_to_find = [['a', ('data-tn-element', 'jobTitle')],
                     # ['a', ('data-tn-element', 'companyName')],
                     ['span', ('class', 'company')],
                     ['span', ('class', 'location')],
                     ['span', ('class', 'summary')]]
        # print(self.items_to_find)

    def test_find_items(self):
        item = find_items(load_html_file('tests/example_job_block.html'), 'a', {'data-tn-element': 'companyName'})
        assert item == 'Intel'
        item = find_items(load_html_file('tests/example_job_block.html'), 'span', {'class': 'location'})
        assert item == 'San Diego, CA 92129'

    def test_parse_page_info(self):
        soup = load_html_file('websites/q-Data-Scientist-jobs.html')
        page_info = parse_page_info(soup, self.items_to_find)
        assert compare_intersect(list(page_info.columns), ['jobTitle', 'company', 'location', 'summary'])

    def test_download_job_links(self):
        download_job_links()

if __name__ == "__main__":

    unittest.main()
