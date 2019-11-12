# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import os
import sys
import random
import glob as gl

#----------------------------------------------------------------------


def MainTableScrape():
	# Output file
	outputfile = open('club_websites.csv', 'wb')
	csv_writer = csv.writer(outputfile)
	csv_writer.writerow(["Club", "Website"])
	
	# Make URL
	finalURL = 'https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League/' #baseURL + Teams[team] + '/Show/' #+ eplTeamsString[team] #archive
	print finalURL
	
	# Connect webdriver
	browser =  webdriver.Chrome("/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/chromedriver")
	#browser.add_argument('headless')
	#browser.set_window_size(1920, 1080) # PhantomJS default to 400X300 is executable element outside might cause problem
	browser.get(finalURL)
	time.sleep(5)
	
	
	
	content = browser.page_source
	soup = BeautifulSoup(''.join(content), 'lxml')
	
	table = soup.find("div", {"id": "standings-17590"}).find("tbody", {"id": "standings-17590-content"})
	
	TeamName = []
	TeamHref = []
	
	
	for i in table:
		rows = i.findAll("td")
		TeamName = rows[1].get_text()
		for link in rows[1].findAll("a"):
			TeamHref = link.get("href")
		csv_writer.writerow([TeamName,TeamHref])	
		
	browser.quit()



def ClubScrape():
	
	TeamName = []
	TeamHref = []
	
	rownumber = 0
	
	with open('club_websites.csv') as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		next(csvDataFile)
		for row in csvReader:
			TeamName.append(row[0])
			TeamHref.append(row[1])			
	
	baseURL = 'https://www.whoscored.com'
	
	count = 0
	
	# Each team
	for team in range(len(TeamName)):	
		if os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/'+TeamName[team]+'_players.csv'):
			continue
		else:
			PlayerDictionary = {}
			finalURL = baseURL + TeamHref[team]
			print finalURL		
			club = TeamName[team]
			
			# Connect webdriver
			browser =  webdriver.Chrome("/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/chromedriver")
			#browser.add_argument('headless')
			#browser.set_window_size(1920, 1080) # PhantomJS default to 400X300 is executable element outside might cause problem
			browser.get(finalURL)
			time.sleep(random.randint(1,5))
			
			# Get content
			try:
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				players = table.findAll("tr")
				for i in players:
					count = count + 1
					playername = i.findAll("td")
					player =  playername[2].get_text()
					justtheplayername = player.split(',')
					PLAYER =  justtheplayername[0][:-3]
					AGE = justtheplayername[0][-3:]
					CLUB  = TeamName[team]
					attributes = i.findAll("a")
					for links in attributes:
						WEBSITE = links.get("href")
					PlayerDictionary[count] = {"PLAYER":PLAYER, "AGE":AGE, "CLUB":CLUB, "WEBSITE":WEBSITE}	     
				PlayerTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("club_files/"+CLUB+"_players.csv", index = False, header=True, encoding = 'utf-8')  
			except: 
				time.sleep(60)
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				players = table.findAll("tr")
				for i in players:
					count = count + 1
					playername = i.findAll("td")
					player =  playername[2].get_text()
					justtheplayername = player.split(',')
					PLAYER =  justtheplayername[0][:-3]
					AGE = justtheplayername[0][-3:]
					CLUB  = TeamName[team]
					attributes = i.findAll("a")
					for links in attributes:
						WEBSITE = links.get("href")
					PlayerDictionary[count] = {"PLAYER":PLAYER, "AGE":AGE, "CLUB":CLUB, "WEBSITE":WEBSITE}	     
				PlayerTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("club_files/"+CLUB+"_players.csv", index = False, header=True, encoding = 'utf-8')	
			else: 
				time.sleep(60)
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				players = table.findAll("tr")
				for i in players:
					count = count + 1
					playername = i.findAll("td")
					player =  playername[2].get_text()
					justtheplayername = player.split(',')
					PLAYER =  justtheplayername[0][:-3]
					AGE = justtheplayername[0][-3:]
					CLUB  = TeamName[team]
					attributes = i.findAll("a")
					for links in attributes:
						WEBSITE = links.get("href")
					PlayerDictionary[count] = {"PLAYER":PLAYER, "AGE":AGE, "CLUB":CLUB, "WEBSITE":WEBSITE}	     
				PlayerTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("club_files/"+CLUB+"_players.csv", index = False, header=True, encoding = 'utf-8')	
			browser.quit()
			
		
	print 'Number of club files written: '	
	print str(len(os.listdir('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/')))
	print str(20-len(os.listdir('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/'))) + ' clubs remaining.' 
	

