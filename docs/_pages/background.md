---
layout: default
title: Background
permalink: /introduction/background/
---

# The Analytics Movement

The term analytics in sports refers to using statistical analysis to inform decisions ranging from player personnel to in-game team strategy. This idea began in baseball with [sabermetrics](http://sabr.org/sabermetrics), a term coined by Bill James. Statistical evaluations in baseball predate James' work, but his seminal Baseball Abstract[^b8e0094e] helped start the broader movement. This approach was not widely adopted until 2002 when Billy Beane (general manager of the low-budget Oakland Athletics) used objective analytical gauges to exploit market inefficiencies, ushering in the Moneyball[^68a05a53] era. This flew in the face of scouts and their often subjective measures of forecasting player performance. However, the A's were successful with a payroll roughly 40% that of big-budget teams and only about a third that of the free-spending Yankees. As a result, teams from several sports now employ statistical analysts---some even have entire departments---and there is a [conference](http://www.sloansportsconference.com/) dedicated to sports analytics.

[![png](https://upload.wikimedia.org/wikipedia/commons/a/ae/MONEYBALLchart.png){: .center-image width="720px" }](https://en.wikipedia.org/wiki/Moneyball)

The impact of analytics in sports is evident with examples including:

1. MLB's increased emphasis on on-base percentage
2. The [rise of the three-point shot](https://bballbreakdown.com/2016/12/16/the-nba-3-point-revolution/) and fall of the midrange jumper in the NBA
3. Increase in [short, high-percentage passes](https://fivethirtyeight.com/features/running-backs-are-finally-getting-paid-what-theyre-worth/) in the NFL

Sports provide an enticing testbed for machine learning. In a [FiveThirtyEight article](https://fivethirtyeight.com/features/rich-data-poor-data/) by Nate Silver, he identified three reasons "sports nerds have it easy."

1. **Sports has awesome data.** Silver describes sports data as not just big data, but rich data, which he defines as "accurate, precise, and subject to rigorous quality control." Data is also readily available with many websites across a variety of sports offering a plethora of information.
2. **In sports, we know the rules.** This allows us to have strong intuition as to what stats make good predictive variables before ever making a model.
3. **Sports offers fast feedback and clear marks of success.** The objective of sports is winning. While that is not a novel concept, such a clear-cut goal is not always present in other subjects.

# Why the NBA?

I chose to focus on basketball primarily because the NBA is arguably the most deterministic of the major American professional sports leagues, providing a comparatively easier problem to tackle than had I selected another sport. Look no further than the 2017 NBA playoffs, where there are two 8-0 teams in the same conference finals for the [first time](http://www.miamiherald.com/sports/spt-columns-blogs/greg-cote/article150421892.html) in NBA history. Those teams---the Cleveland Cavaliers and Golden State Warriors---seem destined to face each other in the finals for a [third consecutive season](https://fivethirtyeight.com/features/the-cavs-and-warriors-might-be-doing-this-finals-thing-for-a-long-time/). The best teams simply win more often in the NBA than in other sports. A team winning 70% of their games in a given NBA season happens [quite often](http://vizual-statistix.tumblr.com/post/66117099636/edit-due-to-numerous-requests-for-the-addition), and is also a strong indicator the team will do well the following season. The much tighter spread of MLB winning percentages makes baseball quite [difficult to predict](https://fivethirtyeight.com/features/the-imperfect-pursuit-of-a-perfect-baseball-forecast/) consistently. The NFL likes to say it has parity, but it is more an artifact of [small sample size](http://www.sloansportsconference.com/mit_news/exploring-consistency-in-professional-sports-how-the-nfls-parity-is-somewhat-of-a-hoax/). A team that goes on a lucky winning streak can have a record at season's end that is inflated compared to its underlying talent level, making it more difficult to predict. The NHL is also [notoriously random](https://fivethirtyeight.com/features/a-home-playoff-game-is-a-big-advantage-unless-you-play-hockey/).

The Harvard Sports Analysis Collective ([HSAC](http://harvardsportsanalysis.org/)) took an interesting approach and calculated the [Gini coefficient](https://en.wikipedia.org/wiki/Gini_coefficient) of preseason title odds for various sports leagues. The Gini coefficient is a metric used to measure the distribution of a resource---typically to evaluate a nation's income inequality---and ranges from 0 (resources spread evenly) to either 1 or 100% (one person/group holds all the resources). Not only did they find the NBA would be the [world's most unequal economy](http://harvardsportsanalysis.org/2016/10/distribution-of-nba-title-odds-would-be-worlds-most-unequal-economy/), they found the NBA has the [least amount of parity](http://harvardsportsanalysis.org/2016/12/which-sports-league-has-the-most-parity/) of the four major American sports by far. With the recent rise of the Warriors and [Cavs](http://fivethirtyeight.com/features/the-cavs-are-obliterating-the-eastern-conference/) coupled with the Philadelphia 76ers' rebuilding process (read [tanking](http://fivethirtyeight.com/features/the-76ers-would-be-the-worst-expansion-team-in-modern-nba-history/)), the NBA looks more like England's Premier League where the same handful of teams traditionally have any realistic shot at the title each season.

# Sports Betting

The world of sports betting can be very lucrative for those that are skilled at it. The sports bettor Haralabos Voulgaris makes a million dollars in a "bad" year.[^a35eeb24] This potential payout coupled with the perception that anyone can do it leads sports betting to be a big industry. An all-time high of [$4.2 billion](http://www.espn.com/chalk/story/_/id/17892685/the-future-sports-betting-how-sports-betting-legalized-united-states-the-marketplace-look-like) was bet on sports in Nevada in 2015, the sixth straight year a record amount was bet. However, it is difficult to be a successful sports bettor. Oddsmakers are very good at their jobs and teams' records against the spread (one of the most popular sports bets) do not typically deviate far from 50%. A perfect example of this is the 2015-16 Golden State Warriors, who set an NBA record for wins in a season with 73. According to [covers.com](http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/standings/2015-2016/sortable/standings_wins.html), they were a mere 45-35-2 against the spread and their over/under record was nearly identical at 45-36-1, meaning their games hit the over 45 times.

Betting on the spread involves picking winners of games where the favorite is handicapped. For example, if a given team is favored by 5 points and wins by more than 5, they are said to have "covered" and won against the spread. The betting line for this scenario will be set at -5 for the favorite. The opposite holds true for underdogs. They cover by either winning or losing by less than the line. An over/under bet requires comparing the total number of points scored by the two teams in a given game to a number set by the oddsmakers. Bettors must decide if they think the total points scored will be over or under this value. These provide more challenging problems than simply picking game winners.

[^b8e0094e]: *The Bill James Baseball Abstract* by Bill James

[^68a05a53]: *Moneyball: The Art of Winning an Unfair Game* by Michael Lewis

[^a35eeb24]: *The Signal and the Noise: Why So Many Predictions Fail --- but Some Don't* by Nate Silver
