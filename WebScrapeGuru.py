# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 13:20:57 2021

@author: Rahul
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

# Paste the URL here
url_site = 'https://www.guru.com/d/jobs/skill/design/'

Dictionary = {"Url":[],"Job Title":[],"About Payment":[],"Wages Per Hour/Total Payment":[],"Total Hours Per Week":[],"Job Period":[],"Preffered Location":[],"Employer Name":[],"Employer Address":[]}

def parseDetails(soup):
    
    for div_tag in soup.find_all('div', attrs={"class":"record__header__identity"}):
        
        #Job Record Title
        Dictionary["Job Title"].append(div_tag.find('h2', attrs={"class":"jobRecord__title"}).text.strip())
        
        #Job Record URL
        url = "https://www.guru.com" + div_tag.find('a').get('href')
        Dictionary["Url"].append(url)
        
        #Job Record Budget
        wholeString = div_tag.find('div', attrs={"class":"jobRecord__budget"}).text.strip().split("|")
        if len(wholeString) > 4:
            Dictionary["About Payment"].append(wholeString[0].strip())
            Dictionary["Wages Per Hour/Total Payment"].append(wholeString[1].strip())
            Dictionary["Total Hours Per Week"].append(wholeString[2].strip())
            Dictionary["Job Period"].append(wholeString[3].strip())
            Dictionary["Preffered Location"].append(wholeString[4].strip())
        
        elif len(wholeString) > 3: 
            Dictionary["About Payment"].append(wholeString[0].strip())
            Dictionary["Wages Per Hour/Total Payment"].append(wholeString[1].strip())
            Dictionary["Total Hours Per Week"].append(wholeString[2].strip())
            Dictionary["Job Period"].append(wholeString[3].strip())
            Dictionary["Preffered Location"].append(" ")
            
        elif len(wholeString) > 2:
            Dictionary["About Payment"].append(wholeString[0].strip())
            Dictionary["Wages Per Hour/Total Payment"].append(wholeString[1].strip())
            Dictionary["Total Hours Per Week"].append(" ")
            Dictionary["Job Period"].append(" ")
            Dictionary["Preffered Location"].append(wholeString[2].strip())
            
        elif len(wholeString) > 1:
            Dictionary["About Payment"].append(wholeString[0].strip())
            Dictionary["Wages Per Hour/Total Payment"].append(wholeString[1].strip())
            Dictionary["Total Hours Per Week"].append(" ")
            Dictionary["Job Period"].append(" ")
            Dictionary["Preffered Location"].append(" ")
            
        else:
            Dictionary["About Payment"].append(wholeString[0].strip())
            Dictionary["Wages Per Hour/Total Payment"].append(" ")
            Dictionary["Total Hours Per Week"].append(" ")
            Dictionary["Job Period"].append(" ")
            Dictionary["Preffered Location"].append(" ")
        
        #Fetch Employer Information
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text,'html.parser')
        
        #Employer Name
        div_tag = soup.find('div', attrs={'class':'jobDetails__employer'})
        Dictionary["Employer Name"].append(div_tag.find('p', attrs={'class':'identityName'}).text.strip())
        Dictionary["Employer Address"].append(div_tag.find('p', attrs={'class':'subtext darkGrey'}).text.strip())

def getResultsfrom5pages(url_site):

  html_text = requests.get(url_site).text
  soup = BeautifulSoup(html_text,'html.parser')
  parseDetails(soup)

  for i in range(2,6):
    html_text = requests.get(url_site+'pg/'+str(i)+'/').text
    soup = BeautifulSoup(html_text,'html.parser')
    parseDetails(soup)
    
def main():
  getResultsfrom5pages(url_site)

  dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
  dataframe=dataframe.fillna("")
  return dataframe

dataframe = main()
print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrape Document Guru')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())
time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")