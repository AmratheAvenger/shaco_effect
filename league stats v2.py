from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time

# golbal variables
api_key = 'RGAPI-c0b5b53f-8225-4137-b7b6-b0c87fce00e4'
watcher = LolWatcher(api_key)
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'AmratheAvenger')

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index=0)
match_list = my_matches['matches']

#print(match_list)
# fetch last match detail
last_match = my_matches['matches'][0]
#print(last_match)
match_detail = watcher.match.by_id(my_region, last_match['gameId'])
#print(match_detail['teams'])

""" participants = []
for row in match_detail['participants']:
    participants_row = {}
    participants_row['win'] = row['stats']['win']
    participants_row['teamId'] = row['teamId']
    participants_row['champion'] = row['championId']
    participants.append(participants_row)
#df = pd.DataFrame(participants) """
#df

""" participants = []
for row in match_detail['participants']:
    participants_row = {}
    participants_row['teamId'] = row['teamId']
    participants_row['champion'] = row['championId']
    participants_row['spell1'] = row['spell1Id']
    participants_row['spell2'] = row['spell2Id']
    participants_row['win'] = row['stats']['win']
    participants_row['kills'] = row['stats']['kills']
    participants_row['deaths'] = row['stats']['deaths']
    participants_row['assists'] = row['stats']['assists']
    participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
    participants_row['goldEarned'] = row['stats']['goldEarned']
    participants_row['champLevel'] = row['stats']['champLevel']
    participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
    participants_row['item0'] = row['stats']['item0']
    participants_row['item1'] = row['stats']['item1']
    participants.append(participants_row)
df = pd.DataFrame(participants) """
#print(df) 

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions('10.10.3216176', False, 'en_US')

#static list of champions
champ_dict = {}
champ_enemy = {}
for key in static_champ_list['data']:
    #print(key)
    row = static_champ_list['data'][key]
   # print(row['key'])
    #print(row['id'])
    champ_dict[row['key']] = row['id']
    #print(champ_dict[row['key']]) 
#for champ in champ_dict:
    #print(champ_dict[str(champ)])

full_match_list = []
i = 0
for match in match_list:
  print("Reading full match %d..." % i)
 # print (match['gameId'])
  m = watcher.match.by_id(my_region, match['gameId'])
  full_match_list.append(m)
  i += 1
  if (i == 20):
    break
  time.sleep(1)  # Pause to avoid overwhelming Riot API quota.

i = 0
participants = []
allie = []
enemy = []
for match in full_match_list:

  print("Match:", i)

  # Go through each player in match.
  i += 1
  for parts in match['participantIdentities']:
    if(parts['player']['summonerName'] == 'AmratheAvenger'):
      partId = parts['participantId']
      #print(partId)
      break
   # print(parts['player']['summonerName'])
  for player in match['participants']:
    if(partId == player['participantId']):
      team = player['teamId']
      break
  for player in match['participants']:  
    participants_row = {}
    champ_allie = {}
    champ_enemy = {}
    if((player['teamId'] == team) and player['stats']['win'] == True):
      # print("allie win")
      champ_allie['Winner'] = champ_dict[str(player['championId'])]
      allie.append(champ_allie)
    elif((player['teamId'] == team) and player['stats']['win'] == False):
    #  print("allie_lose")
      champ_allie['Loser'] = champ_dict[str(player['championId'])]
      allie.append(champ_allie)
    elif((player['teamId'] != team) and player['stats']['win'] == True):
      champ_enemy['Winner'] = champ_dict[str(player['championId'])]
      enemy.append(champ_enemy)
    elif((player['teamId'] != team) and player['stats']['win'] == False):
      champ_enemy['Loser'] = champ_dict[str(player['championId'])]
      enemy.append(champ_enemy)

#df = pd.DataFrame(participants)
#df
dt = pd.DataFrame(allie)
de = pd.DataFrame(enemy)
#print (dt.groupby('Winner').size())
#print (dt.groupby('Loser').size()) 
#print (de.groupby('Winner').size())
#print (de.groupby('Loser').size())

al_wins = dt.groupby('Winner').size()
al_losses = dt.groupby('Loser').size()
en_wins = de.groupby('Winner').size()
en_losses = de.groupby('Loser').size()

Allie = pd.DataFrame({'Wins' : al_wins, 'Losses' : al_losses}).fillna(0)
Enemy = pd.DataFrame({'Wins' : en_wins, 'Losses' : en_losses}).fillna(0)
Allie.to_excel('allie.xlsx', sheet_name='allie_test', index=True)
Enemy.to_excel('enemy.xlsx', sheet_name='enemy_test', index=True)

"""            
 for player in match['participants']:
    participants_row = {}
    champ_allie = {}
    champ_enemy = {}
    participants_row['win'] = player['stats']['win']
    print(player['stats']['win'])
    participants_row['teamId'] = player['teamId']
    participants_row['champion'] = player['championId']
    participants_row['championName'] = champ_dict[str(participants_row['champion'] )]
    #participants.append(participants_row)
    #print(player['championId'])
    for champ in champ_dict:
      if(str(player['championId']) == champ):
        print(champ)
        print(player['teamId'] )
        if((player['teamId'] == 200) and player['stats']['win'] == True):
          #print("my team")
          champ_allie['Winner'] = champ_dict[str(player['championId'])]
          allie.append(champ_allie)
        elif((player['teamId'] == 200) and player['stats']['win'] == False):
          champ_allie['Loser'] = champ_dict[str(player['championId'])]
          allie.append(champ_allie)
        elif((player['teamId'] == 100) and player['stats']['win'] == True):
          champ_enemy['Winner'] = champ_dict[str(player['championId'])]
          enemy.append(champ_enemy)
        elif((player['teamId'] == 100) and player['stats']['win'] == False):
          champ_enemy['Loser'] = champ_dict[str(player['championId'])]
          enemy.append(champ_enemy)
            
"""
""" 
for row in participants:
   # print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
    row['championName'] = champ_dict[str(row['champion'])] """

""" i = 0
for match in full_match_list:

  print("Match:", i)

  # Go through each player in match.
  for player in match['participants']:
    id = player['championId']
    #print(id)

    # Find and print matching champion name from list.
    for champ in champ_dict:
      #print(static_champ_list['data'][champ]['id'])
      #print(champ)
      if champ_dict[row['key']] == id:
        print(" ", id, champ)

  i += 1 
 """
# print dataframe
df = pd.DataFrame(participants)
df.to_excel('league_test.xlsx', sheet_name='league_test', index=False)
#print(df) 

#print(match_detail)

#print(me)