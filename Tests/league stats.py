from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time

# golbal variables
api_key = 'RGAPI-a0be06ae-a6bf-41e2-8c8e-03ebbdbde6f6'
watcher = LolWatcher(api_key)
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'AmratheAvenger')

#can only serach 100 matches in match list so I created 3 different dictionary to get around the problem. Spagehtti code
my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=0, queue = 420, season = 13)
my_matches2 = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=100, queue = 420, season = 13)
my_matches3 = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=200, queue = 420, season = 13)
my_matches4 = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=300, queue = 420, season = 13)
my_matches5 = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=400, queue = 420, season = 13)

match_list = my_matches['matches']
match_list2 = my_matches2['matches']
match_list3 = my_matches3['matches']
match_list4 = my_matches4['matches']
match_list5 = my_matches5['matches']

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions('10.10.3216176', False, 'en_US')

#static list of champions
champ_dict = {}
champ_enemy = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']   

#loop through first list and put it in full match list
full_match_list = []
i = 0
for match in match_list:
  print("Reading full match %d..." % i)
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  i += 1
  if (i == 100):
    break
  time.sleep(3)  # Pause to avoid overwhelming Riot API quota.

#loop through second list and put it in full match list
z = 0
for match in match_list2:
  print("Reading full match %d..." % z)
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  z += 1
  if (z == 100):
    break
  time.sleep(3)  # Pause to avoid overwhelming Riot API quota.

#loop through third list and put it in full match list
x = 0
for match in match_list3:
  print("Reading full match %d..." % x)
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  x += 1
  if (x == 100):
    break
  time.sleep(3)  # Pause to avoid overwhelming Riot API quota.

t = 0
for match in match_list4:
  print("Reading full match %d..." % t)
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  t += 1
  if (t == 100):
    break
  time.sleep(3)  # Pause to avoid overwhelming Riot API quota.

v = 0
for match in match_list5:
  print("Reading full match %d..." % v)
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  v += 1
  if (v == 50):
    break
  time.sleep(3)  # Pause to avoid overwhelming Riot API quota.

#main logic loop
#variables
i = 0
participants = []
allie = []
enemy = []
#loop through full match list
for match in full_match_list:

  print("Match:", i)


  #Find my partcipantId.
  i += 1
  for parts in match['participantIdentities']:
    if(parts['player']['summonerName'] == 'AmratheAvenger'):
      partId = parts['participantId']
      break
  #Find my teamId using participantId to make sure each champ get's put on the right team
  for player in match['participants']:
    if(partId == player['participantId']):
      team = player['teamId']
      break
  #Go through each participant and put them in the right category
  for player in match['participants']:  
    participants_row = {}
    champ_allie = {}
    champ_enemy = {}
    if((player['teamId'] == team) and player['stats']['win'] == True):
      champ_allie['Winner'] = champ_dict[str(player['championId'])]
      allie.append(champ_allie)
    elif((player['teamId'] == team) and player['stats']['win'] == False):
      champ_allie['Loser'] = champ_dict[str(player['championId'])]
      allie.append(champ_allie)
    elif((player['teamId'] != team) and player['stats']['win'] == True):
      champ_enemy['Winner'] = champ_dict[str(player['championId'])]
      enemy.append(champ_enemy)
    elif((player['teamId'] != team) and player['stats']['win'] == False):
      champ_enemy['Loser'] = champ_dict[str(player['championId'])]
      enemy.append(champ_enemy)

#dataframes that have all the champion names
dt = pd.DataFrame(allie)
de = pd.DataFrame(enemy)

#group by each champion to get number of win and losses
al_wins = dt.groupby('Winner').size()
al_losses = dt.groupby('Loser').size()
en_wins = de.groupby('Winner').size()
en_losses = de.groupby('Loser').size()

#new datafram to put them together and put them in an excel sheet.
Allie = pd.DataFrame({'Wins' : al_wins, 'Losses' : al_losses}).fillna(0)
Enemy = pd.DataFrame({'Wins' : en_wins, 'Losses' : en_losses}).fillna(0)
Allie.to_excel('allie.xlsx', sheet_name='allie_test', index=True)
Enemy.to_excel('enemy.xlsx', sheet_name='enemy_test', index=True)