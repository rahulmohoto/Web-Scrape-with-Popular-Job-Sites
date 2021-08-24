# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 18:13:51 2021

@author: Rahul
"""
from bs4 import BeautifulSoup
import pandas as pd

import time

from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Paste the URL here
url_site = 'https://aquent.com/find-work/?k=designer&l=12'

Dictionary = {"Url":[],"Job Title":[],"Job Location":[],"Job Terms":[],"Salary":[],"Starting Date":[],"Employer":[]}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')

prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(url_site)


def parse_details(soup):
    
    div_tag = soup.find('div', attrs={'id':'results'})
    for url in div_tag.find_all('a'):
        # print(url.get('href'))
        
        url = "https://aquent.com"+url.get('href')
        
        wd.get(url)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        Dictionary["Url"].append(url)
        job_title = soup.find('header', attrs={'class':'padding-vertical-2'})
        Dictionary["Job Title"].append(job_title.find('h3').text) #Title
        
        job_info = soup.find('div', attrs={'class': 'job-info'}).text.strip()
        split_upto_location = job_info.split("Location:")[1].split("Job Terms:")
        Dictionary["Job Location"].append(split_upto_location[0].strip()) #Location
        
        if(split_upto_location[1].strip().find("Salary:") != -1):
            split_upto_salary = split_upto_location[1].strip().split("Salary:")
            Dictionary["Job Terms"].append(split_upto_salary[0].strip()) #Job Terms
        else:
            Dictionary["Job Terms"].append("")
        
        if(split_upto_location[1].strip().find("Start date:") != -1):
            split_upto_startDate = split_upto_location[1].strip().split("Start date:")
            if split_upto_startDate[0].find("Salary:") != -1:
                Dictionary["Salary"].append(split_upto_startDate[0][split_upto_startDate[0].find("Salary:")+7:len(split_upto_startDate[0])].strip()) #Salary
            else:
                Dictionary["Salary"].append("")
        else:
            Dictionary["Salary"].append("")
        
        if(split_upto_location[1].strip().find("Posted By:") != -1):
            split_upto_postedBy = split_upto_location[1].strip().split("Posted By:")
            if split_upto_postedBy[0].find("Start date:") != -1:
                Dictionary["Starting Date"].append(split_upto_postedBy[0][split_upto_postedBy[0].find("Start date:")+11:len(split_upto_postedBy[0])].strip()) #Start Date    
            else:
                Dictionary["Starting Date"].append("") #Start Date
        else:
            Dictionary["Starting Date"].append("")
        
        if(split_upto_location[1].strip().find("Date:") != -1):
            split_upto_Date = split_upto_location[1].strip().split("Date:")
            if split_upto_Date[0].find("Posted By:") != -1:
                Dictionary["Employer"].append(split_upto_Date[0][split_upto_Date[0].find("Posted By:")+10:len(split_upto_Date[0])].strip()) #Posted By
            else:
                Dictionary["Employer"].append("")
        else:
            Dictionary["Employer"].append("")
        
        print("Done")
        
def top5pages():
    global url_site
    for i in range(1,6):
        url=url_site[0:url_site.find("k=")]+"page="+str(i)+"&"+url_site[url_site.find("k="):len(url_site)]
        wd.get(url)
        soup = BeautifulSoup(wd.page_source,'html.parser')
        parse_details(soup)

top5pages()

dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
dataframe=dataframe.fillna("")  
    
print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrape Document-Aquent')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())

time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")


    