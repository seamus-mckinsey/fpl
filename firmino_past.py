# Historical data pulled from FPL's "element-summary" API

import pandas as pd
import json, requests

r = requests.get('https://fantasy.premierleague.com/drf/element-summary/235')

# Line below will tell us what keys we can work with
r.json().keys()

data = r.json()['history_past']

firmino_past = pd.DataFrame(data)

firmino_past.shape
pd.set_option('display.max_columns', 30)

firmino_past.head()

# I want the columns organized as follows:
# goals scored, assists, value, penalties missed, yellow cards, red cards, saves, bonus, BPS, Influence, Creativity, Threat, ICT Index

# Listing column names below
firmino_past.columns

# Selecting column order
column_order = ['season_name', 'total_points', 'minutes', 'goals_scored', 'assists',
                'bps', 'bonus', 'start_cost', 'end_cost', 'influence', 'creativity',
                'threat', 'ict_index', 'penalties_missed', 'yellow_cards', 'ea_index',
                'element_code', 'goals_conceded', 'clean_sheets', 'id', 'own_goals',
                'penalties_saved', 'red_cards', 'saves', 'season']

# Resetting firmino index so columns are in nicer order
firmino_past = firmino_past[column_order]

firmino_past

# One large problem at the start is that this API (https://fantasy.premierleague.com/drf/element-summary/235)
# does not include the player's name. # However, this site (https://fantasy.premierleague.com/drf/elements/)
# lists all the # players with their current 'id' which still isn't list in the current
# API pull, annoyingly. We will probably want to have a separate for loop in which
# for num in range (1, 500) Python will go into the elements API and pull the player
# name. Then we can run a join later on with the data above


################################################################################

""" Some closing thoughts on the above. If we're interested in doing machine learning
on the data, I'd be curious to try the following features as predictors of either
total_points OR combo of goals_scored & assists
--> bps
--> ict_index
--> threat
--> influence
"""
