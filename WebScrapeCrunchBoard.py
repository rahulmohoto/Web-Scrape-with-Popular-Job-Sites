# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:43:21 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Job/Company Location":[], "Job Type":[],"Company Name":[], "Posted On":[]}

# Paste the URL here
url_site = 'https://www.crunchboard.com/jobs/search?q=designer'

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2, "profile.default_content_setting_values.cookies": 2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

def parse_details(soup):
    
    for li_tag in soup.find_all('li', attrs={'class':'job-listing'}):
        
        
        if str(li_tag.find('a', {'class':'jobList-title'}).get('href')).find("https:") == -1:
            Dictionary["Url"].append("https://www.crunchboard.com"+li_tag.find('a', {'class':'jobList-title'}).get('href'))
        else:
            Dictionary["Url"].append(li_tag.find('a', {'class':'jobList-title'}).get('href'))
        
        Dictionary["Job Title"].append(li_tag.find('a', {'class':'jobList-title'}).text.strip())
        
        list_li = []
        for tags in li_tag.find_all('li'):
            list_li.append(tags.text.strip())
        
        Dictionary["Company Name"].append(list_li[0])
        
        Dictionary["Job/Company Location"].append(list_li[1])
        
        try:
            Dictionary["Job Type"].append(list_li[2])
        except:
            Dictionary["Job Type"].append("")
        
        Dictionary["Posted On"].append(li_tag.find('div', {'class':'jobList-date text-muted u-textNoWrap'}).text.strip())
        
        
        
        
def top5pages(url_site):
    
    wd.get(url_site)
    time.sleep(2)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,6):
        url = url_site[0:len(url_site)] + "&page=" + str(i)
        wd.get(url)
        time.sleep(2)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)
        print(url)
        
top5pages(url_site)
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
sheet = client.open('Web Scrape Document-CrunchBoard')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")