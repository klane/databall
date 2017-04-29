---
layout: default
title: Stats
permalink: /data/stats/
---

# Collecting the Data

The NBA provides a wealth of basic and advanced stats on their website [stats.nba.com](http://stats.nba.com). The site exposes a wide variety of information in JSON format through various endpoints and parameters that take the form:

```
stats.nba.com/stats/{endpoint}/?{params}
```

This makes it easy to pull in the data programmatically without having to scrape the page HTML. For example, individual player stats from every game of the 2016-17 regular season can be found [here](http://stats.nba.com/stats/leaguegamelog/?LeagueID=00&Season=2016-17&SeasonType=Regular Season&PlayerOrTeam=P&Sorter=PTS&Direction=DESC). I leveraged the existing GitHub project [nba_py](https://github.com/seemethere/nba_py) that provides a simple Python API to pull data from the NBA stats website. If the user has [Pandas](http://pandas.pydata.org/) installed, the package will return a query as a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). For example, player stats from every game of the 2016-17 regular season can be extracted to a DataFrame with:

```python
  from nba_py.league import GameLog
  stats = GameLog(season='2016-17', season_type='Regular Season', player_or_team='P').overall()
```

The API also provides sensible defaults, such as the current season for the season parameter, which reduces the amount of code required. The code below produces the same output as that above given that this page was written during the 2016-17 season. These two code snippets will produce different results at the start of the 2017-18 campaign.

```python
  from nba_py.league import GameLog
  stats = GameLog().overall()
```

This package reduces the burden on the user by not requiring him or her to format the URL explicitly or know all the various options available. In addition to game stats, the package provides access to season stats, tracking stats, game/season splits, lineups, and several others .

# Storing the Data

Now that I have easy access to NBA stats, I need to store them for later use to avoid grabbing the same data from the NBA stats website multiple times. I chose to store the data in a SQLite database. SQLite provides the functionality of a relational database in a local file and is [described](https://www.sqlite.org/about.html) as self-contained, serverless, and zero-configuration. This coupled with the fact that Python has built-in SQLite support made SQLite a natural fit for this project. A Python connection to a SQLite database named nba.db can be opened with:

```python
  import sqlite3
  conn = sqlite3.connect('nba.db')
```

This will also create the database if it does not exist. Pandas DataFrames have SQL support, so writing the stats obtained in the previous section to the database created above is achieved with a single method call.

```python
  stats.to_sql('player_game_stats', conn, if_exists='append')
```

This writes the stats to the database in a table named player_game_stats. The `if_exists` parameter tells SQLite to append to the table if it already exists. The [default behavior](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html) is to do nothing if the specified table exists. Once the database connection is no longer needed it can be closed with:

```python
  conn.close()
```

The process for generating a database of NBA stats consists of four steps:

1. Open a SQLite database connection.
2. Query the NBA stats website with nba_py.
3. Write the stats DataFrame to the database.
4. Close the database connection.

Steps 2 and 3 can be wrapped in a loop to store stats for different seasons. I used this process to create a database with player and team stats for individual games and full seasons going back to the 1989-90 season. The code used to generate the database is located [here](https://github.com/klane/nba/blob/master/nba/database_builder.py).
