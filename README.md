## Welcome to Sorenson Impact Center MAPS Higher Education Scraper
#### -- a fully automated webapge scraper and parser using Google's Custom Search API -- 

### To install Python:

###### Go to https://www.python.org/downlexitoads/
###### Download the latest Python release version

#### Open a terminal (or a command editor)
#### Run

#### Then, to install the TEST algorithm: 
```
user$ pip install -i https://test.pypi.org/simple/ MAPS-test
```

######  (to install the actual algorithm:)
```
user$ pip install MAPS
```


# RUNNING THE PROGRAM
### Main function looks like: 
### google_scraper(random = None, numschools = None, length = None, export=None):
##### variable 'random' lets the program know whether to run a randomo sample or not
##### variable 'length' is how many schools and terms to sample
##### variable 'numschools' is a list-type of which index to start at and which index to finish at -> e.g. [0,30]

### Running for a random-sampled set of schools and terms:
```
user$ python

>>> from scraper import google_scraper as gs
>>> gs.google_scraper(random = True, length = 20)
```
### Running for a partitioned set of schools:
```
>>> gs.google_scraper(numschools = [0,35])
```
### note: 0, 35 will give index 0 through 34.

### Running for the full set of schools:
```
>>> gs.google_scraper()
```

### You have the ability to change some baseline variables, such as the number of threads or the number of urls per Google query
### Baseline threads = 100
### Baseline urls per search = 5
```
from scraper import constants as constant
# to update threads
constant.update_threads()

# to update URLs per Google query
constant.update_num_urls_per_search()

```

### To delete all pickled files:

```
from scraper import functions
functions.delete_all_pickles()
```


### To export pickled files:

```
functions.export_pickles()
```


### If you get an error, please send the log file to noah@sorensonimpact.com
##### You can find the log file by going to your Python root directory, into the MAPS files, into src -> logs -> main.log

# MAPS-scraper
# MAPS-scraper
