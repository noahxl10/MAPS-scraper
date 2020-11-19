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
import numpy as np
from numpy import random
import os
import os.path
from os import path
import json
import gspread
import pickle
import pprint
import logging
import pygsheets
from datetime import date, time, datetime, timedelta
from backports.datetime_fromisoformat import MonkeyPatch
import glob

# import scraper.constants as constant
## uncomment code below and comment above code when running locally
import constants as constant


MonkeyPatch.patch_fromisoformat()
logger = logging.getLogger('functions')


def initiate():

    folderSetup()
    fileSetup()

    client = pygsheets.authorize(service_file=constant.driveAPIpath())
    sh = client.open(constant.sheetFileName())
    wks = sh.updated[0:-1]

    last_sheet_revision = (datetime.fromisoformat(wks) - timedelta(0,6*60*60)).strftime('%Y-%m-%d %H:%M:%S') # - timedelta() to change timezone, essentially
    last_sheet_revision = datetime.strptime(last_sheet_revision, "%Y-%m-%d %H:%M:%S")

    present_time = datetime.now()

    fileR = open(constant.updatehistPath(), 'r')

    lines = [line for line in fileR]

    fileR.close()

    if lines[-1][-1] == '#':
        datacheck = 'nodata'

        
        updaterWriter()

    else:
        datacheck = 'data'
       
        lastupdate = datetime.strptime(lines[-1], "%Y-%m-%d %H:%M:%S")


    if datacheck =='data':
        if (lastupdate - last_sheet_revision).total_seconds() < 0:


            option = input('Google Sheet data is outdated. Would you like to update? ')
            if option in constant.userInpYesList():
                
                print('Deleting old Google sheets data...')

                googleUpdater()

                print('Done!')


            else:
                print('Keeping old data.')


            randomized = input('Would you like to update the randomzed SEARCHED set as well? ')
            if randomized in constant.userInpYesList():


                try:
                    googleMainFramePath = constant.picklePath() + '/google_maindf_randomset.pkl'
                    os.remove(googleMainFramePath)
                except Exception as e:
                    logger.exception(str(e))
                    print(str(e))

                try:
                    searchBuiltPath = constant.picklePath()+'/random_maindf_searchBuilder.pkl'
                    os.remove(searchBuiltPath)
                except Exception as e:
                    logger.exception(str(e))
                    print(str(e))

                try:
                    searchSetPath = constant.picklePath()+'/google_searchSet_randomset.pkl'
                    os.remove(searchSetPath)
                except Exception as e:
                    logger.exception(str(e))
                    print(str(e))


            else:
                print('Keeping old randomized set.')



## FUNCTIONS ##


def delete_all_pickles():
    for file in glob.glob('{}/*pkl'.format(constant.picklePath())):
        subs = file.split('/')
        if subs[-1] not in ['google_dfg.pkl', 'google_dfs.pkl', 'unwantedWords.pkl', 'wantedWords.pkl']:
            os.remove(file)



def export_pickles():
    file_list = ['/ALL_SEARCHES.pkl', '/TIMEDOUT_SEARCHES.pkl', '/PDF_URLS.pkl', '/FAILED_QUERIES.pkl']
    for file in file_list:
        try:
            df = pd.read_pickle('{}{}'.format(constant.picklePath(), file))
            file = file[0:-3] + 'csv'
            df.to_csv('{}{}'.format(constant.exportPath(), file))
        except Exception as e:
            print(str(e))



def clean_and_export():
    file_list = ['/ALL_SEARCHES.pkl','/TIMEDOUT_SEARCHES.pkl', '/PDF_URLS.pkl', '/FAILED_QUERIES.pkl']
    for file in file_list:
        try:
            df = pd.read_pickle('{}{}'.format(constant.picklePath(), file))
            file = file[0:-3] + 'csv'
            df.to_csv('{}{}'.format(constant.exportPath(), file))
        except Exception as e:
            print(str(e))
    try:
        df = pd.read_pickle(constant.picklePath()+'/ALL_SEARCHES.pkl')
        df = df.drop_duplicates(subset='context')
        df.to_csv('{}{}'.format(constant.exportPath(), '/ALL_SEARCHES_cleaned.csv'))
    except Exception as e:
        print(str(e))






