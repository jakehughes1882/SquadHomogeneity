import pandas as pd
import time
import csv
import os
import sys
import random
import glob as gl 
import pandas as pd

	
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
			
#print len(PlayerName)	


playerstats = {}




for Player in range(len(PlayerName)):	
	if os.path.exists('/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '').replace("'", '')+'.csv'):
			
		PlayerDataFile = '/Users/jakehughes/Documents/PythonScripts/FootballCode/Bad_Tottenham/player_history/'+PlayerName[Player].replace(' ', '').replace("'", '')+'.csv'
		
		player_history = pd.read_csv(PlayerDataFile, index_col='Season')
		player_history = player_history.drop_duplicates()
		player_history = player_history.drop('Total / Average')
		#rows_drop = []
		print PlayerName[Player]
		for i in player_history.index.tolist():
			if int(i[:4]) < 2015:
				try:
					player_history = player_history.drop(i)
				except:
					continue
		appearances = []	
		sub_apps = []
		print player_history['PassPercentage']
		
		if player_history['Goals'].dtype == 'object':
			player_history['goals'] = 0
			player_history['goals'] = player_history['Goals'].str.replace('\t','').replace('-', '0').astype('int64')
		else: 
			player_history['goals'] = player_history['Goals']
		
		#print player_history['Assits']
		if player_history['Assits'].dtype == 'object':
			player_history['assists'] = 0
			player_history['assists'] = player_history['Assits'].str.replace('\t','').replace('-', '0').astype('int64')
		else:
			player_history['assists'] = player_history['Assits']
		
		if player_history['MotM'].dtype == 'object':
			player_history['manofthematch'] = 0
			player_history['manofthematch'] = player_history['MotM'].str.replace('\t','').replace('-', '0').astype('int64')
		else:
			player_history['manofthematch'] = player_history['MotM']
		
		if player_history['YellowCards'].dtype == 'object':
			player_history['yellows'] = 0
			player_history['yellows'] = player_history['YellowCards'].str.replace('\t','').replace('-', '0').astype('int64')
		else:
			player_history['yellows'] = player_history['YellowCards']
			
		if player_history['RedCards'].dtype == 'object':
			player_history['reds'] = 0
			player_history['reds'] = player_history['RedCards'].str.replace('\t','').replace('-', '0').astype('int64')
		else: 
			player_history['reds'] = player_history['RedCards']
			
		if player_history['PassPercentage'].dtype == 'object':
			player_history['pp'] = 0
			player_history['pp'] = player_history['PassPercentage'].str.replace('\t','').replace('-', '0').astype('float64')
			print player_history['pp'] 
		else: 
			player_history['pp'] = player_history['PassPercentage']
			
		if player_history['AerielsWon'].dtype == 'object':
			player_history['aw'] = 0
			player_history['aw'] = player_history['AerielsWon'].str.replace('\t','').replace('-', '0').astype('float64')
		else: 
			player_history['aw'] = player_history['AerielsWon']
			
		if player_history['WSRating'].dtype == 'object':
			player_history['ws'] = 0
			player_history['ws'] = player_history['WSRating'].str.replace('\t','').replace('-', '0').astype('float64')
		else: 
			player_history['ws'] = player_history['WSRating']
			
		if player_history['ShotsPerGame'].dtype == 'object':
			player_history['SPG'] = 0
			player_history['SPG'] = player_history['ShotsPerGame'].str.replace('\t','').replace('-', '0').astype('float64')
		else: 
			player_history['SPG'] = player_history['ShotsPerGame']				
				
		for i in range(len(player_history)):	
			if player_history['Apps'].dtype == 'object':		
				if '(' in player_history['Apps'][i]:
					#print int(player_history['Apps'][i].split('(')[0])
					appearances.append(int(player_history['Apps'][i].split('(')[0]))
					sub_apps.append(int(player_history['Apps'][i].split('(')[1].replace(')', '')))
			else:
				appearances.append((player_history['Apps'][i]))	
		player_history_sum = player_history.sum(axis = 0, skipna = True)	
		#print player_history
		player_history_avg = player_history.mean(axis = 0, skipna = True)	
		#print player_history_avg['PassPercentage']
		print player_history['pp']
		#print player_history_avg['WSRating']
		#print player_history_sum['assists']
		#print player_history_sum['manofthematch']
		#print player_history_sum['yellows']
		#print player_history_sum['reds']
		#print sum(appearances)
		#print sum(sub_apps)
		
		playerstats[Player] = {'Player': PlayerName[Player], 'Player Age': PlayerAge[Player], 'CurrentClub': Club[Player], 'Minutes':player_history_sum['Mins'], 'Appearances': sum(appearances), 'AppearancesAsSub': sum(sub_apps), 'Goals': player_history_sum['goals'], 'Assists': player_history_sum['assists'], 'MotM': player_history_sum['manofthematch'], 'YellowCards': player_history_sum['yellows'], 'RedCards': player_history_sum['reds'], 'AerielsWon': player_history_avg['aw'], 'ShotsPerGame': player_history_avg['SPG'], 'PassingAccuracy':  player_history_avg['pp'], "Rating": player_history_avg['ws']}


pd.DataFrame.from_dict(data=playerstats, orient='index').to_csv('Player_stats.csv', index = False, header=True, encoding = 'utf-8')		
		




		