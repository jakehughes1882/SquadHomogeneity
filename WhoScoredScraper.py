import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys



#create header for scraping
#headers = {'User-Agent': 
#           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
           
page = 'https://www.whoscored.com/Teams/167/Show/England-Manchester-City'

pageTree = requests.get(page) #, headers=headers)

print pageTree

#pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

#print pageSoup

#print pageSoup.find_all("td", {"class":"team"})

#print URLS