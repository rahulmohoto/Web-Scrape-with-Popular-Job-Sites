# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 12:49:09 2021

@author: Rahul
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread

Dictionary = {"Url":[],"Job Title":[],"Company Name":[], "Company Rating":[],"Company Address":[],"Salary":[],"Benefits":[], "Qualifications":[]}

# Paste the URL here
url_site = 'https://www.simplyhired.com/search?q=animator&job=wxbWMHA8Rat4NR7FVEn3OyBPnszDIfIFsfS7RRpKJXaGjRyFpGJbmg'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)

def parse_details(soup):
    
    for div_tag in soup.find_all('div', attrs={'class':'SerpJob-jobCard card'}):
        #Url
        url = "https://www.simplyhired.com/job/"+div_tag.get('data-jobkey')
        Dictionary["Url"].append(url)
        
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text,'html.parser')
        
        #Job Title
        Dictionary["Job Title"].append(soup.find('div', attrs={'class':'viewjob-jobTitle h2'}).text.strip())
        
        wholeString = soup.find('div', attrs={'class':'viewjob-labelWithIcon'})
        
        #Company Name and Rating
        Dictionary["Company Rating"].append(wholeString.text.split('-')[1].strip())
        Dictionary["Company Name"].append(wholeString.text.split('-')[0].strip())
        
        wholeString.clear()
        
        #Company Address & Salary
        Dictionary["Company Address"].append(soup.find('div', attrs={'class':'viewjob-header-companyInfo'}).text.strip())
        Dictionary["Salary"].append(soup.find('span', attrs={'class':'viewjob-labelWithIcon viewjob-salary'}).text.strip())
        
        try:
            list_li=""
            ul = soup.find('div',attrs={'class':'viewjob-section viewjob-qualifications viewjob-entities'}).find('ul', attrs={'class':'Chips'})
            for li in ul.find_all('li'):
                list_li = list_li + li.text + "\n"
            Dictionary["Qualifications"].append(list_li)
        except:
            Dictionary["Qualifications"].append(" ")
        
        try:
            list_li=""
            ul = soup.find('div',attrs={'class':'viewjob-section viewjob-benefits viewjob-entities'}).find('ul', attrs={'class':'Chips'})
            for li in ul.find_all('li'):
                list_li = list_li + li.text + "\n"
            Dictionary["Benefits"].append(list_li)
        except:
            Dictionary["Benefits"].append(" ")
        
        # print("\n")
       

def top5pages():
    
    wd.get(url_site)
    soup = BeautifulSoup(wd.page_source,'html.parser')
    parse_details(soup)
    
    for i in range(2,10):
        url=url_site[0:url_site.find('&job')]+"&pn="+str(i)+url_site[url_site.find('&job'):len(url_site)]
        wd.get(url)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)
    
top5pages()
# print(Dictionary)
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
sheet = client.open('Web Scrape Document-SimplyHired')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")