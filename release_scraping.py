
### Script / functions for scraping the press releases

import bs4
import urllib3
import re
import pandas as pd
import util
import queue
import json
import sys
import csv


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

# 'Fed Statement Scraper
#
# 
#



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

def post2013_calendar_scraper(url):
    '''
    Extracts links from a given url.

    Inputs:
        url - (string) url from which to get 
    Outputs:
        links - list of strings, non-repetead and not previously visited
                links
        soup - soup object corresponding to visited url (to be used for 
                getting words)
    '''
    #A. Extracting links
    req = util.get_request(url)
    soup  = make_soup(req)
    home_page = "https://www.federalreserve.gov"
    
    if soup: 
        release_links = []
        tables_list = soup.find_all("div",class_ = "panel panel-default" )
        for t in tables_list:
            statement_list = t.find_all('div', 'col-xs-12 col-md-4 col-lg-2')
            for s in statement_list:
                a_list = s.find_all('a')
                if a_list:
                    if len(a_list) > 1:
                        for a in a_list:
                            if a.text == 'HTML':
                                link_abs = home_page + a['href']
                                #link_abs = util.convert_if_relative_url(a['href'],home_page)
                                release_links.append(link_abs)
                    else:
                        link_abs = home_page + a_list[0]['href']
                        #link_abs = util.convert_if_relative_url(a_list[0]['href'], home_page)
                        release_links.append(link_abs)

    return release_links
	
	

#textdf = pd.DataFrame({'date': [date], 'release_text': [texts]})





