# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:48:41 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Company Name":[], "Company Location":[], "Posted About":[]}

# Paste the URL here
url_site = 'https://jooble.org/SearchResult?p=3&ukw=designer'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)

def parse_details(soup):
    
    for span_tag in soup.find_all('article', attrs={'class':'JobCard_card__FxQpv JobList_card__yKsad'}):
        
        Dictionary["Job Title"].append(span_tag.find('h2', attrs={'class': 'JobCard_position_heading__15V35'}).text) #Job Title
        Dictionary["Url"].append(span_tag.find('h2', attrs={'class': 'JobCard_position_heading__15V35'}).find('a').get('href')) #Job Url
        
        #Company Name
        try:
            Dictionary["Company Name"].append(span_tag.find('div', attrs={'class': 'GoodEmployerWidget_employer__1JrOt JobCard_employer_widget__3mz-P'}).text)
        except:
            Dictionary["Company Name"].append("No Employer details")
        
        Dictionary["Company Location"].append(span_tag.find('a', attrs={'class': 'JobCard_location_label__33iNQ'}).text) #Company Location
        Dictionary["Posted About"].append(span_tag.find('div', attrs={'class': 'JobCard_date_label__19pKu'}).text) #Posted About
        # print("\n")
        
wd.execute_script("function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}"+"for (let i = 0; i < 10; i++) {window.scrollTo(document.body.scrollHeight*i, document.body.scrollHeight*(i+1));await sleep(1000);}") 

        
# def top5pages(url_site):
    # wd.get(url_site)
    # soup = BeautifulSoup(wd.page_source,'html.parser')
    # parse_details(soup)
    
    # for i in range(2,6):
    #     url = url_site[0:len(url_site)]+"&page="+str(i)
    #     wd.get(url)
    #     soup = BeautifulSoup(wd.page_source,'html.parser')
    #     parse_details(soup)
        
    
# top5pages(url_site) 

soup = BeautifulSoup(wd.page_source,'html.parser')
parse_details(soup)
    
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
sheet = client.open('Web Scrape Document-Jobble')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")