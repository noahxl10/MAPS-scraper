
from datetime import date
import pandas as pd 
import json
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import time








print('\n\n')
string = 'https://abcnews.go.com/Health/wireStory/california-biggest-jump-virus-cases-months-74117184?cid=clicksource_4380645_1_heads_hero_live_headlines_hed'
string1 = 'https://miamioh.edu/news/top-stories/30/5/2014/best-buddies-choir.html'
# source = requests.get(string1)



def urlDate(url):
    ########################################################
    
    #########################################################
    def getURLnumbers(url):
        splitURL = url.split('/')
        print(splitURL)
        count_of_dates = []
        dates = []

        list_of_numbers = []
        for index, item in enumerate(splitURL):
            try:
                element1 = int(splitURL[index])
            except:
                element1 = splitURL[index]
            # check to see if any of the items in the URL are numbers
            if isinstance(element1, int) == True:
                list_of_numbers.append(element1)
                    
        return list_of_numbers
    #####################
    def rearrange(numlist):

        numlist = sorted(numlist)

        if len(numlist) > 0:

            highest = numlist[-1]
   
            if highest > 2000 and highest < 2022:
                year = highest
                dates_dict = {'length':len(numlist), 'year':year}
            else:
                dates_dict = None
                return dates_dict
                
            
            if len(numlist) == 2:
                if numlist[-2] > 12 and numlist[-2] < 32:
                    day = numlist[-2]
                    dates_dict = {'length':len(numlist), 'year':year,'day':day}

                elif numlist[-2] < 32:
                    month_or_day = numlist[-2]
                    dates_dict = {'length':len(numlist), 'year':year,'month_or_day':month_or_day}
                else:
                    dates_dict = {'length':len(numlist), 'year':year}

                
            if len(numlist) == 3:
                if numlist[-2] > 12 and numlist[-2] < 32:
                    day = numlist[-2]
                    if numlist[-3] < 13:
                        month = numlist[-3]
                        dates_dict = {'length':len(numlist), 'year':year,'month':month, 'day':day}
                    else:
                        dates_dict = {'length':len(numlist), 'year':year,'day':day}
                
                elif numlist[-3] > 12 and numlist[-3] < 32:
                    day = numlist[-3]
                    if numlist[-2] < 13:
                        month = numlist[-3]
                        dates_dict = {'length':len(numlist), 'year':year,'month':month, 'day':day}
                    else:
                        dates_dict = {'length':len(numlist), 'year':year,'day':day}

                elif numlist[-2] < 32:
                    if numlist[-3] < 32:
                        month_or_day = [numlist[-2], numlist[-3]]
                        dates_dict = {'length':len(numlist), 'year':year,'month_or_day':month_or_day}
                    else:
                        month_or_day = numlist[-2]
                        dates_dict = {'length':len(numlist), 'year':year,'month_or_day':month_or_day}
                else:
                    dates_dict = {'length':len(numlist), 'year':year}

        
        else:
            dates_dict = None
            

        return dates_dict
        


    numlist = getURLnumbers(url)
    return rearrange(numlist)


        

df = pd.read_csv('/Users/noahalex/Documents/Personal/Programming/Sorenson/MAPS_Scraper/main/versions/v1.6/MAPS/src/scraper/ALL_SEARCHES.csv')

dates = []
print(len(df['url']))
for url in df['url']:
    date_dict = urlDate(url)
    dates.append(date_dict)
    
data = [df["url"]]

headers = ['url']

df3 = pd.concat(data, axis=1, keys=headers)
df3['dates'] = dates
df3.to_csv('/Users/noahalex/Documents/Personal/Programming/Sorenson/MAPS_Scraper/main/versions/v1.6/MAPS/src/scraper/date_filter_test.csv')


exit()












def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def metaTags(url):
    source = requests.get(url)
    source = source.text
    soup =  BeautifulSoup(source, 'lxml')
    results = soup.findAll('meta', property='lastPublishedDate')





title = soup.find("meta") #,  property="og:title")
print(title)

url = soup.find("meta",  property="og:url")

print(title["content"] if title else "No meta title given")
print(url["content"] if url else "No meta url given")
print('\n\n')
exit()
text = soup.findAll(text=True)
file = open('/Users/noahalex/Desktop/export/export.txt', 'w')
file.write(str(text))

# visibleText = filter(tag_visible, text)
# pagetext = " ".join(t.strip() for t in visibleText)
# pagetext = pagetext.replace('\xa0', ' ')

# # convert whole page to lowers to make it easier to parse
# pagetext = pagetext.lower()
# print(pagetext)

exit()

import pickle
import constants as constant
import json
# hrefsPath = constant.picklePath() + '/hrefsAR.pkl'
import requests
# with open(hrefsPath, 'rb') as f:
#     hrefsAR = pickle.load(f)
    
# print(hrefsAR)
# exit()
import google_scraper as gs 
import functions as function

pd.set_option('display.max_columns', None)

base = 'https://www.googleapis.com/customsearch/v1?key='
mid1 = '&cx='
cx = '12a4d10a30333b401'
mid2 = '&exactTerms='

mid3 = '&filter='
filter_ = '1' #1 removes duplicates
# mid4 = '&sort='
# sort_='date-date:r:20200301:20201101' #sorts by date (newest first!)
# :r:20200301:20201101

# mid5 = '&dateRestrict='
# datesrestrict_ = str("m[1]")
# mid6 = '&exactTerms='

school = 'university of utah'
term = 'tuition cost'

# &dateRestrict=&exactTerms=university%20of%20utah%20tuition%20cost

search = " ".join([school, term])
search = 'university%20of%20utah%20tuition%20cost'
search = 'university of utah tuition cost'
#url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search])
url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search, mid3, filter_])

print(url)

response = requests.get(url)

content = response.json()


json_formatted_str = json.dumps(content, indent=2)

print(json_formatted_str)


keys = [key for key in content]
hrefs = [i['link'].lower() for i in content['items'][0:8]]
print(hrefs)
exit()
hrefs = [i['link'].lower() for i in content['items'][0:8] if (any(a in i['link'] for a in function.wantedWords()))]
if len(hrefs) == 0:
    hrefs = ['N']
print(hrefs)

# Florida Agricultural and Mechanical University faculty cuts

# https://www.insidehighered.com/news/2011/01/04/minority_faculty_contest_depaul_tenure_denials?page=1



















# source = source.text
# soup =  BeautifulSoup(source, 'lxml')
# results = soup.findAll('meta') #, property='lastPublishedDate')



def labelDates(dates):
        endDict = {}
        for index, i in enumerate(dates):
            if i > 32: # check to make sure i is year
                endDict['year'] = i
                if len(dates) > 1:
                    if index == 0:
                        endDict['month'] = dates[index+1]
                        if len(dates) == 3:
                            endDict['day'] == dates[index+2]

                    if index == 1:
                        if len(dates) == 2:
                            endDict['month'] = dates[0]
                        if len(dates) == 3:
                            endDict['month_and_day'] = [dates[0], dates[2]]
                    if index == 2:
                        if dates[0] > 12:
                            endDict['day'] = dates[0]
                            endDict['month'] = dates[1]
                        if dates[1] > 12:
                            endDict['day'] = dates[1]
                            endDict['month'] = dates[0]
                        else:
                            endDict['month_and_day'] = [dates[0], dates[1]]
                
            return endDict