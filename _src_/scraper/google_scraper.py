import os
import csv
from parsel import Selector
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import requests
import time
import pandas as pd
import timeit
import plotly.express as px
import re
import itertools
import pickle
import numpy as np
import json
import pprint
from datetime import date, datetime, timedelta
import cProfile, pstats, io
from pstats import SortKey
import concurrent.futures
import logging
import context_finder
# import scraper.functions as function
# import scraper.constants as constant

## uncomment code below and comment above code when running locally
import functions as function
import constants as constant

logging.basicConfig(filename= '{}/logs/main.log'.format(constant.dir_path()), level=logging.DEBUG)
logger = logging.getLogger('scraper')






## python3 setup.py sdist bdist_wheel
## /Users/noahalex/Documents/Personal/Programming/Sorenson/MAPS_Scraper/main/versions/v1.6/MAPS
## twine upload --repository testpypi dist/*



pd.set_option('display.max_columns', None)




global hrefsAR
hrefsAR = []
global pdfsAR
pdfsAR = []
global parser_index
parser_index = []
global parser_urls
parser_urls = []
global parser_pagetexts
parser_pagetexts= []


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def search_parser(index):

    num = 8 #constant.num_urls_per_search() # number of websites to scrape off of google search

    url = main_df['searches'].iloc[index]

    response = requests.get(url)

    content = response.json()

    
    keys = [key for key in content]

    if keys[0] == 'error':
        logger.error(content['error'])
        
    temp_metatag = []

    try:
        ## IF YOU ONLY WANT WANTED WORDS:
        hrefs = [i['link'].lower() for i in content['items'][0:num] if (any(a in i['link'] for a in function.wantedWords()))]
     
        ## IF YOU WANT ALL WORDS EXCLUDING UNWANTED WORDS
        # hrefs = [i['link'].lower() for i in content['items'][0:num] if (not any(a in i['link'] for a in function.unwantedWords()))]
        
        if len(hrefs) == 0:
            hrefs = ['N']
        
        pdfs = [i['link'] for i in content['items'][0:num] if i['link'][-3:] == 'pdf']

        try:
            for j in content['items'][0:num]:

                metatags = j['pagemap']['metatags']
                metatag_date = [metatags[0][key] for key in metatags[0] if 'article:published_time' in key]

                if  len(metatag_date) > 0:
                    temp_metatag.append(metatag_date)
                else:
                    temp_metatag.append('No_meta_date')

            hrefsAR.append([main_df['unit_ID'].iloc[index], main_df['school'].iloc[index], main_df['variable'].iloc[index],main_df['term'].iloc[index], hrefs, temp_metatag])
            pdfsAR.append(pdfs)
        
        except Exception as e:
            print('Search_parser exception 1')
            print(e)
            logger.error(str(e))
            meta_dates = ['No_meta_date' for i in range(len(hrefs))]
            hrefsAR.append([main_df['unit_ID'].iloc[index], main_df['school'].iloc[index], main_df['variable'].iloc[index],main_df['term'].iloc[index], hrefs, meta_dates])
            pdfsAR.append(pdfs)

    except Exception as e:
        print('Search_parser exception 2')
        print(e)
        logger.error(str(e))

        hrefsAR.append([main_df['unit_ID'].iloc[index], main_df['school'].iloc[index], main_df['variable'].iloc[index], main_df['term'].iloc[index], 'S', 'S'])
        pdfsAR.append('S')
    time.sleep(.1)


def web_parser_page_scraper(search):
    
    url = search[1]
    source = requests.get(url, headers=constant.headers(), timeout = 1)
    #source = requests.get(url, headers=constant.headers())
    source.encoding = 'utf-8' 
    status = source.status_code
    source = source.text
    soup =  BeautifulSoup(source, 'lxml')
    text = soup.findAll(text=True)
    visibleText = filter(tag_visible, text)
    pagetext = " ".join(t.strip() for t in visibleText)
    pagetext = pagetext.replace('\xa0', ' ')

    # convert whole page to lowers to make it easier to parse
    pagetext = pagetext.lower()
    parser_pagetexts.append([ search[0], url, status, pagetext ])
    


