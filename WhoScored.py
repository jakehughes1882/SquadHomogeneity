# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from bs4 import BeautifulSoup
import time
import csv
import os

#----------------------------------------------------------------------


# Deleting Output file when restarting
#if os.path.exists('PremierLeague1819.csv'):
#    os.remove('PremierLeague1819.csv')
#else:
#    print 'file does not exist'


# Output file
outputfile = open('EPL15162.csv', 'wb')
csv_writer = csv.writer(outputfile)
csv_writer.writerow(["name","tm","nat","age","pos","cm","kg","app","min","G","A","yel","red","spG","pa%","aerWon","moM","tac","int","fouls","offW","clear","drbP","blcks","ownG","KP","drb","fouled","cOff","disp","unsT","avgP","crosses","longB","thrB"])

# Main

# Base URL
baseURL = 'https://www.whoscored.com/Teams/'

# Teams
#Teams =  ['14', '13', '30', '167', '32', '18', '29', '26', '96', '15', '31', '259', '27', '175', '162',
Teams =  [ '183', '16', '23', '168', '24']  


#TeamsString =  ['Leicester', 'Arsenal', 'Tottenham', 'Manchester City', 'Manchester United', 'Southampton', 'West Ham', 'Liverpool', 'Stoke', 'Chelsea', 'Everton', 'Swansea', 'Watford', 'West Bromwich Albion', 'Crystal Palace', 
TeamsString =  ['Bournemouth', 'Sunderland', 'Newcastle United', 'Norwich', 'Aston Villa']        


print len(Teams)
#print len(eplTeamsString)


