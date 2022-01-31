from functools import partial

import pandas as pd
from hyperopt import Trials, fmin, space_eval, tpe
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, LabelEncoder

from databall.util import select_columns, stat_names


def calculate_metrics(models, x, y, attributes, param_name, param_vec, k=6):
    # Initialize list of results
    results = [[]]

    # Make transformer that selects the desired attributes from the DataFrame
    selector = FunctionTransformer(partial(select_columns, attributes=attributes, columns=x.columns))

    for i in range(len(models)):
        for param in param_vec:
            # Make a pipeline that selects the desired attributes prior to the classifier
            model = make_pipeline(selector, models[i](**{param_name: param}))
            metrics = cross_val_scoring(model, x, y, k)

            # Calculate performance metrics
            if i == len(results):
                results += [[metrics]]
            else:
                results[i] += [metrics]

    return results


def cross_val_scoring(model, x, y, k=6, random_state=None):
    # Define metrics
    scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'average_precision']

    # Create cross validator
    kfold = StratifiedKFold(n_splits=k, random_state=random_state)

    # Calculate metrics
    return [cross_val_score(model, x, y, cv=kfold, scoring=score).mean() for score in scoring]


def objective(params, model, x, y, attributes, k=6, random_state=None):
    model.set_params(**params)
    kfold = StratifiedKFold(n_splits=k, random_state=random_state)
    score = cross_val_score(model, x[attributes], y, cv=kfold, scoring='accuracy')
    return 1 - score.mean()


def optimize_params(model, x, y, attributes, space, k=6, max_evals=100, eval_space=False):
    trials = Trials()
    best = fmin(partial(objective, model=model, x=x, y=y, attributes=attributes, k=k),
                space, algo=tpe.suggest, max_evals=max_evals, trials=trials)

    param_values = [t['misc']['vals'] for t in trials.trials]
    param_values = [{key: value for key in params for value in params[key]} for params in param_values]

    if eval_space:
        param_values = [space_eval(space, params) for params in param_values]

    param_df = pd.DataFrame(param_values)
    param_df['accuracy'] = [1 - loss for loss in trials.losses()]
    return space_eval(space, best), param_df


def train_test_split(data, start_season, end_season, test_season_start=None, xlabels=None, ylabel='HOME_SPREAD_WL'):
    if test_season_start is None:
        test_season_start = end_season

    if xlabels is None:
        xlabels = stat_names()

    if 'SEASON' in data.columns:
        data = data[xlabels + [ylabel]].dropna()
    else:
        data = data[xlabels + ['SEASON', ylabel]].dropna()

    x, y = data[xlabels], LabelEncoder().fit_transform(data[ylabel])
    x_train = x[(start_season <= data.SEASON) & (data.SEASON < test_season_start)].copy()
    y_train = y[(start_season <= data.SEASON) & (data.SEASON < test_season_start)].copy()
    x_test = x[(test_season_start <= data.SEASON) & (data.SEASON <= end_season)].copy()
    y_test = y[(test_season_start <= data.SEASON) & (data.SEASON <= end_season)].copy()
    return x_train, y_train, x_test, y_test
