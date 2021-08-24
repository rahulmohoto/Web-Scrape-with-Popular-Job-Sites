# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:03:38 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd

import time

from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Paste the URL here
url_site = 'https://www.flexjobs.com/search?search=&search=designer&location='

Dictionary = {"Url":[],"Job Title":[],"Job Location":[],"Job Terms":[],"Job Type":[],"Posted About":[]}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)


def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'col-md-12 col-12'}):
        Dictionary['Job Title'].append(div_tag.find('a', attrs={'class':'job-title job-link'}).text.strip())
        Dictionary['Url'].append(div_tag.find('a', attrs={'class':'job-title job-link'}).get('href'))
        job_terms=""
        for jobInfo_div_tag in div_tag.find_all('div',attrs={'class':'col-sm-auto pr-sm-0 job-tags'}):
            job_terms = job_terms+jobInfo_div_tag.text.strip()+"\n"
        if len(job_terms.split("\n"))>2:
            Dictionary['Job Terms'].append(job_terms.split("\n")[0])
            Dictionary['Job Type'].append(job_terms.split("\n")[1])
        elif len(job_terms.split("\n")) == 2:
            Dictionary['Job Terms'].append(job_terms.split("\n")[0])
            Dictionary['Job Type'].append(" ")
        else:
            Dictionary['Job Terms'].append(" ")
            Dictionary['Job Type'].append(" ")
            
        Dictionary['Job Location'].append(div_tag.find('div', attrs={'class':'col pr-0 job-locations text-truncate'}).text.strip())
        Dictionary['Posted About'].append(div_tag.find('div', attrs={'class':'job-age'}).text.strip())
        

# soup = BeautifulSoup(wd.page_source,'html.parser')
# parse_details(soup)

def top5pages():
    global url_site
    for i in range(1,6):
        url=url_site[0:url_site.find("&location")]+"&page="+str(i)+url_site[url_site.find("&location"):len(url_site)]
        # print(url)
        wd.get(url)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)
        print("Done")

top5pages()

dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
dataframe=dataframe.fillna("")  
    
print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrape Document-FlexJobs')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")