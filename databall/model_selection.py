import pandas as pd
from functools import partial
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from hyperopt import fmin, tpe, space_eval, Trials
from databall.util import select_columns


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


def cross_val_scoring(model, x, y, k=6):
    # Define metrics
    scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'average_precision']

    # Create cross validator
    kfold = StratifiedKFold(n_splits=k)

    # Calculate metrics
    return [cross_val_score(model, x, y, cv=kfold, scoring=score).mean() for score in scoring]


def objective(params, model, x, y, attributes, k=6):
    model.set_params(**params)
    kfold = StratifiedKFold(n_splits=k)
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
