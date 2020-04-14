---
layout: page
title: Outline
permalink: /introduction/outline/
---

The first step was to collect NBA stats, which I downloaded from the NBA's stats website [stats.nba.com](http://stats.nba.com) and stored in a SQLite database. The site is a treasure trove of stats from basic box score stats to advanced stats like offensive and defensive ratings. It even has a number of obscure stats such as shooting percentage in the 4th quarter of road losses. For all the advanced stats the site has, it lacks some team strength stats like Simple Rating System (SRS) that are available on other sites. Since many can be calculated with box score stats, I wrote some code to calculate them from the stats stored in the database to reduce the complexity of the data collection process.

The next step was to collect point spreads and over/under lines in order to make betting predictions. I pulled the data from [covers.com](http://covers.com), which contains historical betting data going back to the 1990-91 season. Each team page contains season schedules like [this one](http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/2016-2017/team403975.html) for the 2016-17 season of my hometown Sacramento Kings. In addition to game results, the pages include betting lines (point spreads), over/under lines, and the results of both types of bets. Once the betting data was combined with the stats, I could use stats and points spreads to predict if teams will win against the spread.

Once all the data was collected, I trained classification models to predict NBA game winners straight up and against the spread given the strengths of the two teams in question. I arranged the data in such a way that only stats from previous games were associated with each game result. I also trained the models using stats prior to the 2016-17 season and reserved the 2016-17 season as a test set. This constitutes a realistic betting scenario for the test set and allows us to see if this methodology is at all worthwhile to apply in the real world.

All code for this project was written in Python and I used the popular machine learning library [scikit-learn](http://scikit-learn.org/stable/)[^1] to train and evaluate all models.

[^1]: Pedregosa et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research* 12 (2011): 2825-2830.
