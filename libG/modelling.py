from sklearn.metrics import make_scorer, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def model_and_feature_selection(model, X, y, scorer=r2_score, param_grid=None, cv=5, eps=0.00001, plot=False):
    """Performs a greedy feature selection for a given model and parameter grid.

    	Args:
    	    model:              sklearn model to be fitted
    		X:                  Feature Matrix pandas.DataFrame
    		y:                  Label Matrix pandas.DataFrame or pandas.Series
    		scorer:             scorer from sklearn.metrics to determine quality of additional features
    		                    (default: R^2 score for regression)
    		param_grid:         Dictionary parameter grid for the grid search
    		cv:                 Number of cross-validation slices (default 10)
    		eps:                Minimum improvement for additional feature (default 10**(-5))
    		plot:               boolean flag, if True a plot of the scoring evolution will be shown
    		                    (defaut False)

    	Returns:
    		grid_model:         Fitted model with best minimal set of features
    		selected_features:  List of selected features
    """
    # If there's no parameter grid tune the model without grid search
    if param_grid is None:
        grid = model
    else:
        grid = GridSearchCV(model, param_grid, cv=cv, scoring=make_scorer(scorer), n_jobs=-1)

    # Helper function for refitting the models
    def fit_model(grid, features, param_grid):
        if param_grid is None:
            return grid.fit(X[features], y)
        else:
            # In case of a parameter grid perform grid search and select best estimator
            grid.fit(X[features], y)
            return grid.best_estimator_

    features = X.columns.tolist()
    feat_len = len(features)
    selected_features = []
    score = 0.0
    last_score = -1.0
    scores = [score]
    number_of_features = [len(selected_features)]

    while len(selected_features) < feat_len and last_score < score:
        last_score = score
        key = None
        # Iterate over all features...
        for i, f in enumerate(features):
            test_features = selected_features + [f]

            grid_model = fit_model(grid, test_features, param_grid)

            if not plot:
                print('Feature set: ' + ', '.join(test_features) + ' with score: {:.4f}'.format(
                grid_model.score(X[test_features], y)),end='\r')

            if grid_model.score(X[test_features], y) > score + eps:
                key, score = i, grid_model.score(X[test_features], y)

        if key != None:
            # ...remove the best feature from features and add it to selected_features
            new_feat = features.pop(key)
            grid_model = fit_model(grid, selected_features + [new_feat], param_grid)
            if grid_model.score(X[selected_features + [new_feat]], y) > last_score:
                selected_features.append(new_feat)
                score = grid_model.score(X[selected_features], y)
                scores.append(score)
                number_of_features.append(len(selected_features))
        else:
            # when there's no improvement, stop searching, perform a final fit and return
            grid_model = fit_model(grid, selected_features, param_grid)
            print('Final set of features: ' + ', '.join(selected_features) + ' with score: {:.4f}\n'.format(
                grid_model.score(X[selected_features], y)))
            if plot:
                fig, ax = plt.subplots(figsize=(9,6))
                ax.plot(number_of_features, scores, lw=3)
                ax.set_xlabel('Number of features')
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax.set_ylabel('Score')
                fig.tight_layout()
                fig.show()

            return grid_model, selected_features, scores

        # print('Current feature set: ' + ', '.join(selected_features) + ' with score: {:.4f}'.format(
        #     grid_model.score(X[selected_features], y)))

    return grid_model, selected_features, scores