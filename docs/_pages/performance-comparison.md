---
layout: default
title: Performance Comparison
permalink: /results/comparison/
---

# Comparison to Published Works

The roughly 70% prediction accuracy achieved on the test set is in line with published results. Zimmermann[^1] used multi-layer perceptron, random forest, and Na&iuml;ve Bayes classifiers implemented in [Weka](http://www.cs.waikato.ac.nz/ml/weka/) to predict the winners of both NBA (2009-2015) and NCAA men's basketball (2009-2013) games. His setup introduced a temporal component, where only previous games were used to predict games. This is a more realistic approach to utilize in a betting scenario where bettors can only draw on past games to inform their decisions. Zimmermann correctly predicted about 57-68% of NBA games correctly depending on the season and method implemented, though the season with 68% accuracy was an outlier. For most seasons, he achieved accuracies below about 64% percent, meaning his models performed marginally better than selecting the home team as the winner. He was more successful in selecting winners in the NCAA, where the range in skill level is usually much larger than in the NBA.

Loeffelholz et al.[^2] used the [MATLAB neural network toolbox](https://www.mathworks.com/products/neural-network.html) to predict the winners of the first 650 games of the 2007-08 NBA season. They performed a 10-fold cross validation with a training set size of 620 games with the remaining 30 games left for testing. They selected the first fold such that the first 620 games of the season were used for training to ensure they were predicting games using only past games. However, the remaining 9 folds used data selected randomly, though each game only appeared in the test set once during cross validation. This process is more akin to my analysis. They achieved an average accuracy of approximately 74%, slightly higher than the accuracy achieved here. It is unclear whether this accuracy holds when tested against multiple seasons instead of the fraction of a season they examined.

[^1]: Zimmermann, Albrecht. "Basketball predictions in the NCAAB and NBA: Similarities and differences." *Statistical Analysis and Data Mining: The ASA Data Science Journal* 9 (2016): 350–364.

[^2]: Loeffelholz, Bernard, Earl Bednar, and Kenneth W. Bauer. "Predicting NBA Games Using Neural Networks." *Journal of Quantitative Analysis in Sports* 5.1 (2009): 1–17.
