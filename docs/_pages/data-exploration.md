---
layout: page
title: Data Exploration
permalink: /data/explore/
---

This page was created from a Jupyter notebook. The original notebook can be found [here](https://github.com/klane/databall/blob/master/notebooks/data-exploration.ipynb). It explores some of the data contained in or derived from the database. First we must import the necessary installed modules.


```python
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
```

Next we need to import a local module to calculate some advanced stats not stored in the database.


```python
import os
import sys

module_path = os.path.abspath(os.path.join('..'))

if module_path not in sys.path:
    sys.path.append(module_path)

from nba.database import Database
```

The code below simply customizes font sizes for all the plots that follow.


```python
plt.rc('font', size=14)        # controls default text sizes
plt.rc('axes', titlesize=16)   # fontsize of the axes title
plt.rc('axes', labelsize=16)   # fontsize of the x and y labels
plt.rc('xtick', labelsize=14)  # fontsize of the tick labels
plt.rc('ytick', labelsize=14)  # fontsize of the tick labels
plt.rc('legend', fontsize=14)  # legend fontsize
```

We then need to connect to the database generated during the [data wrangling](data-wrangling.md) process.


```python
conn = sqlite3.connect('../nba.db')
```

Without knowing what two teams are playing, a reasonable baseline prediction is probably that the home team wins. Let's take a look at how often that actually happens in the NBA. The SQL query below calculates the home team's winning percentage since the 1990-91 season and groups the results by season. Specifically, it sums up all occurrences of 'W' in the HOME_WL column and divides by the total number of games in a given season.


```python
data = pd.read_sql('''
    SELECT SEASON,
           100.0 * SUM(CASE WHEN HOME_WL = 'W' THEN 1 ELSE 0 END) / COUNT(HOME_WL) AS HomeWinPct
    FROM games
    WHERE SEASON >= 1990
    GROUP BY SEASON''', conn)
```

The plot below shows the win percentage for all home teams across the league from 1990-2015. The chart along with the annotation show that the home team wins about 60% of the time historically. That rate is also remarkably consistent. It has a standard deviation of less than 2% and has stayed within about $$\pm$$4% since the 1990-91 season. FiveThirtyEight [reported](https://fivethirtyeight.com/features/a-home-playoff-game-is-a-big-advantage-unless-you-play-hockey/) a similar percentage when analyzing home court/field/ice advantages of the four major American sports. They calculated that the home team in the NBA has won 59.9% of regular season games since the 2000 season. They also estimated that playing at home provides the biggest advantage in the NBA, where home teams win nearly 10% more games than expected had all games been played at neutral sites. Contrast that with MLB, where home teams win only 4% more games than expected. It is interesting to note that regardless of the sport, FiveThirtyEight's models expect the "home" team to win about 50% of the time on neutral sites, which makes sense when averaged across all teams and multiple seasons.


```python
pct = data.HomeWinPct
plt.figure(figsize=(10, 6))
plt.plot(data.SEASON, pct)
plt.text(1990.5, 83,
         '$\mu=${0:.1f}%\n$\sigma=${1:.1f}%\nRange = {2:.1f}%'
         .format(np.mean(pct), np.std(pct), np.ptp(pct)))
plt.xlabel('Season')
plt.ylabel('NBA Home Team Win Percentage')
plt.title('NBA Home Teams Win Predictably Often')
plt.xlim(1990, 2015)
plt.ylim(0, 100)
plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/home-win-pct.png){: .center-image }

## Historically Great Teams

Now let's calculate some advanced stats from the basic box score data. The code below returns a Pandas DataFrame with season-averaged team offensive and defensive ratings (points scored/allowed per 100 possessions), as well as SRS defined during [data wrangling](data-wrangling.md).


```python
database = Database('../nba.db')
season_stats = database.season_stats()
```

We are first going to look at teams that have some of the best offenses and defenses in NBA history. Since the team stats table includes a team ID that maps to a teams table, we need to pull in the teams table to better identify which teams we are looking at.


```python
teams = pd.read_sql('SELECT * FROM TEAMS', conn)
```

Below are the limits for what defines a great offense, defense, and well-balanced team (high net rating). These limits are not formally defined and are merely selected such that the resulting number of teams is small.


```python
off_lim = 114
def_lim = 98
net_lim = 9
off_flag = (season_stats.TEAM_OFF_RTG > off_lim) & (season_stats.SEASON >= 1990)
def_flag = (season_stats.TEAM_DEF_RTG < def_lim) & (season_stats.SEASON >= 1990)
net_flag = (season_stats.TEAM_NET_RTG > net_lim) & (season_stats.SEASON >= 1990)
stats = ['SEASON', 'TEAM_ID', 'TEAM_OFF_RTG', 'TEAM_DEF_RTG', 'TEAM_NET_RTG', 'TEAM_SRS']
```

There are 13 teams since the 1990-91 season with an offensive rating greater than 114 and 4 of them are Jordan-led Bulls teams. The only other teams to appear more than once are the Suns (one led by Charles Barkley and two by the duo of Steve Nash and Amar'e Stoudemire) and the Warriors (one led by hall of famer Chris Mullin and the record-setting 2015-16 team). Note that the NBA's database does not differentiate teams that change location and/or mascots, so the table identifies the 1994 Oklahoma City Thunder, even though they were the Seattle SuperSonics at the time.


```python
# Isolate desired teams
best_off = season_stats.loc[off_flag, stats]

# Merge with teams table to add team information
best_off = teams.merge(best_off, left_on='ID', right_on='TEAM_ID')

# Remove ID columns
best_off = best_off[[c for c in best_off.columns if 'ID' not in c]]

# Sort by descending offensive rating
best_off.sort_values(by='TEAM_OFF_RTG', ascending=False)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ABBREVIATION</th>
      <th>CITY</th>
      <th>MASCOT</th>
      <th>SEASON</th>
      <th>TEAM_OFF_RTG</th>
      <th>TEAM_DEF_RTG</th>
      <th>TEAM_NET_RTG</th>
      <th>TEAM_SRS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1991</td>
      <td>116.189211</td>
      <td>105.151816</td>
      <td>11.037395</td>
      <td>10.068209</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1995</td>
      <td>115.933867</td>
      <td>102.438493</td>
      <td>13.495374</td>
      <td>11.799077</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ORL</td>
      <td>Orlando</td>
      <td>Magic</td>
      <td>1994</td>
      <td>115.824746</td>
      <td>108.447942</td>
      <td>7.376804</td>
      <td>6.438905</td>
    </tr>
    <tr>
      <th>11</th>
      <td>OKC</td>
      <td>Oklahoma City</td>
      <td>Thunder</td>
      <td>1994</td>
      <td>115.429696</td>
      <td>106.876043</td>
      <td>8.553653</td>
      <td>7.907164</td>
    </tr>
    <tr>
      <th>10</th>
      <td>PHX</td>
      <td>Phoenix</td>
      <td>Suns</td>
      <td>2009</td>
      <td>115.341356</td>
      <td>110.211671</td>
      <td>5.129685</td>
      <td>4.677408</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1990</td>
      <td>115.229301</td>
      <td>105.703474</td>
      <td>9.525826</td>
      <td>8.565998</td>
    </tr>
    <tr>
      <th>12</th>
      <td>UTA</td>
      <td>Utah</td>
      <td>Jazz</td>
      <td>1994</td>
      <td>114.985616</td>
      <td>106.354448</td>
      <td>8.631169</td>
      <td>7.751535</td>
    </tr>
    <tr>
      <th>8</th>
      <td>PHX</td>
      <td>Phoenix</td>
      <td>Suns</td>
      <td>1994</td>
      <td>114.930813</td>
      <td>110.902597</td>
      <td>4.028215</td>
      <td>3.849692</td>
    </tr>
    <tr>
      <th>9</th>
      <td>PHX</td>
      <td>Phoenix</td>
      <td>Suns</td>
      <td>2004</td>
      <td>114.531469</td>
      <td>107.143974</td>
      <td>7.387495</td>
      <td>7.076859</td>
    </tr>
    <tr>
      <th>6</th>
      <td>GSW</td>
      <td>Golden State</td>
      <td>Warriors</td>
      <td>2015</td>
      <td>114.495585</td>
      <td>103.776436</td>
      <td>10.719149</td>
      <td>10.380270</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1996</td>
      <td>114.352283</td>
      <td>102.373550</td>
      <td>11.978733</td>
      <td>10.697142</td>
    </tr>
    <tr>
      <th>0</th>
      <td>CLE</td>
      <td>Cleveland</td>
      <td>Cavaliers</td>
      <td>1991</td>
      <td>114.335981</td>
      <td>108.610216</td>
      <td>5.725766</td>
      <td>5.340416</td>
    </tr>
    <tr>
      <th>5</th>
      <td>GSW</td>
      <td>Golden State</td>
      <td>Warriors</td>
      <td>1991</td>
      <td>114.060850</td>
      <td>110.310391</td>
      <td>3.750460</td>
      <td>3.766748</td>
    </tr>
  </tbody>
</table>
</div>



There are 11 teams since 1990 with a defensive rating under 98 and 3 of them are late 90s/early 2000s Spurs teams with Tim Duncan, two of which featured hall of famer David Robinson. What is more impressive is that they are the only team to grace this list more than once.


```python
# Isolate desired teams
best_def = season_stats.loc[def_flag, stats]

# Merge with teams table to add team information
best_def = teams.merge(best_def, left_on='ID', right_on='TEAM_ID')

# Remove ID columns
best_def = best_def[[c for c in best_def.columns if 'ID' not in c]]

# Sort by ascending defensive rating
best_def.sort_values(by='TEAM_DEF_RTG')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ABBREVIATION</th>
      <th>CITY</th>
      <th>MASCOT</th>
      <th>SEASON</th>
      <th>TEAM_OFF_RTG</th>
      <th>TEAM_DEF_RTG</th>
      <th>TEAM_NET_RTG</th>
      <th>TEAM_SRS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2003</td>
      <td>102.248071</td>
      <td>94.178366</td>
      <td>8.069705</td>
      <td>7.512427</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>1998</td>
      <td>104.036733</td>
      <td>95.000784</td>
      <td>9.035949</td>
      <td>7.151218</td>
    </tr>
    <tr>
      <th>10</th>
      <td>DET</td>
      <td>Detroit</td>
      <td>Pistons</td>
      <td>2003</td>
      <td>102.057437</td>
      <td>95.440557</td>
      <td>6.616880</td>
      <td>5.035363</td>
    </tr>
    <tr>
      <th>0</th>
      <td>ATL</td>
      <td>Atlanta</td>
      <td>Hawks</td>
      <td>1998</td>
      <td>100.516244</td>
      <td>97.138526</td>
      <td>3.377719</td>
      <td>2.790164</td>
    </tr>
    <tr>
      <th>3</th>
      <td>IND</td>
      <td>Indiana</td>
      <td>Pacers</td>
      <td>2003</td>
      <td>103.866828</td>
      <td>97.324036</td>
      <td>6.542792</td>
      <td>4.932295</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ORL</td>
      <td>Orlando</td>
      <td>Magic</td>
      <td>1998</td>
      <td>100.297189</td>
      <td>97.382225</td>
      <td>2.914964</td>
      <td>3.082168</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NYK</td>
      <td>New York</td>
      <td>Knicks</td>
      <td>1998</td>
      <td>98.636273</td>
      <td>97.471817</td>
      <td>1.164456</td>
      <td>1.423433</td>
    </tr>
    <tr>
      <th>4</th>
      <td>PHI</td>
      <td>Philadelphia</td>
      <td>76ers</td>
      <td>1998</td>
      <td>99.928127</td>
      <td>97.632210</td>
      <td>2.295917</td>
      <td>2.528796</td>
    </tr>
    <tr>
      <th>6</th>
      <td>POR</td>
      <td>Portland</td>
      <td>Trail Blazers</td>
      <td>1998</td>
      <td>104.759421</td>
      <td>97.734222</td>
      <td>7.025199</td>
      <td>5.697009</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2000</td>
      <td>106.556068</td>
      <td>97.962401</td>
      <td>8.593667</td>
      <td>7.916999</td>
    </tr>
    <tr>
      <th>5</th>
      <td>PHX</td>
      <td>Phoenix</td>
      <td>Suns</td>
      <td>2000</td>
      <td>100.321422</td>
      <td>97.966276</td>
      <td>2.355146</td>
      <td>2.626301</td>
    </tr>
  </tbody>
</table>
</div>



The 16 teams listed below have a net rating greater than 9 and are some of the strongest teams in NBA history. These include 4 of the Jordan-led Bulls and two of the recent Warriors teams. Only one of the strong defensive teams isolated above make the cut, while 5 of the strong offensive teams appear. As before, note that the 1993 Oklahoma City Thunder were in fact the Seattle SuperSonics.


```python
# Isolate desired teams
best_net = season_stats.loc[net_flag, stats]

# Merge with teams table to add team information
best_net = teams.merge(best_net, left_on='ID', right_on='TEAM_ID')

# Remove ID columns
best_net = best_net[[c for c in best_net.columns if 'ID' not in c]]

# Sort by descending net rating
best_net.sort_values(by='TEAM_NET_RTG', ascending=False)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ABBREVIATION</th>
      <th>CITY</th>
      <th>MASCOT</th>
      <th>SEASON</th>
      <th>TEAM_OFF_RTG</th>
      <th>TEAM_DEF_RTG</th>
      <th>TEAM_NET_RTG</th>
      <th>TEAM_SRS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1995</td>
      <td>115.933867</td>
      <td>102.438493</td>
      <td>13.495374</td>
      <td>11.799077</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1996</td>
      <td>114.352283</td>
      <td>102.373550</td>
      <td>11.978733</td>
      <td>10.697142</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2015</td>
      <td>110.290021</td>
      <td>98.962236</td>
      <td>11.327785</td>
      <td>10.276618</td>
    </tr>
    <tr>
      <th>0</th>
      <td>BOS</td>
      <td>Boston</td>
      <td>Celtics</td>
      <td>2007</td>
      <td>110.171323</td>
      <td>98.933715</td>
      <td>11.237609</td>
      <td>9.307345</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1991</td>
      <td>116.189211</td>
      <td>105.151816</td>
      <td>11.037395</td>
      <td>10.068209</td>
    </tr>
    <tr>
      <th>8</th>
      <td>GSW</td>
      <td>Golden State</td>
      <td>Warriors</td>
      <td>2015</td>
      <td>114.495585</td>
      <td>103.776436</td>
      <td>10.719149</td>
      <td>10.380270</td>
    </tr>
    <tr>
      <th>7</th>
      <td>GSW</td>
      <td>Golden State</td>
      <td>Warriors</td>
      <td>2014</td>
      <td>111.603607</td>
      <td>101.354296</td>
      <td>10.249311</td>
      <td>10.008125</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CLE</td>
      <td>Cleveland</td>
      <td>Cavaliers</td>
      <td>2008</td>
      <td>112.441598</td>
      <td>102.432204</td>
      <td>10.009394</td>
      <td>8.680389</td>
    </tr>
    <tr>
      <th>14</th>
      <td>OKC</td>
      <td>Oklahoma City</td>
      <td>Thunder</td>
      <td>2012</td>
      <td>112.398592</td>
      <td>102.609581</td>
      <td>9.789011</td>
      <td>9.149670</td>
    </tr>
    <tr>
      <th>15</th>
      <td>UTA</td>
      <td>Utah</td>
      <td>Jazz</td>
      <td>1996</td>
      <td>113.642224</td>
      <td>103.950239</td>
      <td>9.691985</td>
      <td>7.969128</td>
    </tr>
    <tr>
      <th>13</th>
      <td>OKC</td>
      <td>Oklahoma City</td>
      <td>Thunder</td>
      <td>1993</td>
      <td>111.969516</td>
      <td>102.366973</td>
      <td>9.602543</td>
      <td>8.675828</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1990</td>
      <td>115.229301</td>
      <td>105.703474</td>
      <td>9.525826</td>
      <td>8.565998</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2006</td>
      <td>109.199410</td>
      <td>99.859543</td>
      <td>9.339868</td>
      <td>8.347217</td>
    </tr>
    <tr>
      <th>6</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>2011</td>
      <td>107.405392</td>
      <td>98.284632</td>
      <td>9.120760</td>
      <td>7.426924</td>
    </tr>
    <tr>
      <th>9</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>1999</td>
      <td>107.325502</td>
      <td>98.224840</td>
      <td>9.100663</td>
      <td>8.413792</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>1998</td>
      <td>104.036733</td>
      <td>95.000784</td>
      <td>9.035949</td>
      <td>7.151218</td>
    </tr>
  </tbody>
</table>
</div>



The following table shows all NBA champions since the 1990-91 season. Not surprisingly, most of the champions have solid net ratings and SRS numbers with the 1995 Bulls shining above all other teams. The weakest champion by these measures is the 1994 Rockets led by hall of famers Hakeem Olajuwon and Clyde Drexler.


```python
# Create champions table that identifies which team won the NBA championship each season
champs = pd.DataFrame({'SEASON': range(1990, 2016),
                       'ABBREVIATION': ['CHI', 'CHI', 'CHI', 'HOU', 'HOU', 'CHI', 'CHI', 'CHI', 'SAS',
                                        'LAL', 'LAL', 'LAL', 'SAS', 'DET', 'SAS', 'MIA', 'SAS', 'BOS',
                                        'LAL', 'LAL', 'DAL', 'MIA', 'MIA', 'SAS', 'GSW', 'CLE']})
# Isolate desired stats from all teams
champ_stats = season_stats[stats]

# Merge with teams table to add team information
champ_stats = teams.merge(champ_stats, left_on='ID', right_on='TEAM_ID')

# Merge with champs table created above
columns = ['ABBREVIATION', 'SEASON']
champ_stats = champs.merge(champ_stats, left_on=columns, right_on=columns)

# Remove ID columns
champ_stats = champ_stats[[c for c in best_net.columns if 'ID' not in c]]
champ_stats
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ABBREVIATION</th>
      <th>CITY</th>
      <th>MASCOT</th>
      <th>SEASON</th>
      <th>TEAM_OFF_RTG</th>
      <th>TEAM_DEF_RTG</th>
      <th>TEAM_NET_RTG</th>
      <th>TEAM_SRS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1990</td>
      <td>115.229301</td>
      <td>105.703474</td>
      <td>9.525826</td>
      <td>8.565998</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1991</td>
      <td>116.189211</td>
      <td>105.151816</td>
      <td>11.037395</td>
      <td>10.068209</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1992</td>
      <td>113.620324</td>
      <td>106.822864</td>
      <td>6.797459</td>
      <td>6.192637</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HOU</td>
      <td>Houston</td>
      <td>Rockets</td>
      <td>1993</td>
      <td>106.444671</td>
      <td>101.900362</td>
      <td>4.544309</td>
      <td>4.194021</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HOU</td>
      <td>Houston</td>
      <td>Rockets</td>
      <td>1994</td>
      <td>110.403045</td>
      <td>108.140634</td>
      <td>2.262411</td>
      <td>2.318131</td>
    </tr>
    <tr>
      <th>5</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1995</td>
      <td>115.933867</td>
      <td>102.438493</td>
      <td>13.495374</td>
      <td>11.799077</td>
    </tr>
    <tr>
      <th>6</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1996</td>
      <td>114.352283</td>
      <td>102.373550</td>
      <td>11.978733</td>
      <td>10.697142</td>
    </tr>
    <tr>
      <th>7</th>
      <td>CHI</td>
      <td>Chicago</td>
      <td>Bulls</td>
      <td>1997</td>
      <td>107.696343</td>
      <td>99.779691</td>
      <td>7.916652</td>
      <td>7.244613</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>1998</td>
      <td>104.036733</td>
      <td>95.000784</td>
      <td>9.035949</td>
      <td>7.151218</td>
    </tr>
    <tr>
      <th>9</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>1999</td>
      <td>107.325502</td>
      <td>98.224840</td>
      <td>9.100663</td>
      <td>8.413792</td>
    </tr>
    <tr>
      <th>10</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>2000</td>
      <td>108.435083</td>
      <td>104.794734</td>
      <td>3.640349</td>
      <td>3.742580</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>2001</td>
      <td>109.407427</td>
      <td>101.713071</td>
      <td>7.694357</td>
      <td>7.145147</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2002</td>
      <td>105.629877</td>
      <td>99.659960</td>
      <td>5.969917</td>
      <td>5.649958</td>
    </tr>
    <tr>
      <th>13</th>
      <td>DET</td>
      <td>Detroit</td>
      <td>Pistons</td>
      <td>2003</td>
      <td>102.057437</td>
      <td>95.440557</td>
      <td>6.616880</td>
      <td>5.035363</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2004</td>
      <td>107.496327</td>
      <td>98.774515</td>
      <td>8.721811</td>
      <td>7.835147</td>
    </tr>
    <tr>
      <th>15</th>
      <td>MIA</td>
      <td>Miami</td>
      <td>Heat</td>
      <td>2005</td>
      <td>108.659652</td>
      <td>104.454414</td>
      <td>4.205239</td>
      <td>3.592696</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2006</td>
      <td>109.199410</td>
      <td>99.859543</td>
      <td>9.339868</td>
      <td>8.347217</td>
    </tr>
    <tr>
      <th>17</th>
      <td>BOS</td>
      <td>Boston</td>
      <td>Celtics</td>
      <td>2007</td>
      <td>110.171323</td>
      <td>98.933715</td>
      <td>11.237609</td>
      <td>9.307345</td>
    </tr>
    <tr>
      <th>18</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>2008</td>
      <td>112.815873</td>
      <td>104.735539</td>
      <td>8.080334</td>
      <td>7.112944</td>
    </tr>
    <tr>
      <th>19</th>
      <td>LAL</td>
      <td>Los Angeles</td>
      <td>Lakers</td>
      <td>2009</td>
      <td>108.764387</td>
      <td>103.716801</td>
      <td>5.047586</td>
      <td>4.782049</td>
    </tr>
    <tr>
      <th>20</th>
      <td>DAL</td>
      <td>Dallas</td>
      <td>Mavericks</td>
      <td>2010</td>
      <td>109.671262</td>
      <td>105.041587</td>
      <td>4.629675</td>
      <td>4.407577</td>
    </tr>
    <tr>
      <th>21</th>
      <td>MIA</td>
      <td>Miami</td>
      <td>Heat</td>
      <td>2011</td>
      <td>106.630278</td>
      <td>100.150438</td>
      <td>6.479840</td>
      <td>5.719582</td>
    </tr>
    <tr>
      <th>22</th>
      <td>MIA</td>
      <td>Miami</td>
      <td>Heat</td>
      <td>2012</td>
      <td>112.332835</td>
      <td>103.744087</td>
      <td>8.588748</td>
      <td>7.031001</td>
    </tr>
    <tr>
      <th>23</th>
      <td>SAS</td>
      <td>San Antonio</td>
      <td>Spurs</td>
      <td>2013</td>
      <td>110.501196</td>
      <td>102.404512</td>
      <td>8.096684</td>
      <td>7.994012</td>
    </tr>
    <tr>
      <th>24</th>
      <td>GSW</td>
      <td>Golden State</td>
      <td>Warriors</td>
      <td>2014</td>
      <td>111.603607</td>
      <td>101.354296</td>
      <td>10.249311</td>
      <td>10.008125</td>
    </tr>
    <tr>
      <th>25</th>
      <td>CLE</td>
      <td>Cleveland</td>
      <td>Cavaliers</td>
      <td>2015</td>
      <td>110.873303</td>
      <td>104.496954</td>
      <td>6.376349</td>
      <td>5.452116</td>
    </tr>
  </tbody>
</table>
</div>



The scatter plot below shows all teams since 1990 represented by their offensive and defensive ratings. The strongest teams are towards the bottom right, those that score a lot and do not give up many points. The line represents a constant net rating of 9, below which are the 16 teams listed above that have a net rating greater than 9.


```python
# Add line of constant net rating
x = np.array([95, 120])
plt.figure(figsize=(10, 8))
plt.plot(x, x-net_lim, 'black', label='Net Rating = %d' % net_lim)

# Isolate teams that do not make the offensive/defensive/net rating cutoffs
others = season_stats.loc[~off_flag & ~def_flag & ~net_flag & (season_stats.SEASON >= 1990), stats]
others = teams.merge(others, left_on='ID', right_on='TEAM_ID')

# Remove the champions with an outer join
columns = ['ABBREVIATION', 'SEASON']
others = champs.merge(others, left_on=columns, right_on=columns, how='outer', indicator=True)
others = others[others._merge == 'right_only']

# Plot data
plt.scatter(x='TEAM_OFF_RTG', y='TEAM_DEF_RTG', data=others, label='Everyone Else')
plt.scatter(x='TEAM_OFF_RTG', y='TEAM_DEF_RTG', data=best_off, label='Off Rating > %d' % off_lim)
plt.scatter(x='TEAM_OFF_RTG', y='TEAM_DEF_RTG', data=best_def, label='Def Rating < %d' % def_lim)
plt.scatter(x='TEAM_OFF_RTG', y='TEAM_DEF_RTG', data=best_net, label='Net Rating > %d' % net_lim)
plt.scatter(x='TEAM_OFF_RTG', y='TEAM_DEF_RTG', data=champ_stats, label='Champions')

# Label axes and add legend
plt.legend()
plt.xlabel('Offensive Rating')
plt.ylabel('Defensive Rating')
plt.xlim(90, 120)
plt.ylim(90, 120)
plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/ratings-scatter.png){: .center-image }

## Team Strength Distribution

The histogram and kernel density estimation (KDE) of team SRS below show that teams are fairly normally distributed. The best fit normal distribution has a mean of essentially zero with a standard deviation of about 4.6 points. A zero-mean distribution makes sense here because an SRS of zero indicates a perfectly average team.


```python
srs = season_stats['TEAM_SRS']
(mu, sigma) = norm.fit(srs)

plt.figure(figsize=(12, 6))
ax = sns.distplot(srs, fit=norm, kde=True, kde_kws={'label': 'KDE', 'color': 'green', 'linewidth': 3},
                  hist_kws={'label': 'SRS', 'edgecolor': 'k', 'linewidth': 2},
                  fit_kws={'label': 'Normal Dist ($\mu=${0:.2g}, $\sigma=${1:.2f})'.format(mu, sigma),
                           'linewidth': 3})
ax.legend()
plt.xlabel('SRS')
plt.ylabel('Frequency')
plt.title('Most NBA Teams are Average')
plt.xlim(-20, 20)
plt.ylim(0, 0.1)
plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/srs-distribution.png){: .center-image }

## Home vs. Away Strength

The next step is to look at games in terms of home and away team stats. The code below joins the games table with the stats table initially by home team stats and followed by away team stats.


```python
seasons = season_stats.filter(regex='SEASON|TEAM')
games = pd.read_sql('SELECT * FROM games', conn)
games = games.merge(seasons, left_on=['SEASON', 'HOME_TEAM_ID'], right_on=['SEASON', 'TEAM_ID'])
games = games.merge(seasons, left_on=['SEASON', 'AWAY_TEAM_ID'], right_on=['SEASON', 'TEAM_ID'], 
                    suffixes=('', '_AWAY'))
```

The plot below shows a 2D KDE that compares home and away team SRS. By inspection, the majority of games occur between teams with SRS values within 5 points of average. This makes intuitive sense given the standard deviation of 4.6 points calculated above. Assuming the Gaussian distribution above, more than 68% of all teams since 1990 have SRS values with a magnitude less than 5 based on the definition of a normal distribution. The distribution appears symmetric about a y=x line because under normal circumstances (each team plays a full season), teams have the same number of home and away games. 


```python
ax = sns.jointplot(x='TEAM_SRS', y='TEAM_SRS_AWAY', data=games, kind='kde',
                   shade_lowest=False, stat_func=None, xlim=(-15, 15), ylim=(-15, 15), size=8)
ax.set_axis_labels(xlabel='Home Team SRS', ylabel='Away Team SRS')
plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/srs-kde.png){: .center-image }

