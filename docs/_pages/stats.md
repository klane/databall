---
layout: page
title: Stats
permalink: /data/stats/
---

## Collecting the Data

The NBA provides a wealth of basic and advanced stats on their website [stats.nba.com](http://stats.nba.com). The site exposes a wide variety of information in JSON format through several web API endpoints and parameters that take the form:

```
  stats.nba.com/stats/{endpoint}/?{params}
```

This makes it easy to pull in the data programmatically without having to scrape the page HTML. For example, individual player stats from every game of the 2016-17 regular season can be found [here](http://stats.nba.com/stats/leaguegamelog/?LeagueID=00&Season=2016-17&SeasonType=Regular Season&PlayerOrTeam=P&Sorter=PTS&Direction=DESC). I leveraged the existing GitHub project [nba_py](https://github.com/seemethere/nba_py) that provides a simple Python API to pull data from the NBA stats website. If the user has [Pandas](http://pandas.pydata.org/) installed, the package will return a query as a [`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). For example, player stats from every game of the 2016-17 regular season can be extracted to a `DataFrame` with:

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

## Storing the Data

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

Steps 2 and 3 can be wrapped in a loop to store stats for different seasons. I used this process to create a database with player and team stats for full seasons since the 1996-97 season and for individual games going back to the 1989-90 season. The season stats start later because the NBA stats website only includes [season stats](http://stats.nba.com/teams/traditional/) since the 1996-97 season, something I did not realize initially, but [box scores](http://stats.nba.com/teams/boxscores/) go back much further. All season stats moving forward are actually averaged from box scores to permit analysis of seasons prior to 1996. The code used to generate the database is located [here](https://github.com/klane/databall/blob/master/databall/database_builder.py).

## Calculating Advanced Stats

We now have a database containing box score stats, but the raw numbers are not all that useful by themselves. We can get more meaningful numbers by calculating a few advanced stats. These stats are included on a combination of sites such as [stats.nba.com](http://stats.nba.com), [Basketball-Reference.com](http://www.basketball-reference.com/), and [ESPN](http://www.espn.com/nba/statistics). In the case of the NBA stats website, the advanced stats JSON endpoint is only for individual games, meaning I must query the site with each game's unique ID. I would much rather use the `GameLog` class described above to obtain a full season's worth of box scores at once and calculate desired stats. I could also write a web scraper to read the stats, but many sites have game stats for a single season spread across multiple pages. I found it more flexible to save box scores from the `GameLog` class and leverage them to calculate additional stats.

### Offensive & Defensive Ratings

The analytics community typically looks at pace-adjusted numbers (see the [Hang Time Blog](http://hangtime.blogs.nba.com/2013/02/15/the-new-nba-comstats-advanced-stats-all-start-with-pace-and-efficiency/) and [Nylon Calculus](http://fansided.com/2015/12/21/nylon-calculus-101-possessions/) for some good discussions) instead of per-game stats to get a picture of team strength. A team scoring 100 points in a game where it had 100 possessions is obviously not as impressive as a team scoring the same number of points in only 90 possessions. The latter team was more efficient with their possessions. Since box scores do not include the number of possessions, we must estimate them. [Basketball-Reference.com](http://www.basketball-reference.com/about/glossary.html) calculates possessions as:

$$POSS_{BBREF}=FGA+0.4*FTA-1.07\left(\frac{OREB}{OREB+DREB_{OPP}}\right)(FGA-FG)+TOV$$

where the values from each team are averaged. The NBA's stats site calculates possessions as:

$$POSS_{NBA}=\frac{FGA+0.44*FTA-OREB+TOV}{2}$$

where the totals from each team are included. I use Basketball-Reference.com's definition for my analysis. The terms in the above equations are as follows:

$$\begin{align}
FG & =\text{field goals made} \\
FGA & =\text{field goal attempts} \\
FTA & =\text{free throw attempts} \\
OREB & =\text{offensive rebounds} \\
DREB & =\text{defensive rebounds} \\
TOV & =\text{turnovers}
\end{align}$$

With this estimate along with points scored/allowed in each game, we can calculate offensive/defensive ratings (also referred to as offensive/defensive efficiencies), which is the number of points scored/allowed per 100 possessions. The difference between the two is called net rating and measures point differential per 100 possessions. Offensive and defensive stats are occasionally presented per 48 minutes instead of per 100 possessions or game. To calculate this we need to know a team's pace, or the number of possessions per 48 minutes. This is calculated as:

$$PACE=\frac{240*POSS}{MIN}$$

where 240 is the number of team minutes in a regulation-length game and $$MIN$$ is the number of team minutes played. Therefore, pace equals possessions for a regulation-length game.

### Simple Rating System

Another stat that models team strength is Sports-Reference.com's [Simple Rating System](http://www.sports-reference.com/blog/2015/03/srs-calculation-details/) (SRS), which was first introduced by [Pro-Football-Reference.com](http://www.pro-football-reference.com/blog/index4837.html?p=37). It is a measure of team strength relative to an average opponent. A team with an SRS of 5 is considered 5 points better than an average team. It is calculated as average margin of victory adjusted for strength of schedule. It must be calculated iteratively because each team's rating depends on those of its opponents. The equation is:

$$\begin{align}
\vec{SRS}_i & =\vec{PD}+\mathbf{S}\times\vec{SRS}_{i-1} \\
\vec{SRS}_0 & =\vec{PD}
\end{align}$$

where $$\vec{SRS}_i$$ is a vector of all team's SRS values at iteration $$i$$, $$\vec{PD}$$ is a vector of average point differentials, and $$\mathbf{S}$$ denotes the schedule matrix. Both $$\vec{PD}$$ and $$\mathbf{S}$$ are fixed (do not update with $$i$$) and $$\vec{SRS}$$ is initialized to $$\vec{PD}$$. The schedule matrix is symmetric about the diagonal and $$\mathbf{S}_{i,j}$$ indicates what percentage of team $$i$$'s games were played against team $$j$$. The SRS vector is updated until it converges, which is achieved when the maximum difference between $$\vec{SRS}_i$$ and $$\vec{SRS}_{i-1}$$ is below a selected tolerance. It typically only requires a few iterations to obtain convergence.

### Four Factors

Another set of stats that can be easily calculated were originally identified by Dean Oliver[^1], which he coined the four factors. They aim to identify four key areas---including their relative weights---that winning teams excel at, namely efficient shooting (40%), minimizing turnovers (25%), rebounding (20%), and getting to the free throw line (15%). The percentages in parentheses are the weights Oliver assigned to each factor. [Basketball-Reference.com's](http://www.basketball-reference.com/about/factors.html) definition of the four factors are:

$$\begin{align}
eFG\% & =\frac{FG+0.5*3FG}{FGA}=\text{effective field goal percentage} \\
TOV\% & =\frac{TOV}{FGA+0.44*FTA+TOV}=\text{turnover percentage} \\
OREB\% & =\frac{OREB}{OREB+DREB_{OPP}}=\text{offensive rebound percentage} \\
DREB\% & =\frac{DREB}{DREB+OREB_{OPP}}=\text{defensive rebound percentage} \\
FTF & =\frac{FT}{FGA}=\text{free throw factor}
\end{align}$$

where $$FT$$ is the number of free throws made and $$3FG$$ is the number of three-point field goals made. The NBA's [definition](http://stats.nba.com/help/faq/) is slightly different than Basketball-Reference.com. The NBA's turnover percentage includes assists in the denominator.

$$TOV\%=\frac{TOV}{FGA+0.44*FTA+AST+TOV}$$

where $$AST$$ is the number of assists. The NBA also uses free throw attempt rate ($$FTA/FGA$$) as the free throw factor instead of free throw rate ($$FT/FGA$$) like Basketball-Reference.com. Basketball-Reference.com uses free throw rate to not only measure how often teams get to the free throw line, but also how often they convert those chances. A lousy free throw shooting team that gets fouled a lot will have a high free throw attempt rate even though their poor foul shooting cost them easy points. However, Basketball-Reference.com's free throw factor is not impressed by fruitless trips to the free throw line. I use Basketball-Reference.com's definition of the four factors for my analysis.

[^1]: Oliver, Dean. *Basketball on Paper: Rules and Tools for Performance Analysis*. Potomac Books, 2004.
