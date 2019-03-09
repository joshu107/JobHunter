# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:59:15 2019

@author: jbhud
"""
#libraries
from urllib import request
from bs4 import BeautifulSoup
import re
#from selenium import webdriver (if needed)

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
links = []
for page in range(totalpages):
    URL = homeURL+"&start="+str(page*10)
    with request.urlopen(URL) as f:
        html = f.read().decode("utf-8")
    newlinks = re.findall("\/rc\/clk\?jk=(.*)&vjs=3", html)
    newlinks = ["https://se.indeed.com/rc/clk?jk="+ext+"&vjs=3" for ext in newlinks]
    links = links+newlinks
    

#visit each job listing, check if new/unique (using id no?), extract job descriptions