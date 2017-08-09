import os
import requests
import unittest
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from app.db_interface import DataBaseInterface

OUT_DIR = 'pdfs'


def pull_site(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content


def get_soup(page_content):
    return BeautifulSoup(page_content, 'html.parser')


def find_urls(page_content, base_url):
    href_list = get_soup(page_content).find_all('a')
    # url_list = [base_url + url.get('href') for url in href_list if url.get_text() == 'pdf']
    if href_list:
        url_list = [base_url + url.get('href') for url in href_list if url.get('href') if 'pdf' in url.get('href')]
    else:
        raise Exception("Error did not find links on page.")
    return url_list


def find_FDA_pages(page_content, base_url):
    href_list = get_soup(page_content).find_all('a')
    if href_list:
        url_list = [base_url + url.get('href') for url in href_list if 'Warning Letters' in url.get_text()
                                                                       and url.get_text()[-4:].isnumeric()]
    else:
        raise Exception("Error did not find links on page.")
    return url_list


def url_to_file_name(url):
    file_name = os.path.split(url)[-1]
    return file_name


def download_links(url_list, verbose=True):
    create_dir(OUT_DIR)
    for url in url_list:
        r = requests.get(url)
        if verbose:
            print("Downloading from:\n" + url)
        if r.status_code == 200:
            save_page_to_file(r.content, os.path.join(OUT_DIR, url_to_file_name(url)), binary=True)
            time.sleep(random.randint(1, 5))


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def save_page_to_file(page_content, file_name, binary=False):
    if binary:
        with open(file_name, 'wb') as f:
            f.write(page_content)
    else:
        with open(file_name, 'w') as f:
            f.write(page_content.decode('utf-8'))


def open_test_file(file_name):
    with open(file_name, 'r') as r:
        content = r.read()
    return content


def download_all_links_on_page(page, domain_name):
    url_list = find_urls(pull_site(page), domain_name)
    download_links(url_list)


def download_jmlr_papers():
    domain_name = 'http://www.jmlr.org'
    page = 'http://www.jmlr.org/papers/v16/'
    download_all_links_on_page(page, domain_name)


def download_fda_letters(domain_name, page):
    domain_name = 'http://www.fda.gov'
    page = 'http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/EnforcementActivitiesbyFDA/WarningLettersandNoticeofViolationLetterstoPharmaceuticalCompanies/ucm482462.htm'
    # content = pull_site(page)
    # url_list = find_urls(content, domain_name)
    download_all_links_on_page(page, domain_name)


def download_all_fda_letters():
    domain_name = 'http://www.fda.gov'
    page = 'http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/EnforcementActivitiesbyFDA/WarningLettersandNoticeofViolationLetterstoPharmaceuticalCompanies/ucm482462.htm'
    page_list = find_FDA_pages(pull_site(page), domain_name)
    for page in page_list[1:]:    # Skip the first page
        print('---------------')
        print(page)
        download_all_links_on_page(page, domain_name)


def get_drug_page_url(base_url, drug_name):
    search_link = base_url + '/dailymed/search.cfm?labeltype=all&query=' + drug_name
    page_content = pull_site(search_link)
    soup = get_soup(page_content)
    url_list = [l.get('href') for l in soup.find_all('a') if drug_name.lower() in l.get_text().lower()
                                                              and 'section' not in l.get('href')]
    if len(url_list) > 0:
        return base_url + url_list[0]
    else:
        print("Warning no urls found on search for page: " + search_link)


def get_link(soup, keyword):
    url_list = soup.find_all('a', keyword)
    # print(url_list)
    return url_list[0].get('href')


def find_product_label_links(base_url, drug_page_url):
    page_content = pull_site(drug_page_url)
    soup = get_soup(page_content)
    xml_link = base_url + get_link(soup, 'xml')
    pdf_link = base_url + get_link(soup, 'pdf')
    return pdf_link, xml_link


def download_drug_product_label(folder, drug_name):
    if not drug_name or type(drug_name) != str:
        raise KeyError("Error Missing drug name" + str(drug_name))
    file_name = None
    base_url = 'https://dailymed.nlm.nih.gov'
    drug_page_url = get_drug_page_url(base_url, drug_name)
    if drug_page_url:
        try:
            pdf_link, xml_link = find_product_label_links(base_url, drug_page_url)
            file_name = os.path.join(folder, drug_name + '_product_label.pdf')
            download_and_save_link(pdf_link, file_name)
        except Exception:
            print("Warning:: " + drug_name + " skipped due to incorrect page link.")
            print(drug_page_url)
    return file_name


def download_and_save_link(pdf_link, file_name, verbose=False):
    r = requests.get(pdf_link)
    if verbose:
        print("Downloading from:\n" + pdf_link)
    if r.status_code == 200:
        save_page_to_file(r.content, file_name, binary=True)
        time.sleep(random.randint(1, 5))


def get_drug_name(file_name):
    name = os.path.splitext(os.path.basename(file_name))[0].split()[0].lower()
    name = name.split('_')[0].split('-')[0]
    num_digits = sum([1 for c in name if c.isdigit()])
    if num_digits < 3:
        return name


def get_drug_names_to_download():
    dbi = DataBaseInterface()
    doc_table = dbi.load_data_from_table('doc_table')
    doc_table['drug_names'] = [get_drug_name(file_name) for file_name in doc_table['file_name']]
    doc_table['folder_path'] = doc_table['full_file_path'].apply(lambda x: os.path.dirname(x))
    drug_names = doc_table.set_index(['drug_names', 'folder_path'])['folder'].drop_duplicates().dropna()  # Get unique set
    drug_names = list(zip(drug_names.index.get_level_values(0), drug_names.index.get_level_values(1)))
    return drug_names


def download_drug_product_labels():
    print('\n')
    file_list = []
    drug_names = get_drug_names_to_download()
    for i, (drug_name, folder) in enumerate(drug_names):
        print(str(i) + ": " + folder)
        if type(drug_name) == str and os.path.exists(folder):
            file_name = download_drug_product_label(folder, drug_name)
            if file_name:
                file_list.append(os.path.join(folder, file_name))
        else:
            print("Warning: Skipped " + str(drug_name) + " due to not a string or folder not existing.")
    pd.DataFrame(file_list).to_csv('product_label_file-list.csv')


class TestPDFMiner(unittest.TestCase):

    def setUp(self):
        self.url = 'http://www.jmlr.org'
        self.file_name = 'jmlr_papers.html'
        self.page_content = open_test_file(self.file_name)
        self.url_list = ['http://www.jmlr.org/papers/volume16/chen15a/chen15a.pdf',
                         'http://www.jmlr.org/papers/volume16/yan15a/yan15a.pdf']

    def _test_pull_site(self):
        r = pull_site(self.url)
        assert type(r) == bytes
        save_page_to_file(r, self.file_name)

    def _find_urls(self):
        url_list = find_urls(self.page_content, self.url)
        assert type(url_list) == list

    def _url_to_file_name(self):
        test_str = 'http://www.jmlr.org/papers/v16/papers/volume16/chen15a/chen15a.pdf'
        file_name = url_to_file_name(test_str)
        assert file_name == 'chen15a.pdf'

    def _download_links(self):
        download_links(self.url_list)

    def test_run(self):
        download_jmlr_papers()

if __name__ == "__main__":
    # unittest.main(module='test_find_urls')
    # t = TestPDFMiner()
    # t.run()
    download_all_fda_letters()