def PlayerScrape():
	
	Club = []
	PlayerAge = []
	PlayerName = []
	PlayerHref = []
	
	rownumber = 0
	for file in gl.glob('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/*.csv'):
		with open(file) as csvDataFile:
			csvReader = csv.reader(csvDataFile)
			next(csvDataFile)
			for row in csvReader:
				Club.append(row[0])
				PlayerName.append(row[1])
				PlayerAge.append(row[2])
				PlayerHref.append(row[3])
	
	baseURL = 'https://www.whoscored.com'
	
	count = 0
	
	# Each team
	for Player in range(len(PlayerName)):	
		if os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+PlayerName[Player]+'.csv'):
			print 'File already written for: ' + PlayerName[Player]	
		elif  os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+".csv"):
			print 'File already written for: ' + PlayerName[Player]
		elif  os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player]+'-'+PlayerName[Player].replace(' ', '')+".csv"):
			print 'File already written for: ' + PlayerName[Player]			
		else:
			PlayerDictionary = {}
			finalURL = baseURL + PlayerHref[Player].replace('Show', 'History')
			count = count + 1
			
			#print finalURL		
			#club = TeamName[team]
			# Connect webdriver
			browser =  webdriver.Chrome("/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/chromedriver")
			#browser.add_argument('headless')
			#browser.set_window_size(1920, 1080) # PhantomJS default to 400X300 is executable element outside might cause problem
			browser.get(finalURL)
			sleeptime = random.randint(1,5)
			print 'sleeping for: ' + str(sleeptime) + " seconds"
			time.sleep(sleeptime)
			print PlayerName[Player]
			
			try:
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				year_comp = table.findAll("tr")
				for i in year_comp:
					lines = i.findAll("td")
					count = count + 1
					Season = lines[0].get_text()
					Team = lines[1].get_text()
					Tournament = lines[2].get_text()
					Apps = lines[3].get_text()
					Mins = lines[4].get_text()
					Goals = lines[5].get_text()
					Assits = lines[6].get_text()
					YellowCards = lines[7].get_text()
					RedCards = lines[8].get_text()
					ShotsPerGame = lines[9].get_text()
					PassPercentage = lines[10].get_text()
					AerielsWon = lines[11].get_text()
					MotM = lines[12].get_text()
					WSRating = lines[13].get_text()
					PlayerDictionary[count] = {"Season": Season, "Team":Team, "Tournament": Tournament, "Apps":Apps, "Mins":Mins, "Goals":Goals, "Assits":Assits, "YellowCards":YellowCards, 
					                           "RedCards":RedCards, "ShotsPerGame":ShotsPerGame, "PassPercentage":PassPercentage, "AerielsWon": AerielsWon, "MotM": MotM, "WSRating":WSRating}
				HistoryTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("player_files/"+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+".csv", index = False, header=True, encoding = 'utf-8')
			except:
				print "Scraped Failed. Sleeping for 30 seconds."
				time.sleep(30)
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				year_comp = table.findAll("tr")
				for i in year_comp:
					lines = i.findAll("td")
					count = count + 1
					Season = lines[0].get_text()
					Team = lines[1].get_text()
					Tournament = lines[2].get_text()
					Apps = lines[3].get_text()
					Mins = lines[4].get_text()
					Goals = lines[5].get_text()
					Assits = lines[6].get_text()
					YellowCards = lines[7].get_text()
					RedCards = lines[8].get_text()
					ShotsPerGame = lines[9].get_text()
					PassPercentage = lines[10].get_text()
					AerielsWon = lines[11].get_text()
					MotM = lines[12].get_text()
					WSRating = lines[13].get_text()
					PlayerDictionary[count] = {"Season": Season, "Team":Team, "Tournament": Tournament, "Apps":Apps, "Mins":Mins, "Goals":Goals, "Assits":Assits, "YellowCards":YellowCards, 
					                           "RedCards":RedCards, "ShotsPerGame":ShotsPerGame, "PassPercentage":PassPercentage, "AerielsWon": AerielsWon, "MotM": MotM, "WSRating":WSRating}
				HistoryTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("player_files/"+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+".csv", index = False, header=True, encoding = 'utf-8')
			else:
				print "Scraped Failed. Sleeping for 30 seconds."
				time.sleep(30)
				content = browser.page_source
				soup = BeautifulSoup(''.join(content), 'lxml')
				
				table = soup.find("div", {"id": "statistics-table-summary"}).find("tbody", {"id": "player-table-statistics-body"})
				
				year_comp = table.findAll("tr")
				for i in year_comp:
					lines = i.findAll("td")
					count = count + 1
					Season = lines[0].get_text()
					Team = lines[1].get_text()
					Tournament = lines[2].get_text()
					Apps = lines[3].get_text()
					Mins = lines[4].get_text()
					Goals = lines[5].get_text()
					Assits = lines[6].get_text()
					YellowCards = lines[7].get_text()
					RedCards = lines[8].get_text()
					ShotsPerGame = lines[9].get_text()
					PassPercentage = lines[10].get_text()
					AerielsWon = lines[11].get_text()
					MotM = lines[12].get_text()
					WSRating = lines[13].get_text()
					PlayerDictionary[count] = {"Season": Season, "Team":Team, "Tournament": Tournament, "Apps":Apps, "Mins":Mins, "Goals":Goals, "Assits":Assits, "YellowCards":YellowCards, 
					                           "RedCards":RedCards, "ShotsPerGame":ShotsPerGame, "PassPercentage":PassPercentage, "AerielsWon": AerielsWon, "MotM": MotM, "WSRating":WSRating}
				HistoryTable = pd.DataFrame.from_dict(data=PlayerDictionary, orient='index').to_csv("player_files/"+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+".csv", index = False, header=True, encoding = 'utf-8')
			browser.quit()
			print 'Number of player files written: '	
			print str(len(os.listdir('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/')))
			print str(count-len(os.listdir('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/'))) + ' players remaining.' 			
		
	