def updaterWriter():
    fileW = open(constant.updatehistPath(), 'a')
    present_time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    fileW.write(('\n' + present_time))
    fileW.close()

def googleUpdater():

    updaterWriter()

    # Only removes unwantedWords and the fullset of main_df...Nothing else.
    try:
        unwantedWordsPath = constant.picklePath() + '/unwantedWords.pkl'
        os.remove(unwantedWordsPath)
    except Exception as e:
        logger.exception(str(e))
        print(str(e))

    try:
        google_dfg_path = '{}/google_dfg.pkl'.format(constant.picklePath())
        google_dfs_path = '{}/google_dfs.pkl'.format(constant.picklePath())
        os.remove(google_dfg_path)
        os.remove(google_dfs_path)
    except Exception as e:
        logger.exception(str(e))
        print(str(e))
    try:
        googleMainDFpath = constant.picklePath() + '/google_maindf_fullset.pkl'
        os.remove(googleMainDFpath)
    except Exception as e:
        logger.exception(str(e))
        print(str(e))

    try:
        googleSearchableSet = constant.picklePath()+'/google_searchSet.pkl'
        os.remove(googleSearchableSet)
    except Exception as e:
        logger.exception(str(e))
        print(str(e))

    try:
        searchSetBuilt = constant.picklePath()+'/normal_maindf_searchBuilder.pkl'
        os.remove(searchSetBuilt)
    except Exception as e:
        logger.exception(str(e))
        print(str(e))


def folderSetup():

    file = constant.dir_path()
    file = file+'/pickles'
    if os.path.exists(file) == True:
        print('config/pickles path exists.')
    if os.path.exists(file) != True:
        print('Creting config/pickles path...')
        os.mkdir(file)

    file = constant.dir_path()
    file = file+'/logs'
    if os.path.exists(file) == True:
        print('/logs path exists.')
    if os.path.exists(file) != True:
        print('Creting /logs path...')
        os.mkdir(file)


    file = constant.dir_path()
    file = file+'/export'
    if os.path.exists(file) == True:
        print('/export path exists.')
    if os.path.exists(file) != True:
        print('Creating /export path...')
        os.mkdir(file)



def fileSetup():

    dumpPath = constant.logPath() + '/dump.txt'
    updatehistPath = constant.configPath() + '/google_updatehist'


    with open(dumpPath, 'w') as fp: 
        print('created dump.txt file')
        pass

    if path.exists(updatehistPath) != True:
        with open(updatehistPath, 'w') as fp: 
            pass
            fp.write("## Keeps track of update history ##")
            print('re-wrote to google_updatehist file')



def pdfs_pickle(pdfsAR):
    pdfs_dict_toDF = {'pdf_url' : pdfsAR}
    pdfs_df = pd.DataFrame.from_dict(pdfs_dict_toDF)
    path = constant.pdfsPath()

    if os.path.exists(path) != True:
        pdfs_df.to_pickle(path)
    else:
        og_pdfs_df = pd.read_pickle(path)
        new_pdfs_df = og_pdfs_df.append(pdfs_df)
        #new_pdfs_df = new_pdfs_df.drop_duplicates(subset = 'pdf_url')
        pdfs_df.to_pickle(path)
    print('done with pdfs_pickle')


def failed_queries_pickle(df_of_failed_searches):
    path = constant.failedQueriesPath()

    if os.path.exists(path) != True:
        df_of_failed_searches.to_pickle(path)
    else:
        og_failed_searches = pd.read_pickle(path)
        new_failed_searches = og_failed_searches.append(df_of_failed_searches)
        new_failed_searches.to_pickle(path)


