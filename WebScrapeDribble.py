# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 14:53:59 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Job Type":[], "Job Terms":[], "Company Name":[], "Company Location":[], "Posted About":[]}

# Paste the URL here
url_site = 'https://dribbble.com/jobs?utf8=%E2%9C%93&keyword=&specialty_ids%5B%5D=6&location='

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)

def parse_details(soup):
    
    for li_tag in soup.find_all('li', attrs={'class':'job-list-item'}):
        
        Dictionary["Url"].append("https://dribbble.com" + li_tag.find('a', attrs={'class':'job-link'}).get('href')) #Link
        
        Dictionary["Job Title"].append(li_tag.find('h4', attrs={'class': 'job-title job-board-job-title'}).text.strip()) #Job Title
        
        list_li = []
        for span_tag in li_tag.find('div', attrs={'class':'job-role'}).find_all('span'):
            list_li.append(span_tag.text.strip())
        
        Dictionary["Company Name"].append(list_li[0]) #Company Name
        Dictionary["Job Type"].append(list_li[1]) #Job Type
        if len(list_li) > 2:
            Dictionary["Job Terms"].append(list_li[2]) #Job Terms
        else:
            Dictionary["Job Terms"].append("")
        
        Dictionary["Company Location"].append(li_tag.find('div', attrs={'class':'location-container job-board-job-location'}).text.strip()) #Company Location
        
        Dictionary["Posted About"].append(li_tag.find('div', attrs={'class':'posted-on hide-on-mobile'}).text.strip()) #Posted About
        
        # print("\n")
        
def top5pages(url_site):
    wd.get(url_site)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,6):
        url = url_site[0:len(url_site)]+"&page="+str(i)
        wd.get(url)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)
        
    
top5pages(url_site) 

    
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
sheet = client.open('Web Scrape Document-Dribbble')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")