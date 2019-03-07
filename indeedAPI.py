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
    homepage = f.read().decode('utf-8')
    
#find total number of results
re.search("<div id=\"searchCount\">", homepage)

#text to search for
#<div id="searchCount">
#        Sida 1 av 96 resultat</div>
        
#2. extract job listing links

#visit each job listing, check if new/unique (using id no?), extract job descriptions