def unwantedWords():
    path = constant.picklePath() + '/unwantedWords.pkl'
    try:
        with open(path, 'rb') as file:
            data = pickle.load(file)
        return data

    except Exception as e:
        logger.error(str(e))
        data = GoogleSheetsUnwantedTerms()
        with open(path, "wb") as file:
            pickle.dump(data, file)
        return data


def searchBuilder(main_df, type_, numschools=None):
    # format: https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures
    

    if type_ == 'normal':
        if numschools != None:
            path = constant.picklePath() +'/{}_maindf_searchBuilder_{}_{}.pkl'.format(type_, numschools[0], numschools[1])
        else:
            path = constant.picklePath() +'/{}_maindf_searchBuilder.pkl'.format(type_)

        try:
            df = pd.read_pickle(path)
            return df

        except Exception as e:
        

            base = 'https://www.googleapis.com/customsearch/v1?key='
            mid1 = '&cx='
            cx = ''
            mid2 = '&exactTerms='
            #mid2 = '&q='
            urls = []
            
            for index, school in enumerate(main_df.school):
                search = " ".join([school, main_df['term'].iloc[index]])
                url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search])
                urls.append(url)
            main_df['searches'] = urls
            main_df.to_pickle(path)
            return main_df


    if type_ == 'random':

        path = constant.picklePath()+'/{}_maindf_searchBuilder.pkl'.format(type_)

        try:
            df = pd.read_pickle(path)
            return df

        except (OSError, IOError) as e:
            base = 'https://www.googleapis.com/customsearch/v1?key='
            mid1 = '&cx='
            cx = ''
            mid2 = '&q='
            urls = []
            for index, school in enumerate(main_df.school):
                search = " ".join([school, main_df['term'].iloc[index]])
                url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search])
                urls.append(url)
            main_df['searches'] = urls
            main_df.to_pickle(path)
            return main_df


    else:
        #raise NameError
        print('Name error raised for searchBuilder')



def searchBuilder_small(school, term):
    # format: https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures
    
    base = 'https://www.googleapis.com/customsearch/v1?key='
    mid1 = '&cx='
    cx = '12a4d10a30333b401'
    mid2 = '&q='
    urls = []

    search = " ".join([school, term])
    url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search])
    return url


def GET(url):
    return requests.get(url)   


def parser(response):
    content = response.json()
    try:
        hrefs = [i['link'] for i in content['items'][0:5] if i['link'][-3:] != 'pdf']
        pdfs = [i['link'] for i in content['items'][0:1] if i['link'][-3:] == 'pdf']
        hrefs = np.asarray(hrefs)
        return hrefs, pdfs
    except:
        return 'S', 'S'


def countQueries(cleanvars, dfs):
    count = 0
    for i in cleanvars:
        for j in i:
            count+=1
    numqueries = count * len(dfs.school_name)
    return numqueries


def saveDFloop(df, count, iterTime, genPath, saveParam):

    if count%saveParam==0:
        df.to_csv(genPath + '/data/tidyFrame.csv')
        print("{} rows saved.".format(count))


def cleanTerms(frametype, glossaryframe=None):

    if frametype == 'google':
        print('Google glossary')
        glossaryframe, schoolframe = GoogleSheetsReader()
        cleanterms = []
        for i in glossaryframe.terms:
            terms1 = []
            for k in i.split(","):
                terms1.append(re.sub('[”"“"“]', '', k.strip().lower()))
            cleanterms.append(terms1)
        return cleanterms
    
    else: #if isinstance(glossaryframe, pd.DataFrame):
        cleanterms = []
        print('File glossary')
        for i in glossaryframe.terms:
            terms1 = []
            for k in i.split(","):
                terms1.append(re.sub('[”"“"“]', '', k.strip().lower()))
            cleanterms.append(terms1)
    return cleanterms




