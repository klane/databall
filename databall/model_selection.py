from functools import partial
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
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
