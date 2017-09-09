---
layout: default
title: Home
---

# DataBall

Thank you for visiting my website. It explores a project that combines my interest in data science with my love of sports. The discussion that follows details the process I used to predict NBA game winners against betting lines, from acquiring data to evaluating models. The project's name was inspired by a [Grantland article](http://grantland.com/features/expected-value-possession-nba-analytics/) by Kirk Goldsberry. Several of the pages on this site are converted from [Jupyter Notebooks](http://jupyter.org/), in which case I provide a link to the original notebook hosted on [GitHub]({{ site.github.repository_url }}). This project is a continuation of a [previous project](https://klane.github.io/databall1/) in which I predicted NBA winners straight up using season-averaged stats. I was interested in predicting winners against the spread in a sequential manner to represent a real-life betting scenario, which is what sparked this project.

My first foray into machine learning in sports came in the form of a [Kaggle competition](https://www.kaggle.com/c/march-machine-learning-mania-2014), where competitors were tasked with calculating the odds one team would beat another for each potential matchup of the NCAA men's basketball tournament. Models were evaluated on the [log loss](https://en.wikipedia.org/wiki/Cross_entropy#Cross-entropy_error_function_and_logistic_regression) of their predicted probabilities for the games that actually occurred. This causes models that are incorrectly confident to be heavily penalized. Predicting all possible matchups instead of filling out a traditional bracket also allowed submissions to be easily compared against one another. It would otherwise have been difficult to determine who had the best model since filling out a perfect bracket is [near impossible](http://fivethirtyeight.com/features/the-odds-youll-fill-out-a-perfect-bracket/). This project is a natural progression of that initial work.

As usual, there is a relevant [xkcd](https://xkcd.com/) comic. Let's see what we can learn!

[![png](https://imgs.xkcd.com/comics/machine_learning.png){: .center-image }](https://xkcd.com/1838/)