def GoogleSheetsReader(portion_of_schools = None, sheetname = None):

        #portion_of_schools = [initial:endpoint]

        if sheetname == None:
            sheetname = constant.sheetFileName()
        else:
            sheetname = sheetname
        
        if portion_of_schools != None:
            print('Now re-writing dfs and dfg files...\n')

            os.remove(constant.googledfgPath())
            os.remove(constant.googledfsPath())

            creds = constant.driveAPIkey()
            client = gspread.authorize(creds)
            wholesheet = client.open(sheetname)

            glossary = wholesheet.get_worksheet(0)
            datag = glossary.get_all_records()
            dfg = pd.DataFrame.from_dict(datag)


            schools = wholesheet.get_worksheet(1)
            datas = schools.get_all_records()
            dfs = pd.DataFrame.from_dict(datas)[portion_of_schools[0]:portion_of_schools[1]]
            dfg.to_pickle(constant.googledfgPath())
            dfs.to_pickle(constant.googledfsPath())
            return dfg, dfs
        
        else:
            try:
                dfg = pd.read_pickle(constant.googledfgPath())
                dfs = pd.read_pickle(constant.googledfsPath())
                return dfg, dfs


            except (OSError, IOError) as e:

                creds = constant.driveAPIkey()
                client = gspread.authorize(creds)
                wholesheet = client.open(sheetname)

                glossary = wholesheet.get_worksheet(0)
                datag = glossary.get_all_records()  
                dfg = pd.DataFrame.from_dict(datag)


                schools = wholesheet.get_worksheet(1)
                datas = schools.get_all_records()  
                dfs = pd.DataFrame.from_dict(datas)
                dfg.to_pickle(constant.googledfgPath())
                dfs.to_pickle(constant.googledfsPath())

                return dfg, dfs


                


def GoogleSheetsUnwantedTerms():

        sheetname = 'API_Test'
        creds = constant.driveAPIkey()
        client = gspread.authorize(creds)
        wholesheet = client.open(sheetname)

        glossary = wholesheet.get_worksheet(2)
        datat = glossary.get_all_records()  
        dft = pd.DataFrame.from_dict(datat)

        cleaned = [re.sub('[”"“"“]', '', term.strip().lower()) for term in dft.unwanted_terms]

        return cleaned

def GoogleSheetsWantedTerms():
    
        sheetname = 'API_Test'
        creds = constant.driveAPIkey()
        client = gspread.authorize(creds)
        wholesheet = client.open(sheetname)

        glossary = wholesheet.get_worksheet(3)
        
        datat = glossary.get_all_records()  
        dft = pd.DataFrame.from_dict(datat)


        cleaned = [re.sub('[”"“"“]', '', term.strip().lower()) for term in dft.wanted_terms]

        return cleaned


def wantedWords():
    path = constant.picklePath() + '/wantedWords.pkl'
    try:
        with open(path, 'rb') as file:
            data = pickle.load(file)
        return data

    except Exception as e:
        logger.error(str(e))
        data = GoogleSheetsWantedTerms()
        with open(path, "wb") as file:
            pickle.dump(data, file)
        return data


def randomizer(dfs, dfg, cleanvars, length=None):

    ## CUSTOM FOR 10/20/2020 RUN ##

    # say "True" if you want all terms/variables, but still random schools
    # sat False if you want random terms and variables AND random schools
    randschools_allvars = True

    ## END ## 

    print('Creating randomized test frame from Google. \n')
    path = constant.dir_path()+'/pickles/google_maindf_{}.pkl'.format('randomset')
    
  
    if os.path.exists(path) == True:
        inp = input('Would you like to use old random searchable file?')
        if inp in ['No', 'no']:
            os.remove(path)
      
            df = pd.read_pickle(path)
            

        elif inp in ['Yes', 'yes']:
            df = pd.read_pickle(path)
            print('Successfully pulled in old randomized set.\n')
            return df

    
    else:
        


        print('Creating new randomized set.\n')   

        if length == None:
            length = 50
        if length != None:
            length = length


        unitID = dfs.unit_id

        # len() -1 so that it captures ONLY schools, not an extra row
        schoolindexes = random.randint( low=0, high = (len(dfs.school_name)-1), 
            size = length )  #int(len(dfs.school_name)/10)



        schools_rand = [dfs.school_name[i] for i in schoolindexes]



        varindexes = random.randint(low=0, high = (len(dfg.varname)-1), 
            size = length) #int(len(dfs.school_name)/10)
        


        if randschools_allvars == True:
            variables_rand = dfg.varname #[dfg.varname[i] for i in varindexes]
            terms_rand =  cleanvars 

        else: 
            variables_rand = [dfg.varname[i] for i in varindexes]
            terms_rand = [cleanvars[i] for i in varindexes]



        print(variables_rand)
        

        unit_ID, schools, variables, terms = [ [] for i in range(4) ]

        for schoolIndex, school in enumerate(schools_rand):
            for varIndex, variable in enumerate(variables_rand):
                for term in terms_rand[varIndex]:

                        unit_ID.append(unitID[schoolIndex])
                        schools.append(school)
                        variables.append(variable)
                        terms.append(term)

        df = pd.DataFrame.from_dict(
                    {'unit_ID':unit_ID,
                    'school': schools,
                    'variable': variables,
                    'term': terms})

        df.to_pickle(path)
        
        return df




