---
layout: page
title: Outline
permalink: /introduction/outline/
---

The first step is to collect the data, which I downloaded from the NBA's stats website [stats.nba.com](http://stats.nba.com) and store in a database. The site is a treasure trove of stats from basic box score stats to advanced stats like shooting percentage in the 4th quarter of road losses. For all the advanced stats the site has, it lacks some team strength stats like Simple Rating System (SRS) that are available on other sites. Since many can be calculated with box score stats, I wrote code to calculate them from the database to reduce the complexity of the data collection process.

The next step is to train classification models to predict NBA game winners given the strengths of the two teams in question. The models are trained with season-averaged team stats. While this does not constitute a realistic betting scenario, it provides a quick and dirty method to evaluate what algorithms and stats are successful. The conclusions drawn here will inform a future study.

All code for this project is written in Python and I use the popular machine learning library [scikit-learn](http://scikit-learn.org/stable/)[^1] to train and evaluate all models.

[^1]: Pedregosa et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research* 12 (2011): 2825-2830.
