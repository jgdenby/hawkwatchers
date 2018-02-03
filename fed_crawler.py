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
  

def aux_words(main_t, d, plus, course_map_filename):
    '''
    Updates a word to course code dictionary given a courseblockmain tag

    Inputs:
        main_t - (string) url from which to get 
        d - (dictionary) to be updated
        plus - (string) corresponding to common information for courses
                in sequences. Empty strings if course is not part of a 
                sequence. 
        course_map_filename - (json file) maps course code to course id
    Outputs:
       d - updated dictionary
    '''
    c_map = json.load(open(course_map_filename))

    if (util.is_whitespace(main_t) == False):

        title = main_t.find("p", class_ = "courseblocktitle").text
        title = title.replace("\xa0", " ")
        title = title.replace("&#160", " ")
        course_code = re.search("\w+\s\d+", title).group()
        course_id = c_map[course_code]

        desc = main_t.find("p",  class_="courseblockdesc").text
        words = desc + " " +  title + " " + plus # for subsequences, includes
        # its course block's title and escription text
        words = words.replace("\n", "")
        words_l = re.findall("[a-zA-Z]\w*", words)
        for w in words_l:
            w = w .lower()
            if  w not in INDEX_IGNORE:    
                if w not in d: 
                    d[w] = []
                if course_id not in d[w]:
                    d[w].append(course_id)
    return d 

def extract_words(soup, d_words, course_map_filename):
    '''
    Updates a word to course code dictionary given a soup object for a 
    given url. Calls aux_words function for sequence and non-sequence 
    courses. 

    Inputs:
        soup - (soup) 
        d_words - (dictionary) to be updated
        course_map_filename - (json file) maps course code to course id
    Outputs:
        d_words - updated dictionary

    '''
    soup_div = soup.find_all("div",  class_="courseblock main")

    if len(soup_div) > 0: 
        for main in soup_div:
            if len(util.find_sequence(main)) > 0:
                plus = main.find("p", class_ = "courseblockdesc").text.lower()
                sub_courses = util.find_sequence(main)
                for sub in sub_courses:
                    d_words = aux_words(sub, d_words, plus, course_map_filename) 
            else: 
                d_words = aux_words(main, d_words, "", course_map_filename)

    return d_words


def crawl(url, limiting_domain, limit, course_map_filename):
    '''
    Takes a starting url and subsequently visits links that are found in that
    page and in the following visited ones. Updates a dictionary by mapping 
    words to course codes if information about courses is found in the 
    followed urls. 

    Inputs: 
        url - (string) url from which to get 
        limiting_domain: (string) that links must match
        limit: (int) total number of sites to be visited
        course_map_filename - (json file) maps course code 
                            to course id

    Outputs: 
        d_words - completed dictionary after crawl
    '''
    q = queue.Queue()
    visited_links = [url]
    d_words = {}
    q.put(url)
    count = 0
    while q.empty() == False and count <= limit: 
        links, soup = extract_site(q.get(), limiting_domain, visited_links)
        extract_words(soup, d_words, course_map_filename)
        if  len(links) == 0: 
            continue
        else: 
            for link in links:
                count += 1
                req = util.get_request(link)
                link2 = util.get_request_url(req)
                if link2 in visited_links:
                    continue
                q.put(link2)
                visited_links.append(link2)
                visited_links.append(link)
    return d_words

def output_csv(index, index_filename):
    '''
    Outputs index to csv file
    Inputs: 
        index - (dictionary) completed dictionary after crawl
        index_filename - file to which csv will be copied. 

    '''

    cells= []
    for x in index: 
        for y in index[x]: 
            cells.append((str(y) +"|"+ str(x)))
    f = open(index_filename,'w')
    for pair in cells:
        f.write(pair + "\n")
    f.close()


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs:
        CSV file of the index index.
    '''

    starting_url = ("http://www.classes.cs.uchicago.edu/archive/2015/winter"
                    "/12200-1/new.collegecatalog.uchicago.edu/index.html")
    limiting_domain = "classes.cs.uchicago.edu"
    index = crawl(starting_url, limiting_domain, num_pages_to_crawl, \
        course_map_filename)
    output_csv(index, index_filename)


if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    go(num_pages_to_crawl, course_map_filename, index_filename)