def web_parser(search):

    url = search[1]

    
    logger.info(url)

    try: 
        web_parser_page_scraper(search)
    except Exception as e:
        logger.error(str(e))
        print(str(e))
        parser_pagetexts.append([ search[0], url, 'timeout', 'timeout' ])

    time.sleep(.1)


def downloader_SEARCH(indexes):

    threads = 25

    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        executor.map(search_parser, indexes)



def downloader_WEBPAGE(searches):
    
    threads = constant.num_threads()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        executor.map(web_parser, searches)




def main_threaded(test=None, numschools=None): 
    
    if test != None:
        path = constant.picklePath()+'/google_searchSet_randomset.pkl'

    elif numschools != None:
        path = constant.picklePath()+'/google_searchSet_{}_{}.pkl'.format(numschools[0], numschools[1])
    else:
        path = constant.picklePath()+'/google_searchSet_fullset.pkl'




    try:
        df = pd.read_pickle(path)
        print('Successfully pulled in old searchable set')
        
    except Exception as e:

        logger.exception(str(e))

        print('Creating new searchable set.')

        indexes = range(len(main_df.searches))
        # returns hrefsAR which is a global

        
        # hrefsPath = constant.picklePath() + '/hrefsAR.pkl'
        # if os.path.exists(hrefsPath) == True:
        #     with open(hrefsPath, 'rb') as f:
        #         hrefsAR = pickle.load(f)
        # else:
            
        #     print(hrefsAR)
        #     with open(hrefsPath, 'wb') as f:
        #         pickle.dump(hrefsAR, f)
            

        downloader_SEARCH(indexes)

        print('indexes length: ', len(indexes))
        print('hrefsAR length: ', len(hrefsAR))
        
        

        unit_ID, schools, variables, term, urls, indexes, searches_ar, metatag_dates = [ [] for i in range(8) ]

        specific_index = []
        count = 0
        print('made it 1')
        for array in hrefsAR:
            for index, url in enumerate(array[4]):
                specific_index.append(count)
                unit_ID.append(array[0])
                schools.append(array[1])
                variables.append(array[2])
                term.append(array[3])
                metatag_dates.append(array[5][index])
                urls.append(url)
                count+=1

        print('made it 2')
        # create dataframe to drop all duplicate/repeat websites before parsing to save time!
        df = pd.DataFrame.from_dict({
                                    'unit_ID':unit_ID,
                                    'school':schools,
                                    'variable': variables,
                                    'term': term,
                                    'url': urls,
                                    'metadata_date': metatag_dates
                                    })
        print('DF length before drop duplicates: ', len(df))

        df_failed_queries = df[df['url'] == 'S']
        function.failed_queries_pickle(df_failed_queries)

        

        df_success = df[df['url'] != 'S']
        df_success = df_success.drop_duplicates(subset = 'url')
        df = df_success

        
        print('DF length after drop duplicates: ', len(df))
        



        df = df.reset_index()
        df['index'] = df.index
        df.to_pickle(path)


    # this data frame is comprised of websites, terms, URLs and any important date metadata
    

    AllSearchesPath = constant.picklePath() + '/ALL_SEARCHES.pkl'

    try:
    
        aggregate_df = pd.read_pickle(AllSearchesPath)


        urls = list(aggregate_df.url)
        df = df[~df['url'].isin(urls)]
        df['index'] = [i for i in range(len(df.index))]
        

        print('After removing URLs already scraped, length of new DF to scrape: ', len(df))
        
        if len(df) == 0:
            print('No new URLs to scrape.')
            exit()

        df3 = part2(df)
        
        final_dataframe = part3(df3)
       
        
        timedout_urls_df = final_dataframe[final_dataframe['status_code'] == 'timeout' ]

        if len(timedout_urls_df) > 0:

            final_dataframe = final_dataframe[final_dataframe['status_code'] != 'timeout' ]
            #user_inp = input('Would you like to try scraping these again? (Say "no" if you just want to store them.)')
            timedoutPickleTryExcept(timedout_urls_df)

        
        new_pickle_df = aggregate_df.append(final_dataframe)
        new_pickle_df.to_pickle(AllSearchesPath)



    except Exception as e:
        print('No ALL_SEARCHES pickle.')
        logger.exception(str(e))
        df = df
       
        
        df3 = part2(df)
        final_dataframe = part3(df3)

        timedout_urls_df = final_dataframe[final_dataframe['status_code'] == 'timeout']

        if len(timedout_urls_df) > 0:

            final_dataframe = final_dataframe[final_dataframe['status_code'] != 'timeout']
            #user_inp = input('Would you like to try scraping these again? (Say "no" if you just want to store them.)')
            timedoutPickleTryExcept(timedout_urls_df)

        
        final_dataframe.to_pickle(AllSearchesPath)

        print('Saved final_dataframe as ALL_SEARCHES pickle')
        return final_dataframe