def create_main_df(dfs, dfg, cleanterms, dataset=None, frametype=None, numschools=None):

    # Options for frametype are either "file" or "google"
    # Options for datset are 'tinyset', 'smallset','mediumset'

    if frametype != None:
        print('Creating google main frame')
        if numschools != None:
            path = constant.picklePath()+'/google_maindf_{}_{}.pkl'.format(numschools[0], numschools[1])
            dfs = dfs[numschools[0]:numschools[1]]
            dfs = dfs.reset_index()
            dfs = dfs.drop(columns='index')


        else:
            print('Creating google main frame')
            path = constant.picklePath()+'/google_maindf_fullset.pkl'


        try:
            df = pd.read_pickle(path)
            #print(df)
            return df

        except Exception as e:
            print(dfs)

            unit_ID, schools, variables, terms = [ [] for i in range(4) ]

            
            for schoolIndex, school in enumerate(dfs.school_name):
                for varIndex, variable in enumerate(dfg.varname):
                    for term in cleanterms[varIndex]:
                        unit_ID.append(dfs.unit_id[schoolIndex])
                        schools.append(school)
                        variables.append(variable)
                        terms.append(term)
            print('made it: 1')
            
            df = pd.DataFrame.from_dict(
                        {'unit_ID':unit_ID,
                        'school': schools,
                        'variable': variables,
                        'term': terms})

            df.to_pickle(path)
            return df


    if frametype == None:
        print('Creating test file main frame')
        path = constant.picklePath()+'/file_maindf_{}.pkl'.format(dataset)

        try:
            df = pd.read_pickle(path)
            return df

        except (OSError, IOError) as e:

            logger.exception(str(e))

            unit_ID, schools, variables, terms = [ [] for i in range(4) ]

            for schoolIndex, school in enumerate(dfs.school_name):
                for varIndex, variable in enumerate(dfg.varname):
                    for term in cleanterms[varIndex]:
                        
                        unit_ID.append(dfs.unit_id[schoolIndex])
                        schools.append(school)
                        variables.append(variable)
                        terms.append(term)

            df = pd.DataFrame.from_dict(
                        {'unit_ID':unit_ID,
                        'school': schools,
                        'variable': variables,
                        'term': terms})

            df.to_pickle(path)
            return df

def context_finder(pagetext, set_index):
    
    desired_sentences = 2

    num = desired_sentences + 1

    index = set_index
    period_count = 0
    while period_count != num:
        if pagetext[index] == '.':
                period_count+=1
        index +=1
        if index >= len(pagetext):
            period_count = num
        
        
    top_index = index


    period_count = 0
    index = set_index
    while period_count != num:
        if pagetext[index] == '.':
                period_count+=1
        index -=1
        if index <= 0:
            period_count = num
        

    bottom_index = index

    context_string = pagetext[bottom_index:top_index]
    return context_string



initiate()