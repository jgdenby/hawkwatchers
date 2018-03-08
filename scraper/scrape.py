import urllib.parse
import requests
import os
import bs4
import urllib3
import re
import pandas as pd
import queue
import json
import sys
import csv

FED_HOME_PAGE = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FED_HISTORICAL_PAGE = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"
FRAG = "https://www.federalreserve.gov"
# HEADLINES = ["FRB: Press Release -- FOMC statement --" , "FRB: Press Release -- FOMC statement and Board discount rate action -- ",\
#  "FRB: Press Release--FOMC statement and Board discount rate action--"]

def is_absolute_url(url):
    '''
    Is url an absolute URL?
    '''
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""

def get_request(url):
    '''
    Open a connection to the specified URL and if successful
    read the data.

    Inputs:
        url: must be an absolute URL

    Outputs:
        request object or None

    Examples:
        get_request("http://www.cs.uchicago.edu")
    '''

    if is_absolute_url(url):
        try:
            r = requests.get(url)
            if r.status_code == 404 or r.status_code == 403:
                r = None
        except Exception:
            # fail on any kind of error
            r = None
    else:
        r = None

    return r


def read_request(request):
    '''
    Return data from request object.  Returns result or "" if the read
    fails..
    '''

    try:
        return request.text.encode('iso-8859-1')
    except Exception:
        print("read failed: " + request.url)
        return ""


def get_request_url(request):
    '''
    Extract true URL from the request
    '''
    return request.url

def make_soup(link): 
    '''
    Makes a soup object from a html request object

    Inputs:
        request: a request object of the html 
    Outputs:
        soup - Soup object, if request is valid url. 
    '''
    request = get_request(link)
    html = read_request(request)
    if html is not None and html is not  "":
            soup = bs4.BeautifulSoup(html, "html5lib")
            return soup

    return None

def post2013_calendar_scraper(url = FED_HOME_PAGE):
    '''
    Extracts links from a given url.

    Inputs:
        url - (string) url from which to get links
    Outputs:
        links - list of strings, non-repeated and not previously visited
                links
    '''
    soup  = make_soup(url)
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
                                release_links.append(link_abs)
                    else:
                        link_abs = home_page + a_list[0]['href']
                        release_links.append(link_abs)

    return release_links


def get_hist_links(link = FED_HISTORICAL_PAGE, min_year = 1994, max_year = 2013):
    '''
    Extracts links to Fed statements pre 2013

    Inputs:
        link (str): url
        min_year (float): earliest year
        max_year (float): latest year

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


def scrape_release(link):
	'''
	Takes the URL to an individual press release 
	and an ongoing lists of the dates and texts, 
	scrapes the release date and text from that link's
	press release, and appends that information to the appropriate lists.

	Inputs:
		link: string of the URL to scrape
	
	Outputs:
		date: string of release date
		ptxt: string of release text
	'''

	pm = urllib3.PoolManager()
	html = pm.urlopen(url = link, method = "GET").data
	soup = bs4.BeautifulSoup(html, 'lxml')

	if soup.find_all('p', class_ = "article__time"):

		date = soup.find_all('p', class_ = "article__time")[0].text

		ptxt = ''
		text_divtag = soup.find_all('div', class_ = "col-xs-12 col-sm-8 col-md-8")[0]
		text_ptags = text_divtag.find_all('p')
		for ptag in text_ptags:
			if not ptag.find_all('a'):
				if not re.findall("Voting for the FOMC monetary policy action ",ptag.text): 
					ptxt += ptag.text
					ptxt = ptxt.strip()
					ptxt = ptxt.replace("\n", "")
					ptxt = ptxt.replace('\r', "")


	else:
		date = soup.find_all('title')[0].text
		date = re.findall(r'(\w+\s\d+,\s\d+)', date)[0]
		p = soup.find_all('p')
		ptxt =''
		for t in p:
			ptxt += t.text
			ptxt = ptxt.strip()
		ptxt = ptxt.replace("\n", "")
		ptxt = ptxt.replace('\r', "")
		ptxt = ptxt.replace("\xa0", "")
	
	return date, ptxt





if __name__ == "__main__":
	links = []
	links += get_hist_links()
	links += post2013_calendar_scraper()

	dates = []
	texts = []
	for l in links:
		ldate, ltxt = scrape_release(l)
		dates.append(ldate)
		texts.append(ltxt)

	df = pd.DataFrame({'date': dates, 'release_text':texts})
	df.to_csv('scrapeddata.csv')







