import os
from oauth2client.service_account import ServiceAccountCredentials
import pickle
import logging 

logger = logging.getLogger('constants')

def dir_path():
    # return os.path.dirname(os.path.realpath(__file__))
    return os.path.dirname(__file__)

def headers():
    return {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}

def configPath():
    return dir_path()+'/config'

def exportPath():
    return dir_path() + '/export'

def searchAPIpath():
    return dir_path()+'/config/credentials'

def sheetFileName():
    name = "API_Test"
    return name

def userInpYesList():
    return ['Yes', 'Y', 'y', 'yes', 'ys', 'Yes ', 'yes ', ' yes', ' Yes']

def searchAPIkey():
    try: 
        for line in open(searchAPIpath()):
            if line[0:3]=='key':
              key = line[4:]
              return key
    except:
        raise NameError('Google Search API credential File does not exist.')

def driveAPIpath():
    return dir_path() + '/config/drive_creds.json'

def driveAPIscope():
    return ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive", 'https://www.googleapis.com/auth/drive.metadata.readonly']

def driveAPIkey():
    try: 
        creds = ServiceAccountCredentials.from_json_keyfile_name(driveAPIpath(), driveAPIscope())
        return creds
    except:
        raise NameError('Google Drive API credential file does not exist.')

def threadsPath():
    return configPath() + '/num_threads'


def numPerSearchPath():
    return configPath() + '/num_per_search'


def picklePath():
    return dir_path() + '/pickles'


def googledfgPath():
    return '{}/google_dfg.pkl'.format(picklePath())

def googledfsPath():
    return '{}/google_dfs.pkl'.format(picklePath())

def logPath():
    return dir_path() + '/logs'

def dumpPath():
    return logPath() + '/dump.txt'

def profilelogPath():
    return logPath() + '/profile.log'

def updatehistPath():
    return dir_path() + '/config/google_updatehist'

def update_threads():
    num_threads = int(input('Enter the desired number of threads: '))
    with open(threadsPath(), 'w') as fd:
            fd.writelines('threads={}'.format(num_threads))
    
def failedQueriesPath():
    return picklePath() + '/FAILED_QUERIES.pkl'


def num_threads():
    if os.path.exists(threadsPath()) != True:
        with open(threadsPath(), 'w') as fd:
            fd.writelines('threads=100')
        return 100

    else:
        with open(threadsPath(), 'r') as fd:
            lines = fd.readlines()
        return int(lines[0][8:])


def pdfsPath():
    return picklePath() + '/PDF_URLS.pkl'

def update_num_urls_per_search():
    num_per_search = int(input('Enter the desired number of urls per search: '))
    with open(numPerSearchPath(), 'w') as fd:
            fd.writelines('num={}'.format(num_per_search))


def num_urls_per_search():
    if os.path.exists(numPerSearchPath()) != True:
        with open(numPerSearchPath(), 'w') as fd:
            fd.writelines('num=5')
        return 5

    else:
        with open(numPerSearchPath(), 'r') as fd:
            lines = fd.readlines()
        return int(lines[0][4:])

