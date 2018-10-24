# <img src="docs/assets/icons/favicon.ico" width="48"> DataBall: Betting on the NBA with data

[![GitHub license](https://img.shields.io/github/license/klane/databall.svg)](https://github.com/klane/databall/blob/master/LICENSE)
[![Requirements Status](https://requires.io/github/klane/databall/requirements.svg?branch=master)](https://requires.io/github/klane/databall/requirements/?branch=master)

--------------------------------------------------------------------------------

This project combines my interest in data science with my love of sports. I attempt to predict NBA winners against the spread using stats pulled from the [NBA stats website](http://stats.nba.com/) with [nba_py](https://github.com/seemethere/nba_py) and point spreads and over/under lines from [covers.com](http://covers.com) using the Python web scraping framework [Scrapy](https://scrapy.org/). All code is written in Python and I used the popular machine learning library [scikit-learn](http://scikit-learn.org/stable/) to make all predictions.

Contents:

-   [covers](https://github.com/klane/databall/tree/master/covers): Scrapy project to scrape point spreads and over/under lines from [covers.com](http://covers.com)
-   [databall](https://github.com/klane/databall/tree/master/databall): Python module with support functions to perform tasks including collecting stats to a SQLite database, simulating seasons, and customizing plots
-   [docs](https://github.com/klane/databall/tree/master/docs): Code required to build the GitHub Pages [site](https://klane.github.io/databall/) for this project
-   [notebooks](https://github.com/klane/databall/tree/master/notebooks): Jupyter notebooks of all analyses
-   [report](https://github.com/klane/databall/tree/master/report): LaTeX files for report and slides
