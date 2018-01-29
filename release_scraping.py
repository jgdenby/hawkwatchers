
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
	
	

#textdf = pd.DataFrame({'date': [date], 'release_text': [texts]})





