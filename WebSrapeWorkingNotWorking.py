# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:06:15 2021

@author: Rahul
"""
# import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[],"Job Title":[],"Job Terms":[],"Company Name":[],"Company Location":[]}

# Paste the URL here
url_site = 'https://workingnotworking.com/search/jobs?search_id=30988194&title_ids%5B%5D=35'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={"class":"dt relative z-1"}):
        
        Dictionary["Job Terms"].append(div_tag.find('a', attrs={'class':'link f8 fw7 ttu'}).text)
        Dictionary["Job Title"].append(div_tag.find('a', attrs={'class':'black f5 f3-ns link db truncate'}).text)
        Dictionary["Company Name"].append(div_tag.find('a', attrs={'class':'dib mt1 black-60 f6 f4-ns fw3 link'}).text)
        Dictionary["Company Location"].append(div_tag.find('a', attrs={'class':'f7 black-50 link'}).text)
        Dictionary["Url"].append("https://workingnotworking.com"+div_tag.find('a', attrs={'class':'black f5 f3-ns link db truncate'}).get('href'))
        
        # print("\n")
        
def top5pages(url_site):
    
    wd.get(url_site)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,6):
        url = url_site[0:url_site.find("search_id")-1]+"?page="+str(i)+url_site[url_site.find("search_id")-1:len(url_site)]
        wd.get(url)
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
sheet = client.open('Web Scrape Document-WorkingnotWorking')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")
   

# print(Dictionary)