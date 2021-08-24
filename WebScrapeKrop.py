# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:15:18 2021

@author: Rahul
"""
# import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[],"Job Title":[],"Company Name":[],"Company Location":[]}

# Paste the URL here
url_site = 'https://www.krop.com/creative-jobs/?loc=&pos=animator'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)



def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'item'}):

        if div_tag.find('a', attrs={'class':'posting'}) != None:
            Dictionary["Url"].append(div_tag.find('a', attrs={'class':'posting'}).get('href'))
        else:
            Dictionary["Url"].append("")
            
        if div_tag.find('div', attrs={'class':'title'}) != None:
            Dictionary["Job Title"].append(div_tag.find('div', attrs={'class':'title'}).text.strip())
        else:
            Dictionary["Job Title"].append("")
            
        if div_tag.find('div', attrs={'class':'company'}) != None:
            Dictionary["Company Name"].append(div_tag.find('div', attrs={'class':'company'}).text.strip())
        else:
            Dictionary["Company Name"].append("")
            
        if div_tag.find('div', attrs={'class':'location'}) != None:
            Dictionary["Company Location"].append(div_tag.find('div', attrs={'class':'location'}).text.strip())
        else:
            Dictionary["Company Location"].append("")
        
def top5pages(url_site):
    for i in range(5):
        url = url_site[0:len(url_site)] + "&page=" + str(i+1)
        wd.get(url_site)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)

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
sheet = client.open('Web Scrape Document-Krop')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")