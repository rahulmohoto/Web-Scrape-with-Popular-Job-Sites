# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:17:21 2021

@author: Rahul
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Paste the URL here
url_site = 'https://www.reddit.com/r/forhire/search/?q=Designer&restrict_sr=1'

Dictionary = {"Url":[],"Job Title":[],"Employer":[],"Posted around":[]}

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={"class":"_1poyrkZ7g36PawDueRza-J"}):
        
        Dictionary["Job Title"].append(div_tag.find('div', attrs={"class":"y8HYJ-y_lTUHkQIc1mdCq"}).text.split("]")[1].strip())
        Dictionary["Employer"].append(div_tag.find('a', attrs={"class":"_2tbHP6ZydRpjI44J3syuqC"}).text.split("u/")[1])
        Dictionary["Posted around"].append(div_tag.find('a', attrs={"data-click-id":"timestamp"}).text)
        Dictionary["Url"].append("https://www.reddit.com"+div_tag.find('a', attrs={"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"}).get('href'))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)

#Scrollbar Action 4times
wd.execute_script("function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}"+"for (let i = 0; i < 5; i++) {window.scrollTo(document.body.scrollHeight*i, document.body.scrollHeight*(i+1));await sleep(3000);}") 

def main():
  soup = BeautifulSoup(wd.page_source,'html.parser')
  parse_details(soup)

  dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
  dataframe=dataframe.fillna("")
  return dataframe

try:
    element = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_1poyrkZ7g36PawDueRza-J"))
    )
finally:
    soup = BeautifulSoup(wd.page_source,'html.parser')
    dataframe = main()
    wd.quit()

print(dataframe)
    
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrape Document Reddit-Hire')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())
time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
# # define the scope
# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# # add credentials to the account
# creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json", scope)

# # authorize the clientsheet 
# client = gspread.authorize(creds)

# # get the instance of the Spreadsheet
# sheet = client.open('Web Scrape Document Reddit-Hire')

# # get the first sheet of the Spreadsheet
# sheet_instance = sheet.get_worksheet(0)

# sheet_instance.append_row(dataframe.columns.tolist())

# time.sleep(1)

# for index in range(len(dataframe.index)):
#   sheet_instance.append_row(dataframe.iloc[index].values.tolist())
#   time.sleep(1)
# print("Done")
