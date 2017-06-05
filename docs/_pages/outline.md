---
layout: page
title: Outline
permalink: /introduction/outline/
---

The first step is to train classification models to predict NBA game winners given the strengths of the two teams in question. The models are initially trained with season-averaged team stats. While this does not constitute a realistic betting scenario, it provides a quick and dirty method to evaluate what algorithms and stats are successful. Since bettors will only have data available from past games to aid decisions, I then train models with team stats from games prior to the game in question. I experiment with how much data to use to predict a given game. This window size (the number of games to use) is a model parameter that must be tuned for maximum performance. This sequential classification methodology allows me to track model accuracy throughout the season. It will likely be inaccurate at the beginning of the season, but will better predict games as the season goes on and more data becomes available.

After predicting game winners straight up, I build models to predict winners against the spread using data from [covers.com](http://covers.com). I am also interested in predicting game winners straight up and against the spread using player stats instead of team stats to train the models. The absence of a team's best player generally affects an NBA team more than teams from other sports, which would be reflected in the betting lines. Models built using team stats would not pick up on this, but building a model using player stats from the players in each game's lineup would better account for this.

All code for this project is written in Python and I use the popular machine learning library [scikit-learn](http://scikit-learn.org/stable/index.html)[^1] to train and evaluate all models.

Coming soon:
* Sequential predictions using stats from previous games
* Player-based predictions
* Predictions against the spread

[^1]: Pedregosa et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research* 12 (2011): 2825-2830.