def Filerename():
	
	Club = []
	PlayerAge = []
	PlayerName = []
	PlayerHref = []
	
	rownumber = 0
	for file in gl.glob('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/club_files/*.csv'):
		with open(file) as csvDataFile:
			csvReader = csv.reader(csvDataFile)
			next(csvDataFile)
			for row in csvReader:
				Club.append(row[0])
				PlayerName.append(row[1])
				PlayerAge.append(row[2])
				PlayerHref.append(row[3])
	
	baseURL = 'https://www.whoscored.com'
	
	count = 0
	print len(PlayerHref)
	
	
	# Each team
	for Player in range(len(PlayerName)):	
		if os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+PlayerName[Player]+'.csv'):
			continue
			#os.system('cp -R /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+PlayerName[Player].replace(' ', '\ ')+'.csv /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '')+'.csv')
			
		elif  os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+".csv"):
			continue
			#os.system('cp -R /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player].replace(' ', '')+'-'+PlayerName[Player].replace(' ', '')+'.csv /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '')+'.csv')

		elif  os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player]+'-'+PlayerName[Player].replace(' ', '')+".csv"):
			continue
			#os.system('cp -R /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player].replace(' ', '\ ')+'-'+PlayerName[Player].replace(' ', '')+'.csv /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '')+'.csv')			
			
		elif  os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player]+'-'+PlayerName[Player].replace(' ', '')+".csv"):
			continue
			#os.system('cp -R /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_files/'+Club[Player]+'-'+PlayerName[Player].replace(' ', '')+'.csv /Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '')+'.csv')
								
			
		else:
			print PlayerName[Player]
		
		



#MainTableScrape()
#ClubScrape()
#PlayerScrape()
Filerename()


