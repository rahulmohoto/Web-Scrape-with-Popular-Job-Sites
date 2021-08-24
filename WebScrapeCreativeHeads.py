# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:41:23 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Skills":[], "Company Name":[], "Company Location":[], "Posted On":[]}

# Paste the URL here
url_site = 'https://www.creativeheads.net/job-search/designer/everywhere/1'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2, "profile.default_content_setting_values.cookies": 2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'job'}):
        
        # Date Posted
        Dictionary["Posted On"].append(div_tag.find('div', attrs={'class':'job-content'}).find('h3').find('div', attrs={'class':'date'}).text.strip())
        
        # Job Url
        Dictionary["Url"].append("https://www.creativeheads.net"+div_tag.find('div', attrs={'class':'job-content'}).find('h3').find('a').get('href'))
        
        # Job Title
        Dictionary["Job Title"].append(div_tag.find('div', attrs={'class':'job-content'}).find('h3').find('a').text.strip())
        
        # Skill List
        skill_list=""
        for skill in div_tag.find('div', attrs={'class':'job-content'}).find('p', attrs={'class':'skillList'}).find_all('a'):
            skill_list+=skill.text.strip()+"\n"
        Dictionary["Skills"].append(skill_list)
        
        # Company Name
        Dictionary["Company Name"].append(div_tag.find('div', attrs={'class':'job-content'}).find('p').text.strip().split("-")[0])
        
        # Company Location
        Dictionary["Company Location"].append(div_tag.find('div', attrs={'class':'job-content'}).find('p').text.strip().split("-")[1].strip())
        
        # print("\n")
        
def top5pages(url_site):
    
    for i in range(1,6):
        url = url_site[0:len(url_site)-1] + str(i)
        wd.get(url)
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
sheet = client.open('Web Scrape Document-CreativeHeads')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")
        
        