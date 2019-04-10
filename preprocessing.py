# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:01:01 2019

@author: jbhud
"""
#NLP on job listings#

#librairies
import json
import nltk
nltk.download()
#home directory-> repo folder
homedir = "C:/Users/jbhud/Documents/GitHub/JobHunter/"

#load data: dictiory of listings
with open(homedir+"Data/descriptions.json", "r") as f:
    ads = json.load(f)
    
