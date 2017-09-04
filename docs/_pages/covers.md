---
layout: page
title: Covers
permalink: /data/covers/
---

I combined the stats with spreads and over/under lines obtained from [covers.com](http://covers.com), which provides information going back to the 1990-91 season. I utilized the Python web scraping framework Scrapy for this task.

The Scrapy spider involves crawling pages like [this one](http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/2016-2017/team403975.html) for the 2016-17 season of my hometown Sacramento Kings. Each page includes matchup information (date, opponent, and location), results (score and W/L for the team in question), and betting information (betting line for the team, W/L against the spread, over/under line, and the over/under result). 
