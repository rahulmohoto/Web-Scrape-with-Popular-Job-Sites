# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:59:07 2021

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
url_site = 'https://www.monster.com/jobs/search?q=designer&where='

Dictionary = {"Url":[],"Job Title":[],"Company Name":[],"Company Location":[]}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

top_five_pages = "&page=5"
url_site = url_site + top_five_pages

wd.get(url_site)

def parse_details(soup):
    
  for div_tag in soup.find_all('div', attrs={"class":"title-company-location"}):
    #Url
    url = "https://www.monster.com" + div_tag.find('a').get('href')
    Dictionary["Url"].append(url)
        
    #Job Title
    job_title = div_tag.find('h2', attrs={"name":"card_title"}).text
    Dictionary["Job Title"].append(job_title)
        
    #Company Name
    company_name = div_tag.find('h3', attrs={"name":"card_companyname"}).text
    Dictionary["Company Name"].append(company_name)
        
    #Company Location
    company_location = div_tag.find('span', attrs={"name":"card_job_location"}).text
    Dictionary["Company Location"].append(company_location)

def main():
  soup = BeautifulSoup(wd.page_source,'html.parser')
  parse_details(soup)

  dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
  dataframe=dataframe.fillna("")
  return dataframe

try:
  element = WebDriverWait(wd, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "title-company-location"))
  )
finally:
  dataframe=main()
  wd.quit()

print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrap Document Monster Jobs')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())
time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")
        
        
