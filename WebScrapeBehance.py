# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:40:13 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Company Name":[], "Company Location":[]}

# Paste the URL here
url_site = 'https://www.behance.net/joblist?search=designer&country=BD'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)

def parse_details(soup):
    
    for div_tag in soup.find_all('a', attrs={'class':'JobCard-routerLink-3Ln'}):
        
        Dictionary["Url"].append(div_tag.find('div', attrs={'class':'JobCard-avatarContainer-3Ig'}).find('a').get('href'))
        
        Dictionary["Company Name"].append(div_tag.find('h1', attrs={'class': 'JobCard-company-2dc'}).text.strip()) #Company Name
        Dictionary["Company Location"].append(div_tag.find('p', attrs={'class': 'JobCard-location-1iF'}).text.strip()) #Company Location
        Dictionary["Job Title"].append(div_tag.find('h2', attrs={'class': 'JobCard-title-25T e2e-JobCard-title'}).text.strip()) #Job Title
        
        # print("\n")
        
wd.execute_script("function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}"+"for (let i = 0; i < 10; i++) {window.scrollTo(document.body.scrollHeight*(i/20), document.body.scrollHeight/(10/(i+1)));await sleep(1000);}") 

try:
    element = WebDriverWait(wd, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "JobCard-companyDetails-161"))
    )
    
finally:
    # time.sleep(10)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    # print(Dictionary)
    # wd.quit()
    
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
sheet = client.open('Web Scrape Document-Behance')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")
