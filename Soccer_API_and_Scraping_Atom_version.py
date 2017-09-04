# FPL Model -- shortened

import pandas as pd
import requests, json
# requests is a python library that provides useful methods for api requests and webscraping

r = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')

data = r.json()['elements']

pd.set_option('display.max_columns', 60)
pd.options.display.max_rows = 999

df = pd.DataFrame(data)

df[df['web_name']=='Firmino']

df.tail()


df[df['second_name'] == 'Alonso']


df.sort_values(by='total_points', ascending=False)[0:20]

df.columns

columns_to_keep = ['web_name', 'total_points', 'goals_scored', 'assists', 'points_per_game', 'value_form', 'form',
                   'value_season' ,'now_cost', 'bonus', 'bps', 'minutes', 'selected_by_percent',
                   'code', 'ict_index', 'creativity', 'influence', 'threat', 'yellow_cards',
                  ]

df = df[columns_to_keep]
df.dtypes

objects = ['points_per_game', 'value_form', 'form', 'value_season', 'selected_by_percent', 'ict_index',
          'creativity', 'influence', 'threat']

for i in objects:
    df[i] = pd.to_numeric(df[i])

df.dtypes


df.sort_values(by='total_points', ascending=False)


df.sort_values(by='value_form', ascending=False)


df[df['web_name'].isin(['De Bruyne', 'David Silva'])]

#################################################################################

# Adding coefficient and z-score
from scipy import stats
coef_df = df.copy(deep=True)

coef_df.describe()

# Creating coefficient weights here
coef_df['goal_z-score'] = stats.zscore(coef_df['goals_scored'])
coef_df['goal_coef'] = coef_df['goal_z-score'] * 0.35

coef_df['assist_z-score'] = stats.zscore(coef_df['assists'])
coef_df['assist_coef'] = coef_df['assist_z-score'] * 0.20

coef_df['value-form_z-score'] = stats.zscore(coef_df['value_form'])
coef_df['value-form_coef'] = coef_df['value-form_z-score'] * 0.05

coef_df['form_z-score'] = stats.zscore(coef_df['form'])
coef_df['form_coef'] = stats.zscore(coef_df['form_z-score']) * 0.10

coef_df['bps_z-score'] = stats.zscore(coef_df['bps'])
coef_df['bps_coef'] = stats.zscore(coef_df['bps_z-score']) * 0.05

coef_df['ict_z-score'] = stats.zscore(coef_df['ict_index'])
coef_df['ict_coef'] = stats.zscore(coef_df['ict_z-score']) * 0.15

coef_df['total_coef'] = coef_df['goal_coef'] + coef_df['assist_coef'] + coef_df['value-form_coef'] + \
    coef_df['form_coef'] + coef_df['bps_coef'] + coef_df['ict_coef']

# With all the data

coef_df.sort_values(by='total_coef', ascending=False)

coef_df['points_per_min'] = coef_df['total_points'] / coef_df['minutes']


coef_df[coef_df['minutes'] > 90].sort_values(by='points_per_min', ascending=False)


# Consolidated view

coef_df[['web_name', 'ict_index', 'now_cost', 'total_coef', 'minutes',
        'points_per_min']].sort_values(by='total_coef', ascending=False)


coef_df['ppm/now_cost'] = coef_df['points_per_min'] / coef_df['now_cost']
coef_df[['web_name', 'ict_index', 'now_cost', 'total_coef', 'minutes',
        'points_per_min', 'ppm/now_cost']][coef_df['minutes']>90].sort_values(by='ppm/now_cost', ascending=False)[0:40]

coef_df[['web_name', 'ict_index', 'now_cost', 'total_coef', 'minutes',
        'points_per_min', 'ppm/now_cost']][coef_df['minutes']>90][coef_df['now_cost']>70]\
        .sort_values(by='ppm/now_cost', ascending=False)[0:40]


#        [coef_df['minutes']>90][coef_df['now_cost']>70].sort_values(by='ppm/now_cost', ascending=False)[0:40]
