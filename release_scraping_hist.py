### Script / functions for scraping the press releases

import bs4
import urllib3
import re
import util
import sys
import pandas as pd
import csv


fed_home_page = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
fed_hist_page = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"
FRAG = "https://www.federalreserve.gov"


def get_hist_links(link = fed_hist_page, min_year = 2006, max_year = 2007):
    '''
    Extracts links to Fed statements pre 2013

    Inputs:
        (str): url
        (float): earliest year
    Outputs:
        (list): links to statement, html version 
    '''
    soup = make_soup(link)
    a_links = soup.find_all('a')
    st_links =[]
    for a in a_links:
        if re.findall("/monetarypolicy/fomchistorical", a.get("href")) and float(a.text) >=  min_year and float(a.text) <= max_year: 
            mp_link = FRAG + a.get("href")
            soup  = make_soup(mp_link)
            links = soup.find_all('a')
            for a in links:
                if a.text == "Statement":
                    st_links.append(FRAG + a.get("href"))
    return st_links



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

def scrape_release_hist(link, dates, texts):
    '''
    Takes the URL to an individual press release 
    and an ongoing lists of the dates and texts, 
    scrapes the release date and text from that link's
    press release, and appends that information to the appropriate lists.

    Inputs:
        link: string of the URL to scrape
        dates: list of release dates
        texts: list of release text

    Outputs:
        dates: updated list of release dates
        texts: updated list with the links' text data
    '''

    pm = urllib3.PoolManager()
    html = pm.urlopen(url = link, method = "GET").data
    soup = bs4.BeautifulSoup(html, 'lxml')

    date = soup.find_all('p', class_ = "article__time")[0].text

    ptxt = ''
    text_divtag = soup.find_all('div', class_ = "col-xs-12 col-sm-8 col-md-8")[0]
    text_ptags = text_divtag.find_all('p')
    for ptag in text_ptags:
        if not ptag.find_all('a'):
            if not re.findall("Voting for the FOMC monetary policy action ",ptag.text): 
                ptxt += ptag.text
    ptxt = ptxt.strip()

    dates.append(date)
    texts.append(ptxt)
    
    return dates, texts


dates, texts, info = [], [], []
links = get_hist_links()
for link in links:
    scrape_release_hist(link, dates, texts)
for i in range(len(dates)):
    info.append((dates[i], texts[i].replace(",", " ")))

df = pd.DataFrame(info, columns=["date", "text"])
df.to_csv('texts06_07.csv')









