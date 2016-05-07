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

def loadListingInfo(myURL):
    
    r = requests.get(myURL)
    soup = BeautifulSoup(r.text,'html.parser')

    myAddress = soup.find(itemprop="streetAddress").get_text() + ", " + soup.find(itemprop="addressLocality").get_text()
    myPrice = soup.find(itemprop="price").get_text()
    myPhone = soup.find(itemprop="telephone").get_text()

    return({'address':myAddress.strip(),'price':myPrice.strip(),'phone':myPhone.strip()})
    

def loadAllListings(URLs):
    
    allListings = pd.DataFrame(columns=['address','price','phone'])

    for myURL in URLs:    
        try:
            listingInfo = loadListingInfo(myURL)
            allListings = allListings.append(listingInfo,ignore_index=True)
            print(allListings)
        except:
            print('Failed to Load listing at ' + myURL)
        
        time.sleep(1)            
    
    return(allListings)


if __name__ == "__main__":
    os.chdir('C:/Users/Bob/Documents/Business/Real Estate')
    
    baseURL = 'https://www.rentler.com/listings?maxprice=650&ne.lat=40.29076056513011&ne.lon=-111.57613623906252&sw.lat=40.17687915713456&sw.lon=-111.74093116093752'    
    
    URLs = ['https://www.rentler.com/listings/ut/spanish-fork/apartments/24666/r163924',
            'https://www.rentler.com/listings/ut/provo/apartments/23179/r1261770',
            'https://www.rentler.com/listings/ut/provo/multi-family-homes/r737192',
            'https://www.rentler.com/listings/ut/spanish-fork/apartments/r1527621',
            'https://www.rentler.com/listings/ut/provo/subleases/r1527588',
            'https://www.rentler.com/listings/ut/provo/condos-townhomes/r1238222',
            'https://www.rentler.com/listings/ut/springville/apartments/118685/r1314190',
            'https://www.rentler.com/listings/ut/provo/apartments/19077/r222730',
            'https://www.rentler.com/listings/ut/springville/single-family-homes/18926/r1205348']

    URLs = ['https://www.rentler.com/listings/ut/provo/apartments/13998/r1151225',
            'https://www.rentler.com/listings/ut/springville/manufactured-homes/r1507017']
    
    allListings = loadAllListings(URLs)
    allListings.to_csv('currentListings.csv')

    