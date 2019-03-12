# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:59:15 2019

@author: jbhud
"""
#libraries
from urllib import request
#from bs4 import BeautifulSoup
import re
import os
import json
#import datetime
#import time
#from selenium import webdriver (if needed)
#home directory-> repo folder
homedir = "C:/Users/jbhud/Documents/GitHub/JobHunter/"

#1. get search result pages
#future function inputs
query = "data scientist" 
query = "+".join(query.split())
loc = "Stockholm"

#build search result url, sorted by DATE
#eg: https://se.indeed.com/jobb?q=data+scientist&l=Stockholm&sort=date
homeURL = "https://se.indeed.com/jobs?"
homeURL = homeURL+"q="+query+"&l="+loc+"&sort=date"

#open 1st result page
with request.urlopen(homeURL) as f:
    homepage = f.read().decode("utf-8")
    
#find total number of results
totalres = int(re.search("(?<=Sida 1 av )(\d+)(?= resultat)", homepage).group())
#NOTE: read up on ?<= "lookaround"/lookbehind regex stuff
#total number of search 
totalpages = totalres//10+1  
    
#2. extract job listing links
if "links.json" in os.listdir(homedir+"Data"):
    with open(homedir+"Data/links.json", "r") as f:
        links = json.load(f)
else:
    links = {} #initial run
    
for page in range(totalpages):
    URL = homeURL+"&start="+str(page*10)
    with request.urlopen(URL) as f:
        html = f.read().decode("utf-8")
    html = html.replace("\n", " ")
    listings = re.findall("jobsearch-SerpJobCard.*?\/rc\/clk\?jk.*?&vjs=3", html)
    for job in listings:
        #jobid = re.search("(?<=id=\")(.*)(?=\" data-jk=)", job).group() #(LOOKAROUND PRACTISE)
        jobid = re.findall("id=\"(.*)\" data-jk=", job)[0]
        link = re.findall("\/rc\/clk\?jk=(.*)&vjs=3", job)[0]
        link = "https://se.indeed.com/rc/clk?jk="+link+"&vjs=3"
        tempdict = {jobid:link}
        tempdict.update(links)
        links = tempdict #done to keep newest version of same job ad
with open(homedir+"Data/links.json", "w") as f:
    json.dump(links, f)

#use of dictionary omits 17 similar results that Indeed omits really 96 results->79
#PROBLEM: was planning on stopping search as soon as a job id is recognised, ie. already scraped job ad but the re-posting 
        #by companies means that i cant do this, i need to search through all each time
        #SOLUTION: use date posted? -> eg regex <span class="date">2 dagar sedan</span>
#visit each job listing, extract job descriptions