#import libraries
import requests
import pprint
import pathlib
import pickle
import re
import time
import csv
import pandas as pd

#sets up the path to where the keywords pickle file are held
path = pathlib.Path("C:/Users/sguru/Documents/Python_Scripts")
#for obama
keywords_obama = path/"keywords_obama"
#checks to see if the file has been made already. If not, it creates it 
if not pathlib.Path(keywords_obama).is_dir():
    keywords_obama.mkdir()

#for trump
keywords_trump = path/"keywords_trump"
if not pathlib.Path(keywords_trump).is_dir():
    keywords_trump.mkdir()

#sets API variables
KEY = 'CVwEh1GLlXGki8GbHlfZnOD2KGPGJsi4'
url ='https://api.nytimes.com/svc/search/v2/articlesearch.json'

#creating parameters
parameters = {'q':'pollution+environment','api-key': KEY}

#creating new parameters
filter = 'document_type:("article") AND section_name:("U.S.")'

#updating parameters
parameters['fq']=filter

#obama's 1st term start and end date
parameters['being_date']='20090120'
parameters['end_date']='20130120'

parameters['page']=0


print("\n This is for Obama: \n")
print(parameters)

#gets all the matches for the parameters I have set in place and sets them into a json file

response = requests.get(url,params=parameters)
content = response.json()

print(content['response']['meta']['hits'])


# loads the keywords into pickle files
# iterate over 10 pages
for i in range(10):
    try:
        #sets up the naming system and parameters to which the data will be pulled in 
        pagenum = i
        filename = f"keywords_page{pagenum}"
        #creates a list for each page
        for docs in content['response']['docs']:
            key_list = []
            #appends the values to the list
            for key in docs['keywords']:
                key_list.append(key['value'])
            #creates and puts the values from the list into the specified file location 
            with open(f"C:/Users/sguru/Documents/Python_Scripts/keywords_obama/{filename}","wb") as p_file:
                pickle.dump(key_list, p_file)
    except:
        break

#creates a list for all the keywords being used
allkeywordsO = []

#iterates through the directory to unpickle the pickle files so that the files have human readable keywords
for i in keywords_obama.iterdir():
    with open(i, 'rb') as keyfile:
        kwl = pickle.load(keyfile)  
        for keywords in kwl:
            allkeywordsO.append(keywords)

print(allkeywordsO)

#creates a list to where more refined keywords will be placed
pollution_listO = []
regex_list = ["Pollution","Toxic","Waste"]
for refinedkeys in allkeywordsO:
    for x in regex_list:
        if re.findall(x,refinedkeys):
            pollution_listO.append(refinedkeys)

print(pollution_listO)

#creates a list such that the keywords are not repeated
clean_pollution_listO = []
clean_pollution_listO = set(pollution_listO)
print(clean_pollution_listO)

#creates a method that will look up the articles with these keywords and give us the amount of times each pollution topic was written about
def article_number(article_keyword):
    parameters['q'] = article_keyword
    response = requests.get(url,params=parameters)
    content = response.json()
    return content['response']['meta']['hits']

#creates lists to which the results will be saved
resultsO_section = []
resultsO_hits = []

#iterates through the clear pollution list. For each section specifiied, it hits the API and retreives the amount of hits that keyword has gotten
for p in clean_pollution_listO:
    result_section = (f"{p}")
    result_hits = (f"{article_number(p)}")
    resultsO_section.append(result_section)
    resultsO_hits.append(result_hits)
    time.sleep(4)

print(resultsO_section)
print(resultsO_hits)

#converts the resulting lists from above into a dataframe
dfO = pd.DataFrame(list(zip(resultsO_section, resultsO_hits)), columns = ["Section","Hits"])

print(dfO)

#checks to see if the file does not exist then saves the results into a csv file
if not pathlib.Path("obama_results.csv").is_file():
    dfO.to_csv("C:/Users/sguru/Documents/Python_Scripts/obama_results.csv", index=False)
else:
    print("file already exists")






#everything below is the same as above but with variables changed to fit trump
parameters = {'q':'pollution+environment','api-key': KEY}

filter = 'document_type:("article") AND section_name:("U.S.")'

parameters['fq']=filter

#trump's 1st term start and end date
parameters['being_date']='20170120'
parameters['end_date']='20210120'

parameters['page']=0


print("\n \n \nThis is for Trump: \n")
print(parameters)


response = requests.get(url,params=parameters)
content = response.json()

print(content['response']['meta']['hits'])

for i in range(10):
    try:
        pagenum = i
        filename = f"keywords_page{pagenum}"
        for docs in content['response']['docs']:
            key_list = []
            for key in docs['keywords']:
                key_list.append(key['value'])
            with open(f"C:/Users/sguru/Documents/Python_Scripts/keywords_trump/{filename}","wb") as p_file:
                pickle.dump(key_list, p_file)
    except:
        break

allkeywordsT = []


for i in keywords_trump.iterdir():
    with open(i, 'rb') as keyfile:
        kwl = pickle.load(keyfile)  
        for keywords in kwl:
            allkeywordsT.append(keywords)

print(allkeywordsT)

pollution_listT = []
regex_list = ["Pollution","Toxic","Waste"]
for refinedkeys in allkeywordsT:
    for x in regex_list:
        if re.findall(x,refinedkeys):
            pollution_listT.append(refinedkeys)

print(pollution_listT)

clean_pollution_listT = []
clean_pollution_listT = set(pollution_listT)
print(clean_pollution_listT)

def article_number(article_keyword):
    parameters['q'] = article_keyword
    response = requests.get(url,params=parameters)
    content = response.json()
    return content['response']['meta']['hits']


resultsT_section = []
resultsT_hits = []


for p in clean_pollution_listO:
    result_section = (f"{p}")
    result_hits = (f"{article_number(p)}")
    resultsT_section.append(result_section)
    resultsT_hits.append(result_hits)
    time.sleep(4)

print(resultsT_section)
print(resultsT_hits)


dfO = pd.DataFrame(list(zip(resultsT_section, resultsT_hits)), columns = ["Section","Hits"])

print(dfO)


if not pathlib.Path("trump_results.csv").is_file():
    dfO.to_csv("C:/Users/sguru/Documents/Python_Scripts/trump_results.csv", index=False)
else:
    print("file already exists")