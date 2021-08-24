# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 01:31:32 2021

@author: Rahul
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

# Paste the Url Here
url_site = 'https://www.indeed.com/jobs?q=animator&l&vjk=fb36dfb84626551e'

Dictionary = {"Url":[], "Job Title":[], "Company Name":[], "Ratings":[], "Company Address & Job Location":[], "Salary":[], "Job Type":[], "Recruitment Number":[]}

def parse_details(soup):
    
    for a_tag in soup.find_all('a',attrs={"class": "tapItem"}):
        
        href_tag = a_tag.get('data-jk')
            
        url_site_jobInfo = "https://www.indeed.com/viewjob?"+"jk="+href_tag+"&from=serp&vjs=3"
        
        #Get Job Url
        Dictionary["Url"].append(url_site_jobInfo)
        
        html_text_jobInfo = requests.get(url_site_jobInfo).text
        soup_jobInfo = BeautifulSoup(html_text_jobInfo,'html.parser')
    
        for div_tag in soup_jobInfo.find_all('div',attrs={"class":"jobsearch-DesktopStickyContainer"}):
            
            #Job Title
            job_title = div_tag.find('h1',attrs={"class":"jobsearch-JobInfoHeader-title"}).text.strip()
            Dictionary["Job Title"].append(job_title)

            
            #Company Name with Link
            company_name = div_tag.find('a')
            if company_name is None:
                company_name = div_tag.find('div', attrs={"class": "jobsearch-InlineCompanyRating"})
            Dictionary["Company Name"].append(company_name.text.strip())

                
            #Company Ratings    
            rating = div_tag.find('div',attrs={"class":"icl-Ratings-count"})
            if rating is not None:
                Dictionary["Ratings"].append(rating.text.strip())
            else:
                Dictionary["Ratings"].append(" ")
            
            #Company Address and Job Location
            data=""
            for details in div_tag.find('div',attrs={"class":"jobsearch-DesktopStickyContainer-subtitle"}):
                extract = div_tag.find('div',attrs={"class":"jobsearch-InlineCompanyRating"})
                extract.clear()

            Dictionary["Company Address & Job Location"].append(details.text.strip())
                    
        #Salary and Job Type            
        for div_tag in soup_jobInfo.find_all('div',attrs={"class":"jobsearch-JobDescriptionSection-section"}):
            if div_tag.text.find('Salary') != -1:
                salary = div_tag.text[div_tag.text.find('Salary')+6:div_tag.text.find('Job Type')]
                Dictionary["Salary"].append(salary.strip())
            else:
                Dictionary["Salary"].append(" ")

            if div_tag.text.find('Job Type') != -1:
                job_type = div_tag.text[div_tag.text.find('Job Type')+7:div_tag.text.find('Number of hires for this role')]
                Dictionary["Job Type"].append(job_type.strip())
            else:
                Dictionary["Job Type"].append(" ")

            if div_tag.text.find('Number of hires for this role') != -1:
                number_of_recruitment = div_tag.text[div_tag.text.find('Number of hires for this role')+29:len(div_tag.text)]
                Dictionary["Recruitment Number"].append(number_of_recruitment.strip())
            else:
                Dictionary["Recruitment Number"].append(" ")
            
#         print("\n")

def url_parser(url):
    url_search_index = url.find("q")
    url_job_key_index = url.find("vjk")
    
    #top 4 pages of indeed
    array = ["10","20","30","40"]
    custom_url = [url]
    
    for array_element in array:
        custom_url.append(url[0:url_search_index]+url[url_search_index:url_job_key_index]+"start="+array_element+"&"+url[url_job_key_index:len(url)])
    
    for urls in custom_url:
        url_to_html(urls)       

def url_to_html(url):
    html_text = requests.get(url_site).text
    soup = BeautifulSoup(html_text,'html.parser')
    
    parse_details(soup)
    
def main(url_site):
  html_text = requests.get(url_site).text
  soup = BeautifulSoup(html_text,'html.parser')

  url_parser(url_site)
  # print(Dictionary)
  dataframe=pd.DataFrame({ key:pd.Series(value) for key, value in Dictionary.items() })
  dataframe=dataframe.fillna("")
  # parse_details(soup)
  return dataframe

dataframe=main(url_site)
print(dataframe)

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Asus/Desktop/python video stream/my-excel-api-project-5d671d873ee0.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Web Scrap Document Indeed')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_instance.append_row(dataframe.columns.tolist())
time.sleep(1)

for index in range(len(dataframe.index)):
  sheet_instance.append_row(dataframe.iloc[index].values.tolist())
  time.sleep(1)
print("Done")

    