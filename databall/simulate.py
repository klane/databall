from hyperopt import fmin, space_eval, tpe
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder


def simulate(model, data, season, predictors, output, build=None, evolve=False, freq=1):
    result = output + '_PRED'
    data = data.copy()
    encoder = LabelEncoder().fit(data[output])
    data[output] = encoder.transform(data[output])
    train, test = data[data.SEASON < season].copy(), data[data.SEASON == season].copy()

    if build is None:
        build = fit

    if evolve:
        test[result] = test[output]
        test_groups = test.groupby('GAME_DATE')
        count = 0

        for day in test_groups.groups:
            if count == freq or count == 0:
                build(model, train[predictors], train[output])
                count = 0

            games = test_groups.get_group(day)
            test.loc[games.index, [result]] = model.predict(games[predictors])
            train = train.append(games)
            count += 1
    else:
        build(model, train[predictors], train[output])
        test[result] = model.predict(test[predictors])

    test[output] = encoder.inverse_transform(test[output])
    test[result] = encoder.inverse_transform(test[result])
    return test


def fit(model, x, y):
    model.fit(x, y)


class HyperOptFit:
    def __init__(self, space, max_evals=10, n_splits=10, scoring='roc_auc', random_state=8):
        self.space = space
        self.max_evals = max_evals
        self.n_splits = n_splits
        self.scoring = scoring
        self.random_state = random_state

    def fit(self, model, x, y):
        best = fmin(lambda params: self.objective(model, params, x, y),
                    self.space, algo=tpe.suggest, max_evals=self.max_evals)
        best_params = space_eval(self.space, best)
        model.set_params(**best_params)
        model.fit(x, y)

    def objective(self, model, params, x, y):
        model.set_params(**params)
        cv = StratifiedKFold(n_splits=self.n_splits, random_state=self.random_state)
        score = cross_val_score(model, x, y, cv=cv, scoring=self.scoring)
        return 1 - score.mean()
