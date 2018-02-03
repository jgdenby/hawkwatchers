
### Script / functions for scraping the press releases

import bs4
import urllib3
import re
import pandas as pd


fed_home_page = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"


def scrape_release(link, dates, texts):
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

print(scrape_release(www.federalreserve.gov/newsevents/pressreleases/monetary20170201a.htm))

# 'Fed Statement Scraper
#
# 
#

import re
import util
import bs4
import queue
import json
import sys
import csv

INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                 'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])


# Helper Function 1

def make_soup(request): 
    '''
    Makes a soup object from a html request object

    Inputs:
        request: a request object of the html 
    Outputs:
        soup - Soup object, if request is valid url. 
    '''

    html = util.read_request(request)
    if html is not None and html is not  "":
            soup = bs4.BeautifulSoup(html, "html5lib")
            return soup

    return None

# Helper Function 2

def calendar_scraper(url, limiting_domain):
    '''
    Extracts links from a given url.

    Inputs:
        url - (string) url from which to get 
        limiting_domain: (string) that links must match
        visited_links: (list) of already visited sites 
    Outputs:
        links - list of strings, non-repetead and not previously visited
                links
        soup - soup object corresponding to visited url (to be used for 
                getting words)
    '''
    #A. Extracting links
    req = util.get_request(url)
    url2 = util.get_request_url(req)
    soup  = make_soup(req)
    
    if soup: 
        cal = []
        cal_list = soup.find_all("div",class_ = "panel panel_default" )
        for d in div_list:
            d_tr = util.remove_fragment(link.get("href")) 
            d_abs = util.convert_if_relative_url(url2, d_tr)
            if util.is_url_ok_to_follow(d_abs, limiting_domain):
                cal.append(d_abs)

        art = []
        art_list = soup.find_all("div",class_ = "panel panel_default" )
        for d in div_list:
            d_tr = util.remove_fragment(link.get("href")) 
            d_abs = util.convert_if_relative_url(url2, d_tr)
            if util.is_url_ok_to_follow(d_abs, limiting_domain):
                cal.append(d_abs)
    return cal, art

	
	

#textdf = pd.DataFrame({'date': [date], 'release_text': [texts]})





