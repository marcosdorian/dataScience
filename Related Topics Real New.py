import pytrends
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import json
import re

"""
In this project I automatized the search on Google for the trends and their related topics of the day hourly.
It gets the data, stores in a Json file and upgrades it automatically.
"""

#pip install pytrends

pytrends = TrendReq(hl='pt-br', tz=180, timeout=7)
#plt.style.use('ggplot')

def trend_search():
    result_df_today = pd.DataFrame()
    data = pytrends.trending_searches(pn='brazil')
    return data[0]

trend_search()

listaPalavras = [trend_search()]
cat = '0'
geo = 'BR'
gprop = ''
timeframe = ['today 1-y', 'today 6-m',
             'now 1-d', 'now 1-H']

num = range(1,1000)
specialChar = ["!", "@", "#", '$', "%", "¨", "&", "*", "+", "?", "^", "`", "´", ";", "...", num]

def char_remove(old, to_remove):
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, "")
        return new_string

def rel_topics0():
    dfResults = pd.DataFrame(None)
    search = trend_search()
    for palavra in search:
        palavra = char_remove(palavra, specialChar)
        pytrends.build_payload([palavra],
                               cat,
                               timeframe[3],
                               geo,
                               gprop)
        data = pytrends.related_topics()
        tryCount = 0
        if(len(data[palavra]['top']) == 0):
            while((len(data[palavra]['top']) == 0) and (tryCount < 5)):
                data = pytrends.related_topics()
                tryCount = tryCount + 1
            if (len(data[palavra]['top']) == 0):
                data[palavra]['top']=pd.DataFrame(data={}, columns=['value', 'formattedValue', 'hasData', 'link',
                                                                'topic_middle', 'topic_title', 'topic_type'])
            else:
                dfResults = pd.concat([dfResults, data[palavra]['top']['topic_title']], axis=1)
        else:
            dfResults= pd.concat([dfResults, data[palavra]['top']['topic_title']], axis=1)
            #print(data[palavra]['top']['topic_title'])
    dfResults.columns = search
    return dfResults


from datetime import datetime, timedelta, date
print(date.today())
print(datetime.today())

dfResults = rel_topics0()

def dicionario(dfResults):
    strToday = str(datetime.today())[0:16]
    dictResults = {}
    dictResults[strToday] = {}
    dfResults = dfResults.fillna("")
    for palavra in dfResults.columns:
        dictResults[strToday][palavra] = {}
        #for palavraRel in dfResults[palavra]:
            #dictResults["20/10/2022"]["Hora"][palavra][0] = palavraRel
        for i in range(len(dfResults[palavra])):
            dictResults[strToday][palavra][i] = dfResults[palavra][i]
    return dictResults

dicionario(dfResults)

"""with open("reportDay.json", 'w+') as jsonFile:
    jsonData = json.load(jsonFile)
    jsonData["20/10/2022"] = dicionario(dfResults)
    json.dump(jsonData, jsonFile, indent = 4) 
    jsonFile.close()"""
def write_json(filename='/home/rsa-key-20220916/GTrends/reportDay.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        #file_data["emp_details"] = {}
        # Join new_data with file_data inside emp_details
        file_data.update(dicionario(dfResults))
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

write_json()

