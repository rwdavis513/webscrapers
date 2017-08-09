# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:29:48 2015

@author: Bob
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from time import sleep
import random


def parse_page_info(soup, items_to_find):
    
    data = pd.DataFrame(columns=items_to_find.keys())
    alist = soup.find_all("a", class_="business-name")
    for section in alist:
        #print(section.get_text())
        business_section = section.parent.parent
        business_info = extract_section_info(business_section, items_to_find)
        data = data.append(business_info, ignore_index=True)
        
    return data


def extract_section_info(info, items_to_find, verbose=False):
    results = {}
    for item, header in items_to_find.items():
        try:
            if header == 'itemprop':
                results[item] = info.find(itemprop=item).get_text()
            else:
                if 'website' in item:
                    results[item] = info.find(class_=item).get('href')
                else:
                    results[item] = info.find(class_=item).get_text()
        except:
            if verbose:
                print("Warning: " + item + " was not found.")
            
    return results


def scrape_page(city, state, search_item='conference+management'):
    base_url = 'http://www.yellowpages.com/search?search_terms='
    where = 'geo_location_terms=' + city + '+' + state
    #print(where)
    
    URL = base_url + search_item + '&' + where
    URL = URL.replace(" ", "%20")
    #print(URL)
    
    items_to_find = {'business-name':'class_', 'telephone':'itemprop',
                     'streetAddress':'itemprop', 'addressLocality':'itemprop',
                     'addressRegion':'itemprop', 'postalCode':'itemprop', 
                     'track-visit-website':'class_'}
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.text,'html.parser')
    with open('websites/' + state +'_' + city + '.html', 'w') as f:
        f.write(r.text)
    page_data = parse_page_info(soup, items_to_find)
    page_data.to_csv(state + '_' + city + '.csv')
    return page_data


def load_cities():
    city_list = pd.read_csv('census_population_short.csv')
    for i in range(city_list[['NAME','STNAME']].shape[0]):
    #for i in range(4,5):
        print(city_list['NAME'].ix[i], city_list['STNAME'].ix[i])
        if 'city_data' not in locals():
            city_data = scrape_page(city_list['NAME'][i], city_list['STNAME'][i])
        else:
            new = scrape_page(city_list['NAME'][i], city_list['STNAME'][i])
            city_data = pd.concat([city_data, new])
        sleep(random.randint(30,80))
    city_data.to_csv('all.csv')
    return city_data
                     
if __name__ == "__main__":
    scrape_page()

    