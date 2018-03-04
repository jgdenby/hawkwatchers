### Script / functions for scraping the press releases

import bs4
import urllib3
import re
import util
import sys
import csv


fed_home_page = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
fed_hist_page = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"
FRAG = "https://www.federalreserve.gov"
HEADLINES = ["FRB: Press Release -- FOMC statement --" , "FRB: Press Release -- FOMC statement and Board discount rate action -- ",\
 "FRB: Press Release--FOMC statement and Board discount rate action--"]


def get_hist_links(link = fed_home_page, min_year = 2006, max_year = 2007, doc_type = "Statement"):
    '''
    Extracts links to Fed statements pre 2013

    Inputs:
        (str): url
        (float): earliest year
        (str) document wanted: "Statement", "Minutes", etc.
    Outputs:
        (list): links to statement, html version 
    '''
    doc_type = "Statement"
    soup = make_soup(link)
    a_links = soup.find_all('a')
    st_links = []
    for a in a_links:
        if re.findall("/monetarypolicy/fomchistorical", a.get("href")) and float(a.text) >= min_year and float(a.text) <= max_year: 
            mp_link = FRAG + a.get("href")
            soup  = make_soup(mp_link)
            links = soup.find_all('a')
            for a in links:
                if a.text == doc_type: 
                    st_links.append(FRAG + a.get("href"))
    ds_txts = []
    for link in st_links:
        soup = make_soup(link)
        date = soup.find_all('title')[0].text
        for h in HEADLINES:
            if h in date:
                date = date.replace(h , "")
        p = soup.find_all('p')
        txt =''
        for t in p:
            txt += t.text
        txt = txt.replace("\n", "")
        txt = txt.replace("\xa0", "")
        pair = [date, txt]

        ds_txts.append(pair)

    return ds_txts

def make_soup(url): 
    '''
    Makes a soup object from a html request object

    Inputs:
        request: a request object of the html 
    Outputs:
        soup - Soup object, if request is valid url. 
    '''
    req = util.get_request(url)
    html = util.read_request(req)
    if html is not None and html is not  "":
            soup = bs4.BeautifulSoup(html, "html5lib")
            return soup
    return None




