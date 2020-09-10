import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

def plot_feature_importance(weights,feature_names, title):
    """Plots the importance of the features of a given model.

        Args:
            weights:            List with weights of a model (e.g. coefficients of a linear model)
            feature_names:      List with names of the features
            title:              String with label for the plot

    """
    fig, ax = plt.subplots(nrows=1, figsize=(9, 8))

    xc = pd.Series(data=abs(weights), index=feature_names)
    xc.sort_values(ascending=True, inplace=True)
    ax = xc.plot.barh()

    #ax[i].barh(xc.index, xc.values)
    ax.set_title('Label {}'.format(title))
    ax.set_xlabel('Weight')

def plot_true_v_pred(model, X_train, X_test, y_train, y_test, label, title=None):
    """Produces a scatter plot where the true values are given on the x-axis and the predicted values are on the y-axis.

        Args:
            model:              sklearn model used to predict values
            X_train:            pandas.Dataframe with features used for training
            X_test:             pandas.Dataframe with features used for testing
            y_train:            pandas.DataFrame or Series with labels used for training
            y_test:             pandas.DataFrame or Series with labels used for testing
            label:              Name of the label
            title:              Optional title for the plot

    """
    fig, ax = plt.subplots(figsize=(9,6))
    ax.scatter(y_train[label],model.predict(X_train), s=50, label='Training Data')
    ax.scatter(y_test[label],model.predict(X_test), s=50, label='Test Data')
    ax.set_xlabel('True values for {}'.format(label))
    ax.set_ylabel('Predicted values for {}'.format(label))
    if title != None:
        ax.set_title(title)
    ax.legend()
    fig.show()

def plot_partial_dependence(model, X, col, label=None, log=None, bins=10):
    """Produces partial dependece plot for the features given in col.

        Args:
            model:              sklearn model used to predict values
            X:                  pandas.Dataframe with data
            col:                list or str with feature names
            label:              Name of the label
            log:                int or list of ints which control which x-axes should be drawn with log scale
            bins:               int or list of ints which control the number of bins in each histogram

        """
    if type(col) != list:
        col = [col]

    if log == None:
        log = [0] * len(col)
    elif type(log) == int:
        log = [0 if i+1 != log else log for i in range(len(col))]

    if type(bins) != list:
        bins = [bins for i in col]

    X_s = X[col]

    f_mean = defaultdict(list)
    f_var = defaultdict(list)
    for c in col:
        for i, x in enumerate(X_s[c].values):
            X_t = X.copy()
            X_t[c] = x
            pred = model.predict(X_t)
            f_mean[c].append(pred.mean())
            f_var[c].append(pred.var())
        f_mean[c] = np.array(f_mean[c])
        f_var[c] = np.array(f_var[c])

    # if len(col)%2 == 0:
    #     rows = int(len(col)/2)
    #     fig, ax = plt.subplots(figsize=(16, 6 * rows), nrows=rows, ncols=2)
    #     if label is not None:
    #         fig.suptitle("Label {}".format(label), fontsize=16)
    # else:
    #     rows = len(col)
    #     fig, ax = plt.subplots(figsize=(8 * rows, 6), nrows=rows, ncols=1)
    #     if label is not None:
    #         ax[0].set_title("Label {}".format(label), fontsize=16)
    rows = len(col)
    fig, ax = plt.subplots(figsize=(16, 6 * rows), nrows=rows, ncols=2)

    if label is not None:
        fig.suptitle("Label {}".format(label), fontsize=16)

    for i, c in enumerate(col):
        # Plotte Histogramme der Features
        ax[i][0].hist(X[c], bins=bins[i], histtype='stepfilled')
        ax[i][0].set_xlabel(c)
        ax[i][0].set_ylabel('Absolute Häufigkeit')

        # Plotte Partial dependece plots
        x = X[c].sort_values()
        index = x.index
        sigma = np.sqrt(f_var[c])
        # p = 0.05 -> z = 1.64485
        err_h = f_mean[c] + 1.64485 * sigma
        err_l = f_mean[c] - 1.64485 * sigma

        ax[i][1].plot(x, [f_mean[c][i] for i in index], lw=3, label='mean')
        ax[i][1].fill(np.concatenate([x, x[::-1]]),
                      np.concatenate([[err_l[i] for i in index],
                                      [err_h[i] for i in index][::-1]]),
                      alpha=.5, ec='None', color='lightcoral',label='95% CL')

        ax[i][1].set_xlabel(c)
        if log[i] > 0:
           ax[i][1].set_xscale('log')
        ax[i][1].set_ylabel('Partial Dependence')
        ax[i][1].set_xlim((min(X[c])), max(X[c]))
        ax[i][1].set_ylim((0, 1.1 * max(err_h)))
        ax[i][1].legend()

    plt.show();