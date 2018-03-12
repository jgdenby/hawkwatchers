# hawkwatchers

__hawkwatchers__ is an interface allowing users to predict fluctuations in the US Federal interest rate based on the text of press releases, helping them make more informed financial decisions.

## Getting Started
__hawkwatchers__ runs on [Django](https://www.djangoproject.com/) and makes use of a variety of [Python 3.6](https://docs.python.org/3/) packages.

1. [`pandas`](https://pandas.pydata.org/)
2. [`numpy`](http://www.numpy.org/)
3. [`scikit-learn`](http://scikit-learn.org/)
4. [`nltk`](http://www.nltk.org/)
5. [`pyenchant`](https://github.com/rfk/pyenchant)
6. [`beautifulsoup4`](https://pypi.python.org/pypi/beautifulsoup4)
7. [`urllib3`](https://urllib3.readthedocs.io/en/latest/)
8. [`django`](https://www.djangoproject.com/)

The following built-in modules are also used: `sys`, `re`, `math`, `csv`

All requisite packages can be installed as such:
```
$ pip install [package name]
```

After installing all requisite packages, run the following command within the home directory to view the Django site locally:
```
$ python3 hawksite/manage.py runserver
```

Then, type the following URL into your favorite browser to view the site!
`http://127.0.0.1:8000/hawk_tracker/`

## Authors
- Elena Badillo Goicoechea
- Natasha Mathur
- Joseph Denby

We are graduate students in the [CAPP](https://capp.uchicago.edu/) and [MACSS](https://macss.uchicago.edu/) programs at the University of Chicago. 


## Data Collection & Model Construction

### Web Scraping

The press releases used were scraped from the [Federal Reserve](https://www.federalreserve.gov/default.htm). The releases are located in different locations for [2013 - 2018](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) and for [pre-2013](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm), as well as in different formats between [pre-](https://www.federalreserve.gov/boarddocs/press/monetary/2005/20051213/) and [post-2006](https://www.federalreserve.gov/newsevents/pressreleases/monetary20060131a.htm). As such, we employed separate web scrapers functions and scripts. 

`scraper/scrape.py` 

`scraper/util.py` 

### Rate Sources

The effective federal funds rate was collected from the [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/series/FEDFUNDS). There is a period of time when the interest rate does not change; for that time range, the shadow interest rate calculated by [Wu/Xia](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2321323) was used. It was sourced from the [Federal Reserve Bank of Atlanta](https://www.frbatlanta.org/cqer/research/shadow_rate.aspx?panel=1). It is housed within `data/all_rates.csv`.

The [Labor Market Conditions Index](https://www.investopedia.com/articles/markets/113015/what-labor-market-conditions-index.asp) was used as a means of comparison to our text model. The data was downloaded from the [Federal 
Reserve Bank of Kansas City](https://www.kansascityfed.org/research/indicatorsdata/lmci). It is housed within `data/Labor_Conditions_Index.csv`.

### Model Construction

`nltk_processing.ipynb` 

The above notebook contains the code to clean and combine the aforementioned data sources, as well as several modeling techniques and methods of validation. 

The consolidated modeling code used for the Django site is outlined in the file below:

`hawkwatchers/hawksite/hawk_tracker/nn_model.py`  

## Instructions to Run All Code

### Link & Text Scraping

All functions/scripts relating to data collection via webscraping are contained within the `scraper` directory. 

Running the following command within that directory will scrape all relevant press releases (by aggregating links to press releases and scraping via the appropriate HTML format) and output the file `scrapeddata.csv`, which contains all Fed press releases since January 1994 paired with their release date:
```
$ python3 scrape.py
```

Ignore any `InsecureRequestWarning` error messages; they are merely a product of the scraping package used and are inconsequential for our purposes.

### Data Cleaning and Model Exploration
In `nltk_processing.ipynb` lives the code used to clean and aggregate the data scraped in the above step into a manageable format. Further, it contains code responsible for processing the text data and employing it to train a variety of classification models from `scikit-learn`, as well as code for assessing and validating those models (e.g., classification reports, LOOCV, Bootstrapping, etc.). It is not essential to the running of our Django site – it stands simply as a record of our data cleaning, EDA, and modeling thought processes. Anyone wishing to recreate the steps we took to achieve our final modeling decisions would find everything they need for this step within this file.

### Final Model & Website

All code related to the website is contained within the `hawksite` directory. To view the website locally, ensure that you have all requisite packages installed, then run the following command within that directory:
```
$ python3 manage.py runserver
```

Then, type the following URL into your favorite browser to view the site!
`http://127.0.0.1:8000/hawk_tracker/`
