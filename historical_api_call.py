# API call for all players in Premier League

import pandas as pd
import numpy as np
import json, requests
from time import sleep

################################################################################

# Will start by pulling data for each player from 1 through 543 (see range below)

df = pd.DataFrame()

type(df)

for i in range (1, 544):
    r = requests.get('https://fantasy.premierleague.com/drf/element-summary/'+str(i))
    data = r.json()['history_past']
    if not data:
        data = [{'assists': 'NaN_',
                        'bonus': 'NaN',
                        'bps': 'NaN',
                        'clean_sheets': 'NaN',
                        'creativity': 'NaN',
                        'ea_index': 'NaN',
                        'element_code': 'NaN_'+str(i),
                        'end_cost': 'NaN',
                        'goals_conceded': 'NaN',
                        'goals_scored': 'NaN',
                        'ict_index': 'NaN',
                        'id': 'NaN',
                        'influence': 'NaN',
                        'minutes': 'NaN',
                        'own_goals': 'NaN',
                        'penalties_missed': 'NaN',
                        'penalties_saved': 'NaN',
                        'red_cards': 'NaN',
                        'saves': 'NaN',
                        'season': 'NaN',
                        'season_name': 'NaN',
                        'start_cost': 'NaN',
                        'threat': 'NaN',
                        'total_points': 'NaN',
                        'yellow_cards': 'NaN'}]
        df1 = pd.DataFrame(data)
    else:
        df1 = pd.DataFrame(data)
    df = df.append(df1, ignore_index=True)
    sleep(.005)
#print(df)


df.shape
df.head(100)


df['unique_element_code'] = pd.factorize(df['element_code'])[0]
df['unique_element_code'] = df['unique_element_code'] + 1

# Running a quick test on firmino historical data (url ending 235)
df[df['unique_element_code']==235]


################################################################################

# This section will pull the player name from https://fantasy.premierleague.com/drf/elements/

e = requests.get('https://fantasy.premierleague.com/drf/elements/')

# checking the keys
list(e)

# Checking the json
elements = e.json()


elements_df = pd.DataFrame(elements)
elements_df.columns

pd.set_option('display.max_columns', 60)
elements_df[['id', 'web_name', 'element_type']]
elements_df = elements_df[['id', 'web_name', 'element_type']]

# Renaming 'id' Series so it'll match with df
elements_df = elements_df.rename(columns = {'id': 'unique_element_code'})

elements_df.head(30)

################################################################################

# Now that we have all the elements, with names, we can merge the DataFrames
# New DataFrame will be called historic

pd.options.display.max_rows = 1900

historic = pd.merge(df, elements_df, on='unique_element_code', how='outer')

historic

historic.shape
historic.dtypes

# Checking Hazard
historic[historic['web_name']=='Hazard']

# Mapping players by position
historic['position'] = historic.element_type.map({1:'goalkeeper', 2:'defender', 3:'midfielder', 4:'forward'})
list(historic.columns)

# Changing the column order
column_order = ['web_name', 'season_name', 'position', 'total_points', 'minutes', 'goals_scored', 'assists',
                'clean_sheets', 'goals_conceded', 'saves', 'bonus', 'bps', 'penalties_missed',
                'penalties_saved', 'start_cost', 'end_cost', 'ict_index', 'influence',
                'creativity', 'threat', 'id', 'element_code', 'ea_index', 'element_type',
                'unique_element_code', 'season', 'red_cards', 'yellow_cards', 'own_goals']
len(column_order)

historic = historic[column_order]

historic.tail(50)

# Saving data to csv
historic.to_csv('historic_data_all_epl_players.csv')
historic['total_points'] = pd.to_numeric(historic['total_points'], errors='coerce')
historic['goals_scored'] = pd.to_numeric(historic['goals_scored'], errors='coerce')

# Quick groupby to see some stats by position
historic.groupby('position').total_points.mean()

historic.groupby('position').goals_scored.mean()