def timedoutPickleTryExcept(timedout_urls_df):
      
    TimedoutSearchesPath = constant.picklePath() + '/TIMEDOUT_SEARCHES.pkl'

    try:
        
        timedout_pickle_df = pd.read_pickle(TimedoutSearchesPath)

        pastURLs = list(timedout_pickle_df.url)

        timedout_urls_df = timedout_urls_df[~timedout_urls_df['url'].isin(pastURLs)]


        if len(timedout_urls_df)  ==  0:
            print('Timedout urls already added to TIMEDOUT_SEARCHES pickle')


        new_timedout_pickle_df = timedout_pickle_df.append(timedout_urls_df)

        new_timedout_pickle_df.to_pickle(TimedoutSearchesPath)

        print('Done appending final_dataframe to pickel path!')

    except (OSError, IOError) as e:
        timedout_urls_df.to_pickle(TimedoutSearchesPath)
        print('done creating timedout_urls_df pickle')


def part2(df):
    # build search_array in order to provide an easy method to match data when multiprocessing
    search_ar = [ [index, url] for index, url in enumerate(df.url) ]


    ## SECTION HERE TO ONLY DO URLS THAT HAVEN'T BEEN SCRAPED

    downloader_WEBPAGE(search_ar)
    # this returns parser_pagetexts, which is a global array 
    # It is only indexes, URLs, and status codes/pagetexts...
    # Because it doesn't have the other data (Terms, etc) we match the index with the old dataframe index!



    print('made it 2')

    df2 = pd.DataFrame.from_dict(
        {'index': [x[0] for x in parser_pagetexts],
        'url': [x[1] for x in parser_pagetexts],
        'date_originally_scraped': [datetime.now() for i in range(len(parser_pagetexts))],
        'status_code': [x[2] for x in parser_pagetexts],
        'pagetext': [x[3] for x in parser_pagetexts]
        })



    ## create dataframe that contains school, vars, terms, searches, 
    

    df3 = df.merge(df2, on='index')
    df3 = df3.drop(columns = ['url_y', 'index'])


    return df3