# Each team
for team in range(len(Teams)):

    # We will write from this dict
    ALLTHEDAMNPLAYERS = {}
    baseURL = 'https://www.whoscored.com/Teams/'
    # Make URL
    finalURL = baseURL + Teams[team] + '/Archive/?stageId=12496'
    print finalURL

    club = TeamsString[team]

    # Connect webdriver
    browser =  webdriver.Chrome("/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/chromedriver")
    #browser.add_argument('headless')
    #browser.set_window_size(1920, 1080) # PhantomJS default to 400X300 is executable element outside might cause problem
    browser.get(finalURL)
    time.sleep(10)
    # The different tables
    tableNames = ['summary', 'defensive', 'offensive', 'passing']
    # Load all tables in list
    datas = []
    # Get all tables
    while len(datas) != 4:
	    for tableName in tableNames:
	        try:
	            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='#team-squad-archive-stats-" + tableName + "']")))
	            time.sleep(10)
	            browser.execute_script("arguments[0].click();", element)
	            time.sleep(10)
	        except:
	            print "Problems with loading webpage in browser."
	            time.sleep(60)
	            print 'Sleeping for one minute. They I will try again'
	
	        # Get content
	        content = browser.page_source
	        soup = BeautifulSoup(''.join(content), 'lxml')
	
	        table = soup.find("div", {"id": "statistics-table-" + tableName }).find("tbody", {"id": "player-table-statistics-body"})
	
	        #Save data
	        datas.append(table)
	
	        print 'Data has length ' + str(len(datas)) + " at the moment."
    browser.quit()
    print ('')
    print ("-----------THE DATA-----------")
    print (team)
    print (datas)
    print ("------------------------------")
    print ('')
    # Action will be different for each table
    j = 0
    for data in datas:
	
	    # Get players
	    players = data.findAll("tr")
	
	    #Get stats
	    i = 0
	
	    while i < len(players):
	        stats = players[i].findAll("td")
	
	        if j == 0:
	            index = stats[0].get_text()
	            nation = stats[1].find("span").get("class")[2].rsplit('-', 1)[1]
	            name = stats[2].findChildren()[0].get_text().encode('utf-8').strip()
	            team = stats[2].findChildren()[2].get_text().rsplit(',', 1)[0]
	            age = stats[2].findChildren()[3].get_text()
	            pos = stats[2].findChildren()[4].get_text().split(',', 1)[1].strip()
	            cm = stats[3].get_text().strip()
	            kg = stats[4].get_text().strip()
	            apps = stats[5].get_text().strip()
	            mins = stats[6].get_text().strip()
	            goals = stats[7].get_text().strip()
	            assists = stats[8].get_text().strip()
	            yellow = stats[9].get_text().strip()
	            red = stats[10].get_text().strip()
	            SpG = stats[11].get_text().strip()
	            PassPer = stats[12].get_text().strip()
	            AerialsWon = stats[13].get_text().strip()
	            MotM = stats[14].get_text().strip()
	
	            ALLTHEDAMNPLAYERS[name] = []
	            ALLTHEDAMNPLAYERS[name].append(team)
	            ALLTHEDAMNPLAYERS[name].append(nation)
	            ALLTHEDAMNPLAYERS[name].append(age)
	            ALLTHEDAMNPLAYERS[name].append(pos)
	            ALLTHEDAMNPLAYERS[name].append(cm)
	            ALLTHEDAMNPLAYERS[name].append(kg)
	            ALLTHEDAMNPLAYERS[name].append(apps)
	            ALLTHEDAMNPLAYERS[name].append(mins)
	            ALLTHEDAMNPLAYERS[name].append(goals)
	            ALLTHEDAMNPLAYERS[name].append(assists)
	            ALLTHEDAMNPLAYERS[name].append(yellow)
	            ALLTHEDAMNPLAYERS[name].append(red)
	            ALLTHEDAMNPLAYERS[name].append(SpG)
	            ALLTHEDAMNPLAYERS[name].append(PassPer)
	            ALLTHEDAMNPLAYERS[name].append(AerialsWon)
	            ALLTHEDAMNPLAYERS[name].append(MotM)
	
	        if j == 1:
	            name = stats[2].findChildren()[0].get_text().encode('utf-8').strip()
	            tackles = stats[7].get_text().strip()
	            inter = stats[8].get_text().strip()
	            fouls = stats[9].get_text().strip()
	            offW = stats[10].get_text().strip()
	            clear = stats[11].get_text().strip()
	            drbP = stats[12].get_text().strip()
	            blocks = stats[13].get_text().strip()
	            ownG = stats[14].get_text().strip()
	
	            ALLTHEDAMNPLAYERS[name].append(tackles)
	            ALLTHEDAMNPLAYERS[name].append(inter)
	            ALLTHEDAMNPLAYERS[name].append(fouls)
	            ALLTHEDAMNPLAYERS[name].append(offW)
	            ALLTHEDAMNPLAYERS[name].append(clear)
	            ALLTHEDAMNPLAYERS[name].append(drbP)
	            ALLTHEDAMNPLAYERS[name].append(blocks)
	            ALLTHEDAMNPLAYERS[name].append(ownG)
	
	        if j == 2:
	            name = stats[2].findChildren()[0].get_text().encode('utf-8').strip()
	            KP = stats[10].get_text().strip()
	            drb = stats[11].get_text().strip()
	            fouled = stats[12].get_text().strip()
	            cOff = stats[13].get_text().strip()
	            disp = stats[14].get_text().strip()
	            unsT = stats[15].get_text().strip()
	
	            ALLTHEDAMNPLAYERS[name].append(KP)
	            ALLTHEDAMNPLAYERS[name].append(drb)
	            ALLTHEDAMNPLAYERS[name].append(fouled)
	            ALLTHEDAMNPLAYERS[name].append(cOff)
	            ALLTHEDAMNPLAYERS[name].append(disp)
	            ALLTHEDAMNPLAYERS[name].append(unsT)
	
	
	        if j == 3:
	            name = stats[2].findChildren()[0].get_text().encode('utf-8').strip()
	            avgP = stats[9].get_text().strip()
	            crosses = stats[11].get_text().strip()
	            longB = stats[12].get_text().strip()
	            thrB = stats[13].get_text().strip()
	
	            ALLTHEDAMNPLAYERS[name].append(avgP)
	            ALLTHEDAMNPLAYERS[name].append(crosses)
	            ALLTHEDAMNPLAYERS[name].append(longB)
	            ALLTHEDAMNPLAYERS[name].append(thrB)
	
	        i += 1
	
	    j += 1
	    
    for indiv in ALLTHEDAMNPLAYERS:
    	csv_writer.writerow([indiv,ALLTHEDAMNPLAYERS[indiv][0],ALLTHEDAMNPLAYERS[indiv][1],ALLTHEDAMNPLAYERS[indiv][2],ALLTHEDAMNPLAYERS[indiv][3],ALLTHEDAMNPLAYERS[indiv][4],ALLTHEDAMNPLAYERS[indiv][5],ALLTHEDAMNPLAYERS[indiv][6],ALLTHEDAMNPLAYERS[indiv][7],ALLTHEDAMNPLAYERS[indiv][8],ALLTHEDAMNPLAYERS[indiv][9],ALLTHEDAMNPLAYERS[indiv][10],ALLTHEDAMNPLAYERS[indiv][11],ALLTHEDAMNPLAYERS[indiv][12],ALLTHEDAMNPLAYERS[indiv][13],ALLTHEDAMNPLAYERS[indiv][14],ALLTHEDAMNPLAYERS[indiv][15],ALLTHEDAMNPLAYERS[indiv][16],ALLTHEDAMNPLAYERS[indiv][17],ALLTHEDAMNPLAYERS[indiv][18],ALLTHEDAMNPLAYERS[indiv][19],ALLTHEDAMNPLAYERS[indiv][20],ALLTHEDAMNPLAYERS[indiv][21],ALLTHEDAMNPLAYERS[indiv][22],ALLTHEDAMNPLAYERS[indiv][23],ALLTHEDAMNPLAYERS[indiv][24],ALLTHEDAMNPLAYERS[indiv][25],ALLTHEDAMNPLAYERS[indiv][26],ALLTHEDAMNPLAYERS[indiv][27],ALLTHEDAMNPLAYERS[indiv][28],ALLTHEDAMNPLAYERS[indiv][29],ALLTHEDAMNPLAYERS[indiv][30],ALLTHEDAMNPLAYERS[indiv][31],ALLTHEDAMNPLAYERS[indiv][32],ALLTHEDAMNPLAYERS[indiv][33]])
	
	
	
	
