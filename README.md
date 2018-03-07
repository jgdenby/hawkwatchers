# hawkwatchers

__hawkwatchers__ is an interface allowing users to predict fluctuations in the US Federal interest rate based on the text of press releases.

## Getting Started
__hawkwatchers__ runs on [Django](https://www.djangoproject.com/) and makes use of a variety of [Python 3.6](https://docs.python.org/3/) packages.

1. [`pandas`](https://pandas.pydata.org/)
2. [`numpy`](http://www.numpy.org/)
3. [`scikit-learn`](http://scikit-learn.org/)
4. [`nltk`](http://www.nltk.org/)
5. [`pyenchant`](https://github.com/rfk/pyenchant)
6. [`beautiful_soup`](https://pypi.python.org/pypi/beautifulsoup4)
7. [`urllib3`](https://urllib3.readthedocs.io/en/latest/)

The following built-in modules are also used: `sys`, `re`, `math`, `csv`

All requisite packages can be installed as such:
```
$ pip install [package name]
```


## Authors
- Elena Badillo Goicoechea
- Natasha Mathur
- Joseph Denby

We are graduate students in the [CAPP](https://capp.uchicago.edu/) and [MACSS](https://macss.uchicago.edu/) programs at the University of Chicago. 

TODO:

- add instructions for:
    + scraping links/texts
    + nltk processing
    + scikit learn
    + nn_model
- add data cleaning code / description 

## Note on Modified Code

Code from outside sources was used in the following contexts and manners:

Web Scraping: We used the following util functions from files provided in course [CAPP 30122](https://classes.cs.uchicago.edu/archive/2018/winter/30122-1/index.html) as part of [PA #2](https://classes.cs.uchicago.edu/archive/2018/winter/30122-1/pa/pa2/index.html).
```python
>>> util.read_request()
>>> util.get_request()
```

 
Text Processing: . . . . . 

Website Construction:
 - We utilized code generated by Django  . . . . 
 - When creating the web pages we used code snippets from a [Bootstrap template](https://getbootstrap.com/docs/4.0/examples/cover/). 


## Data Collection

### Web Scraping

The press releases used were scraped from the [Federal Reserve](https://www.federalreserve.gov/default.htm). The releases are located in different locations and in different formats for [2013 - 2018](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) and for [pre-2013](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm). As such, we employed separate web scrapers and starting urls. 

`scraper/release_scraping.py` (Elena, Natasha, Joseph) (Original / Heavily Modified)

`scraper/release_scraping_hist.py` (Elena) (Heavily Modified)


`scraper/util.py` (Direct copy)

### Rate Sources

The effective federal funds rate was collected from the [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/series/FEDFUNDS). There is a period of time when the interest rate does not change. For that time range, the shadow interest rate calculated by Wu/Xia was used. It was sourced from the [Federal Reserve Bank of Atlanta](https://www.frbatlanta.org/cqer/research/shadow_rate.aspx?panel=1
).

`data/all_rates.csv`




The Labor Market Conditions Index was used to create a counterpoint to our model. The data was downloaded from the [Federal 
Reserve Bank of Kansas City](https://www.kansascityfed.org/research/indicatorsdata/lmci). 

`data/Labor_Conditions_Index.csv` 



### Combined Data

The data is consolidated in the following `.csv` files that were used to run the models. 

`data/allratesdf.csv` (Joseph) (Original)
- Contains Federal Funds rate data since Feb. 1994

`data/allreleasescleaned.csv` (Joseph) (Original)
- Contains press release text data since Feb. 1994

`data/allreleaserates.csv` (Joseph) (Original)
- Merged representation of above two datasets

## Model Construction

`nltk_processing.ipynb` (Joseph) (Heavily Modified)

The above notebook contains the code to clean and combine the DataFrames as well as several modeling techniques and methods of verification. 

The consolidated code used for the Django site is in the below file:

`hawkwatchers/hawksite/hawk_tracker/nn_model.py`  (Joseph) (Original)

## Website Construction

hawksite folder (Elena and Natasha) (Modified)

## Instructions to Run All Code

...