def part3(df3):

    unit_ID, schools, variables, terms, urls, count, context, pagetexts, metadata_dates, dates_originally_scraped, status_codes = [ [] for i in range(11) ]
    # parse through text in pagetext to find matching variables
    for i in df3.index:

        term = df3['term'].iloc[i]
        

        pagetext = str(df3['pagetext'].iloc[i])
        
        
        if pagetext.count(term) == 0:
            pagetexts.append(pagetext)
            terms.append(term)
            count_of_vars = 0
            contextString = 'NoContext'
            count.append(count_of_vars)

            context.append(contextString)

            urls.append(df3['url_x'].iloc[i])
            status_codes.append(df3['status_code'].iloc[i])
            schools.append(df3['school'].iloc[i])
            unit_ID.append(df3['unit_ID'].iloc[i])
            variables.append(df3['variable'].iloc[i])
            metadata_dates.append(df3['metadata_date'].iloc[i])
            dates_originally_scraped.append(df3['date_originally_scraped'].iloc[i])

        else:
            for num in [m.start() for m in re.finditer(term, pagetext)]:
                pagetexts.append(pagetext)
                terms.append(term)
                count_of_vars = 1
                urls.append(df3['url_x'].iloc[i])

                contextString = context_finder.context_finder(pagetext, num)
                count.append(count_of_vars)
                context.append(contextString)
                status_codes.append(df3['status_code'].iloc[i])
                schools.append(df3['school'].iloc[i])
                unit_ID.append(df3['unit_ID'].iloc[i])
                variables.append(df3['variable'].iloc[i])
                metadata_dates.append(df3['metadata_date'].iloc[i])
                dates_originally_scraped.append(df3['date_originally_scraped'].iloc[i])

    finaldict = {'unit_ID': unit_ID,
                'school': schools, 
                'term': terms,
                'variable': variables,
                'url': urls, 
                'status_code': status_codes,
                'metadata_date': metadata_dates,
                'date_originally_scraped':dates_originally_scraped,
                'count': count, 
                # 'pagetext':pagetexts, 
                'context': context} 


    final_dataframe = pd.DataFrame.from_dict(finaldict)

    # RETURNS DATA FRAME SORTED BY UNIT_ID FROM SMALLEST TO LARGEST
    final_dataframe = final_dataframe.sort_values(by=['unit_ID']) 
    
    return final_dataframe




def data_setup(random = None, numschools = None, length = None):


    dfg, dfs = function.GoogleSheetsReader()
    cleanterms = function.cleanTerms(frametype = 'google')


    ## Count number of queries
    numqueries = function.countQueries(cleanterms, dfs)
    print('Total number of queries in Google Sheet: ', numqueries)
    

    if random == None:
        print('normal run set')

        main_df = function.create_main_df(dfs, dfg, cleanterms, frametype='google', numschools=numschools)
        main_df = function.searchBuilder(main_df, 'normal', numschools=numschools)
        return main_df


    ## FOR RANDOM SET ##
    else:
        print('Random test set')
        if length != None:
            length = length
        else:
            length = 5

        main_rand_df = function.randomizer(dfs, dfg, cleanterms, length=length)
        print(main_rand_df)
        
        main_rand_df = function.searchBuilder(main_rand_df, 'random')

        return main_rand_df




def google_scraper(random = None, numschools = None, length = None, export=None):
    if numschools != None:
        if numschools[1] < numschools[0]:
            raise Exception('Second numschools index needs to be larger than first index!')

    pr = cProfile.Profile()
    pr.enable()
    start = time.time()
    global main_df


    
    
    if random != None:
        main_df = data_setup(random=True, length=length) 
        

        final_frame = main_threaded(test=True)
        if export != None:
            try:
                final_frame.to_csv('{}/random_final.csv'.format(constant.exportPath()))
            except Exception as e:
                print(str(e))
    else:
        main_df = data_setup(numschools=numschools) 
        
        final_frame = main_threaded(numschools=numschools)
        if export != None:
            try:
                final_frame.to_csv('{}/normal_final.csv'.format(constant.exportPath()))
            except Exception as e:
                print(str(e))


    function.pdfs_pickle(pdfsAR)
    

    end = time.time()
    print('Final time: ', round(end-start, 2))
    pr.disable()    
    ps = pstats.Stats(pr).sort_stats(SortKey.TIME)
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME)
    ps.dump_stats(constant.dumpPath())
    # convert to human readable format
    out_stream = open(constant.profilelogPath(), 'a')
    ps = pstats.Stats(constant.dumpPath(), stream=out_stream).sort_stats(SortKey.TIME)
    ps.print_stats(25)


google_scraper(random=True, length=8, export=True)

# 117 per school

function.export_pickles()