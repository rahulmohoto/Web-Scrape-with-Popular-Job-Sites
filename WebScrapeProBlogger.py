# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 12:52:35 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

Dictionary = {"Url":[], "Job Title":[], "Job Type":[] , "Job Terms":[], "Company Name":[], "Company Location":[]}

# Paste the URL here
url_site = 'https://problogger.com/jobs/?show_results=1&query=writer&location'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'wpjb-grid-row'}):
        try:
            #Title
            Dictionary["Job Title"].append(div_tag.find('div', attrs={'class':'wpjb-grid-col wpjb-col-35 wpjb-col-title'}).find('span', attrs={'class':'wpjb-line-major'}).text.strip())
        except:
            continue
        
        #Url
        Dictionary["Url"].append(div_tag.find('div', attrs={'class':'wpjb-grid-col wpjb-col-35 wpjb-col-title'}).find('span', attrs={'class':'wpjb-line-major'}).find('a').get('href'))
        #Company Name
        Dictionary["Company Name"].append(div_tag.find('div', attrs={'class':'wpjb-grid-col wpjb-col-35 wpjb-col-title'}).find('span', attrs={'class':'wpjb-sub wpjb-sub-small'}).text.strip())
        
        div_tag.find('div', attrs={'class':'wpjb-grid-col wpjb-col-35 wpjb-col-title'}).clear()
        
        #Company Location
        Dictionary["Company Location"].append(div_tag.find('span', attrs={'class':'wpjb-line-major'}).text.strip())
        #Job Terms
        Dictionary["Job Terms"].append(div_tag.find('span', attrs={'class':'wpjb-sub wpjb-sub-small'}).text.strip())
        
        #Job Type
        Dictionary["Job Type"].append(div_tag.find('div', attrs={'class':'custom-category-col'}).text.strip())
        
        # print(div_tag,"\n")
        

        
def top5pages(url_site):
    wd.get(url_site)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,6):
        url = url_site[0:url_site.find("?show_results")]+"page/"+str(i)+"/"+url_site[url_site.find("?show_results"):len(url_site)]
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
sheet = client.open('Web Scrape Document-ProBlogger')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")