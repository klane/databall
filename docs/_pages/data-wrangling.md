---
layout: default
title: Stats
permalink: /data/wrangling/
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

Steps 2 and 3 can be wrapped in a loop to store stats for different seasons. I used this process to create a database with player and team stats for full seasons since the 1996-97 season and for individual games going back to the 1989-90 season. The season stats start later because the NBA stats website only includes [season stats](http://stats.nba.com/teams/traditional/) since the 1996-97 season, something I did not realize initially, but [box scores](http://stats.nba.com/teams/boxscores/) go back much further. All season stats moving forward are actually averaged from box scores to permit analysis of seasons prior to 1996. The code used to generate the database is located [here](https://github.com/klane/nba/blob/master/nba/database_builder.py).

# Calculating Advanced Stats

We now have a database containing box score stats, but the raw numbers are not all that useful by themselves. We can get more meaningful numbers by calculating a few advanced stats. These stats are included on a combination of sites such as [stats.nba.com](http://stats.nba.com), [Basketball-Reference.com](http://www.basketball-reference.com/), and [ESPN](http://www.espn.com/nba/statistics). In the case of the NBA stats website, the advanced stats JSON endpoint is only for individual games, meaning I must query the site with each game's unique ID. I would much rather use the GameLog class described above to obtain a full season's worth of box scores at once and calculate desired stats. I could also write a web scraper to read the stats, but many sites have game stats for a single season spread across multiple pages. I found it more flexible to save box scores from the GameLog class and leverage them to calculate additional stats.

## Offensive & Defensive Ratings

The analytics community typically looks at pace-adjusted numbers (see the [Hang Time Blog](http://hangtime.blogs.nba.com/2013/02/15/the-new-nba-comstats-advanced-stats-all-start-with-pace-and-efficiency/) and [Nylon Calculus](http://fansided.com/2015/12/21/nylon-calculus-101-possessions/) for some good discussions) instead of per-game stats to get a picture of team strength. A team scoring 100 points in a game where it had 100 possessions is obviously not as impressive as a team scoring the same number of points in only 90 possessions. The latter team was more efficient with their possessions. Since box scores do not include the number of possessions, we must estimate them. I use Basketball-Reference.com's [definition](http://www.basketball-reference.com/about/glossary.html) that averages both teams' stats in a given game. With this estimate along with points scored/allowed in each game, we can calculate offensive/defensive ratings (also referred to as offensive/defensive efficiencies), which is the number of points scored/allowed per 100 possessions. The difference between the two is called net rating and measures point differential per 100 possessions.

## Simple Rating System

Another stat that models team strength is Sports-Reference.com's [Simple Rating System](http://www.sports-reference.com/blog/2015/03/srs-calculation-details/) (SRS), which was first introduced by [Pro-Football-Reference.com](http://www.pro-football-reference.com/blog/index4837.html?p=37). It amounts to team strength relative to an average opponent. A team with an SRS of 5 is considered 5 points better than an average team. It is calculated as average margin of victory adjusted for each team's strength of schedule.

## Four Factors

Another set of stats that can be easily calculated are coined the four factors. They aim to identify four key areas that winning teams excel at, namely efficient shooting, rebounding, minimizing turnovers, and getting to the free throw line. The [NBA](http://stats.nba.com/help/faq/) and [Basketball-Reference.com](http://www.basketball-reference.com/about/factors.html) differ slightly in their definitions of the four factors. The NBA's turnover percentage includes assists in the denominator. They also use free throw attempt rate (FTA/FGA) whereas Basketball-Reference.com uses free throw rate (FT/FGA). Basketball-Reference.com uses free throw rate to not only measure how often teams get to the free throw line, but also how often they convert those chances. A team that gets fouled a lot but shoots free throws at a low percentage will have a high free throw attempt rate even though their poor foul shooting cost them easy points. However, Basketball-Reference.com's free throw factor is not impressed by fruitless trips to the free throw line. I use Basketball-Reference.com's definition of the four factors for my analysis.
