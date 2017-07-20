---
layout: page
title: Future Work
permalink: /results/future-work/
---

The predictions shown here do not constitute a realistic betting scenario since prospective bettors will only have data available from past games to aid decisions. The next step of this analysis should be to train models with team stats from games prior to the game in question. I will experiment with how much data to use to predict a given game. This window size (the number of games to use) will be a model parameter that must be tuned for maximum performance. This sequential classification methodology will allow me to track model accuracy throughout the season. It will likely be inaccurate at the beginning of the season, but will better predict games as the season goes on and more data becomes available.

After predicting game winners straight up, I will build models to predict winners against Vegas spreads using data from [covers.com](http://covers.com). This is undoubtedly a more difficult problem than simply picking game winners since Vegas oddsmakers are very good at their jobs, as discussed in the [background](background.md). I am also interested in predicting game winners straight up and against the spread using player stats instead of team stats to train the models. The absence of a team's best player due to injury or [rest](https://www.si.com/nba/2017/03/13/warriors-spurs-stephen-curry-kevin-durant-kawhi-leonard-player-rest) generally affects an NBA team more than teams from other sports, which would be reflected in the betting lines and the team's chance of winning. Models built using team stats would not pick up on this, but building a model using player stats from the players in each game's lineup would better account for this.
