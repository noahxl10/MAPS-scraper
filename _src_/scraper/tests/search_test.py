
import pickle
import constants as constant
import json

import requests
from datetime import datetime
import pandas as pd

# import google_scraper as gs 
import functions as function


def toJulian(startdate,enddate):    
    sddays = datetime.fromisoformat(startdate).timetuple().tm_yday
    sdyear = datetime.fromisoformat(startdate).year
    sd= str(sdyear)[-2:]+str(sddays)
    eddays = datetime.fromisoformat(enddate).timetuple().tm_yday
    edyear = datetime.fromisoformat(enddate).year
    ed = str(edyear)[-2:]+str(eddays)
    return sd, ed

startdate, enddate=toJulian("2018-12-07","2019-09-08")


pd.set_option('display.max_columns', None)

base = 'https://www.googleapis.com/customsearch/v1?key='
mid1 = '&cx='
cx = '12a4d10a30333b401'
#mid2 = '&exactTerms='
mid2 = '&q='
mid3 = '&orTerms'
mid4 = '&num='
mid5 = '&start='
# mid3 = '&filter='
# filter_ = '1'  #1 removes duplicates



#search = '"Miami University" allintext:expand to adults site:insidehighered.com'
search = 'university' #daterange:{}-{}'.format(startdate,enddate)
search1 = 'university OR utah'
print(search)
search2 = 'utah'
#url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search])
url = "".join([base, constant.searchAPIkey().strip('\n'), mid1, cx, mid2, search1,  mid4, '10', mid5, '1'])

print(url)

response = requests.get(url)

content = response.json()


json_formatted_str = json.dumps(content, indent=2)

#print(json_formatted_str)


keys = [key for key in content]
hrefs = [i['link'].lower() for i in content['items'][0:8]]
print(hrefs)
exit()


mid4 = '&sort='
sort_='date-date:r:20200301:20201101' #sorts by date (newest first!)



# mid5 = '&dateRestrict='
# datesrestrict_ = "y[1]"
# # mid6 = '&exactTerms='






hrefs = [i['link'].lower() for i in content['items'][0:8] if (any(a in i['link'] for a in function.wantedWords()))]
if len(hrefs) == 0:
    hrefs = ['N']
print(hrefs)

# Florida Agricultural and Mechanical University faculty cuts

# https://www.insidehighered.com/news/2011/01/04/minority_faculty_contest_depaul_tenure_denials?page=1