The function below makes and customizes KDE plots of home and away team stats.


```python
def kde(data, stat, label, title, ax):
    stat = 'TEAM_' + stat
    sns.kdeplot(data[stat], data[stat + '_AWAY'], cmap='Blues', shade=True, shade_lowest=False, ax=ax)
    ax.plot(0, 0, 'or')
    ax.set_xlabel('Home Team ' + label)
    ax.set_ylabel('Away Team ' + label)
    ax.set_title(title)
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
```

A better view of this data is to separate games into home team wins and losses. The plots below show KDE plots of SRS for home team wins and losses with a red marker added to easily identify the origin (average home and away teams). The high-density area towards the lower right of the origin for home team wins (left plot) indicates there are many games in the dataset where above-average home teams beat below-average away teams, which is not a surprising revelation. We draw the opposite conclusion for home team losses. The highest density occurs towards the upper left of the origin, meaning games where a below-average home team plays an above-average visiting teams typically does not go well for the home team. There is also a small cluster of games in the left plot where above-average home teams beat above-average visitors of roughly equal quality. This may be caused by home court advantage, but was not investigated further.


```python
plt.figure(figsize=(14, 6))

# Find games where the home team won
kde(games[games.HOME_WL=='W'], 'SRS', 'SRS', 'KDE of Home Team Wins', plt.subplot(121))

# Find games where the home team lost
kde(games[games.HOME_WL=='L'], 'SRS', 'SRS', 'KDE of Home Team Losses', plt.subplot(122))

plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/srs-win-loss-kde.png){: .center-image }

The KDE plots below repeat those above for team net ratings (offensive rating - defensive rating). They illustrate that the same trends hold true for net ratings as did for SRS above.


```python
plt.figure(figsize=(14, 6))

# Find games where the home team won
kde(games[games.HOME_WL=='W'], 'NET_RTG', 'Net Rating', 'KDE of Home Team Wins', plt.subplot(121))

# Find games where the home team lost
kde(games[games.HOME_WL=='L'], 'NET_RTG', 'Net Rating', 'KDE of Home Team Losses', plt.subplot(122))

plt.show()
```


![png]({{ site.baseurl }}/assets/images/data-exploration/net-rating-win-loss-kde.png){: .center-image }
