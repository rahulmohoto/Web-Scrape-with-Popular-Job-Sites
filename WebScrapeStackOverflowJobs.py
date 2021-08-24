# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 17:23:57 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Job Terms":[] , "Skills":[], "Company Name":[], "Company Location":[], "Posted About":[]}

# Paste the URL here
url_site = 'https://stackoverflow.com/jobs?q=designer'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2, "profile.default_content_setting_values.cookies": 2}
options.add_experimental_option("prefs",prefs)

# options.AddUserProfilePreference("profile.default_content_setting_values.cookies", 2);

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)

wd.find_element_by_css_selector('.s-btn.s-btn__primary.js-accept-cookies').click()

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'flex--item fl1'}):
        
        # Job Title
        try:
            Dictionary["Job Title"].append(div_tag.find('h2', attrs={'class':'mb4 fc-black-800 fs-body3'}).text.strip())
        except:
            continue
        
        # Job Url
        Dictionary["Url"].append("https://stackoverflow.com"+div_tag.find('h2', attrs={'class':'mb4 fc-black-800 fs-body3'}).find('a').get('href'))
        
        # Company Name, Company Location
        span_list=[]
        for span_tag in div_tag.find('h3', attrs={'class':'fc-black-700 fs-body1 mb4'}).find_all('span'):
            span_list.append(span_tag.text.strip())
        
        Dictionary["Company Name"].append(span_list[0])
        Dictionary["Company Location"].append(span_list[1])
        
        #Skills
        skills_required=""
        for a_tag in div_tag.find('div', attrs={'class':'d-inline-flex gs4 fw-wrap'}).find_all('a'):
            skills_required+=a_tag.text.strip()+"\n"
        
        Dictionary["Skills"].append(skills_required)
        
        #Job Terms & Posted About
        index = 0
        terms = ""
        for li_tag in div_tag.find('ul', attrs={'class':'mt4 fs-caption fc-black-500 horizontal-list'}).find_all('li'):
            if index == 0:
                 Dictionary["Posted About"].append(li_tag.text.strip())
            else:
                terms+=li_tag.text.strip()+"\n"
                
            index=-1
        
        Dictionary["Job Terms"].append(terms)
            
        # print("\n")

        
def top5pages(url_site):
    wd.get(url_site)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,6):
        url = url_site[0:len(url_site)]+"&pg="+str(i)
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
sheet = client.open('Web Scrape Document-StackOverflowJobs')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")