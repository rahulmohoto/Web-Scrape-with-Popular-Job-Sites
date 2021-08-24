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
url_site = 'https://www.freelancer.com.bd/jobs/?keyword=designer'

Dictionary = {"Url":[],"Job Title":[],"Speciality":[],"Biding Price":[],"Total Bids":[],"Employer Review":[],"Employer Address":[]}

def parseDetails(soup):
    
    for div_tag in soup.find_all('div',attrs={"class":"JobSearchCard-item-inner"}):
        
        #Job Title
        Dictionary["Job Title"].append(div_tag.find('a',attrs={"class":"JobSearchCard-primary-heading-link"}).text.strip())
        
        #Link
        url = "https://www.freelancer.com.bd"+div_tag.find('a',attrs={"class":"JobSearchCard-primary-heading-link"}).get('href')+"?ngsw-bypass=&w=f"
        Dictionary["Url"].append(url)
        
        #Tags
        Dictionary["Speciality"].append(div_tag.find('div',attrs={"class":"JobSearchCard-primary-tags"}).text.strip())
        
        #Biding Price
        biding_price = div_tag.find('div',attrs={"class":"JobSearchCard-secondary-price"})
        if biding_price is not None:
            Dictionary["Biding Price"].append(biding_price.text.lstrip().split("\n")[0].strip()+" "+biding_price.text.lstrip().split("\n")[2].strip())
        else:
            Dictionary["Biding Price"].append(" ")
        
        #Biding Number
        biding_number = div_tag.find('div',attrs={"class":"JobSearchCard-secondary-entry"})
        if biding_number is not None:
            Dictionary["Total Bids"].append(biding_number.text.lstrip())
        else:
            Dictionary["Total Bids"].append(" ")
        
        #Parsing Job Urls
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text,'html.parser')
        
        wholeLocationString = soup.find('span',attrs={'class':'Rating-review'})
        if wholeLocationString is not None:
            reviews = wholeLocationString.text[(wholeLocationString.text.find("reviews")-7):(wholeLocationString.text.find("reviews")+7)]
            Dictionary["Employer Review"].append(reviews.strip())
        else:
            Dictionary["Employer Review"].append(" ")
        
        employee_address = soup.find('span',attrs={"itemprop":"addressLocality"})
        if employee_address is not None:
            Dictionary["Employer Address"].append(employee_address.text.strip())
        else:
            Dictionary["Employer Address"].append(" ")
        
    
def getResultsfrom5pages(url_site):

  html_text = requests.get(url_site[0:url_site.find("jobs")+4]+url_site[url_site.find("/?keyword"):len(url_site)]).text
  soup = BeautifulSoup(html_text,'html.parser')
  parseDetails(soup)

  for i in range(2,6):
    html_text = requests.get(url_site[0:url_site.find("jobs/")+5]+str(i)+url_site[url_site.find("/?keyword"):len(url_site)]).text
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
sheet = client.open('Web Scrape Document Freelance Bd')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())
time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")