# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 13:38:08 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

# Paste the URL here
url_site = 'https://remote.co/remote-jobs/design/'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2, "profile.default_content_setting_values.cookies": 2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

Dictionary = {"Url":[], "Job Title":[], "Job Terms":[],"Company Name":[], "Posted About":[]}


def parse_details(soup):
    
    for a_tag in soup.find_all('a', {'class':'card m-0 border-left-0 border-right-0 border-top-0 border-bottom'}):
        
        # Link
        Dictionary["Url"].append("https://remote.co"+a_tag.get('href'))
        
        # Job Title
        Dictionary["Job Title"].append(a_tag.find('p', {'class':'m-0'}).find('span', {'class':'font-weight-bold larger'}).text.strip())
        
        # Posted About
        Dictionary["Posted About"].append(a_tag.find('p', {'class':'m-0'}).find('span', {'class':'float-right d-none d-md-inline text-secondary'}).text.strip())
        
        # Job Terms
        terms=""
        for info in a_tag.find('p', {'class':'m-0 text-secondary'}).find_all('span', {'class':'badge badge-success'}):
            terms += info.text.strip() + "\n"       
            info.clear()
            
        Dictionary["Job Terms"].append(terms);
        
        # Company Name
        Dictionary["Company Name"].append(a_tag.find('p', {'class':'m-0 text-secondary'}).text.split("|")[0].strip())
            
        # print("\n")

        
wd.get(url_site)
soup = BeautifulSoup(wd.page_source,'html.parser')
parse_details(soup)
wd.quit()
  
dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
dataframe=dataframe.fillna(" ")  

print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrape Document-RemoteCO')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")

