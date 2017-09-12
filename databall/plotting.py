import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score


def cross_val_curves(model, x, y, k=10, figsize=(16, 6), legend=True):
    fig = plt.figure(figsize=figsize)

    # Plot ROC curve
    ax1 = plt.subplot(121)
    cross_val_roc_curve(model, x, y, ax1, k=k, label='Mean', show_folds=True)

    # Plot precision/recall curve
    ax2 = plt.subplot(122)
    cross_val_precision_recall_curve(model, x, y, ax2, k=k, label='Mean', show_folds=True)

    if legend:
        ax1.legend()
        ax2.legend()

    return fig, ax1, ax2


def cross_val_precision_recall_curve(model, x, y, ax, k=10, label='Mean', show_auc=True, show_folds=False):
    # Compute cross-validated precision/recall curve and area under the curve
    kfold = StratifiedKFold(n_splits=k)
    proba = cross_val_predict(model, x, y, cv=kfold, method='predict_proba')
    mean_precision, mean_recall, thresholds = precision_recall_curve(y, proba[:, 1])
    mean_auc = average_precision_score(y, proba[:, 1])

    # Loop over k folds and get precision/recall curve for each fold
    if show_folds:
        for i, (train, test) in enumerate(kfold.split(x, y)):
            # Fit model for the ith fold
            proba = model.fit(x.iloc[train], y[train]).predict_proba(x.iloc[test])

            # Compute precision/recall curve and area under the curve
            precision, recall, thresholds = precision_recall_curve(y[test], proba[:, 1])
            pr_auc = average_precision_score(y[test], proba[:, 1])
            ax.plot(recall, precision, lw=1, label='Fold %d (Area = %0.2f)' % (i + 1, pr_auc))

        ax.plot(mean_recall, mean_precision, 'k--', label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)
    elif show_auc:
        ax.plot(mean_recall, mean_precision, label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)
    else:
        ax.plot(mean_recall, mean_precision, label=label, lw=2)

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')


def cross_val_roc_curve(model, x, y, ax, k=10, label='Mean', show_auc=True, show_folds=False):
    # Compute cross-validated ROC curve and area under the curve
    kfold = StratifiedKFold(n_splits=k)
    proba = cross_val_predict(model, x, y, cv=kfold, method='predict_proba')
    mean_fpr, mean_tpr, thresholds = roc_curve(y, proba[:, 1])
    mean_auc = roc_auc_score(y, proba[:, 1])

    # Loop over k folds and get ROC curve for each fold
    if show_folds:
        for i, (train, test) in enumerate(kfold.split(x, y)):
            # Fit model for the ith fold
            proba = model.fit(x.iloc[train], y[train]).predict_proba(x.iloc[test])

            # Compute ROC curve and area under the curve
            fpr, tpr, thresholds = roc_curve(y[test], proba[:, 1])
            roc_auc = roc_auc_score(y[test], proba[:, 1])
            ax.plot(fpr, tpr, lw=1, label='Fold %d (Area = %0.2f)' % (i + 1, roc_auc))

        ax.plot(mean_fpr, mean_tpr, 'k--', label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)
    elif show_auc:
        ax.plot(mean_fpr, mean_tpr, label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)
    else:
        ax.plot(mean_fpr, mean_tpr, label=label, lw=2)

    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')


def format_538(fig, source, ax=None, xlabel=None, ylabel=None, title=None, subtitle=None, bottomtick=0, sig='line',
               n=75, xoff=(-0.075, 1.01), yoff=(-0.1, -0.15), toff=(-0.07, 1.15), soff=(-0.07, 1.05),
               prefix='', suffix='', suffix_offset=0):
    plt.style.use('fivethirtyeight')

    if ax is None:
        ax = [fig.gca()]
    elif type(ax) is not list and type(ax) is not tuple:
        ax = [ax]

    if type(bottomtick) is not list and type(bottomtick) is not tuple:
        bottomtick = [bottomtick] * len(ax)

    # Customize axis labels
    if xlabel is None:
        [a.set_xlabel(a.get_xlabel(), fontsize=20, weight='bold') for a in ax]
    elif type(xlabel) is str:
        plt.xlabel(xlabel, fontsize=20, weight='bold')
    else:
        [a.set_xlabel(x, fontsize=20, weight='bold') for a, x in zip(ax, xlabel)]

    if ylabel is None:
        [a.set_ylabel(a.get_ylabel(), fontsize=20, weight='bold') for a in ax]
    elif type(ylabel) is str:
        plt.ylabel(ylabel, fontsize=20, weight='bold')
    else:
        [a.set_ylabel(y, fontsize=20, weight='bold') for a, y in zip(ax, ylabel)]

    # Customize ticks
    [a.tick_params(axis='both', which='major', labelsize=16) for a in ax]
    [a.axhline(y=btick, color='black', linewidth=1.3, alpha=0.7) for a, btick in zip(ax, bottomtick)]
    fig.canvas.draw()
    [t.set_alpha(0.5) for a in ax for t in a.get_xticklabels()]
    [t.set_alpha(0.5) for a in ax for t in a.get_yticklabels()]

    if type(prefix) is str:
        prefix = [prefix]

    if type(suffix) is str:
        suffix = [suffix]

    if type(suffix_offset) is not list and type(suffix_offset) is not tuple:
        suffix_offset = [suffix_offset]

    for (a, p, s, so) in zip(ax, prefix, suffix, suffix_offset):
        ticks = a.get_yticklabels()
        index = [i for i in range(len(ticks)) if len(ticks[i].get_text()) == 0]

        if len(index) > 0:
            index = max(index) - 1
        else:
            index = len(ticks) - 1

        [t.set_text(t.get_text() + ' ' * so) for t in ticks[:index]]
        ticks[index].set_text(p + ticks[index].get_text() + s)
        a.set_yticklabels(ticks)

    # Add title and subtitle
    ax[0].text(x=toff[0], y=toff[1], s=title, fontsize=26, weight='bold', alpha=0.75, transform=ax[0].transAxes)
    ax[0].text(x=soff[0], y=soff[1], s=subtitle, fontsize=20, alpha=0.85, transform=ax[0].transAxes)
    [a.set_title(a.get_title(), fontsize=20, weight='bold') for a in ax]

    # Add signature bar
    label1 = '©Kevin Lane'
    label2 = 'Source: ' + source

    if sig is 'line':
        ax[0].text(x=xoff[0], y=yoff[0], s='  ' + '_' * n, color='grey', alpha=0.7, transform=ax[0].transAxes)
        ax[0].text(x=xoff[1], y=yoff[0], s='_' * n + '  ', color='grey', alpha=0.7, transform=ax[0].transAxes,
                   horizontalalignment='right')
        ax[0].text(x=xoff[0], y=yoff[1], s='  ' + label1, fontsize=14, color='grey', transform=ax[0].transAxes)
        ax[0].text(x=xoff[1], y=yoff[1], s=label2 + '  ', fontsize=14, color='grey', transform=ax[0].transAxes,
                   horizontalalignment='right')
    elif sig is 'bar':
        ax[0].text(x=xoff[0], y=-0.14, s='  ' + label1 + ' ' * n, fontsize=14, color='#f0f0f0', backgroundcolor='grey',
                   transform=ax[0].transAxes)
        ax[0].text(x=xoff[1], y=-0.14, s=' ' * n + label2 + '  ', fontsize=14, color='#f0f0f0', backgroundcolor='grey',
                   transform=ax[0].transAxes, horizontalalignment='right')


def plot_confusion_matrix(cm, classes, title='Confusion Matrix', cmap=plt.get_cmap('Blues')):
    # This function prints and plots the confusion matrix.
    fig = plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    plt.grid(visible=False)

    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    thresh = cm.max() / 2

    for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '%d\n%.2f%%' % (cm[i, j], cm_norm[i, j] * 100),
                 horizontalalignment='center', color='white' if cm[i, j] > thresh else 'black')

    plt.tight_layout()
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')

    return fig


def plot_matrix(x, y, xlabel, ylabel, rows, cols, figsize=(16, 8), logx=False, logy=False):
    fig = plt.figure(figsize=figsize)
    ax = []
    n = len(ylabel)

    if type(logy) is bool:
        logy = [logy] * n

    for i in range(n):
        ax += [plt.subplot(rows, cols, i + 1)]

        if logx and logy[i]:
            ax[i].loglog(x, y[:, i], '.', markersize=5)
        elif logx:
            ax[i].semilogx(x, y[:, i], '.', markersize=5)
        elif logy[i]:
            ax[i].semilogy(x, y[:, i], '.', markersize=5)
        else:
            ax[i].plot(x, y[:, i], '.', markersize=5)

        ax[i].set_xlabel(xlabel)
        ax[i].set_ylabel(ylabel[i])

    return fig, ax


def plot_metrics(x, y, xlabel, legend=None, legendsize=14, figsize=(16, 8), log=False):
    rows = 2
    cols = 3
    ylabel = ['Accuracy', 'Precision', 'Recall', 'ROC Area', 'Precision/Recall Area']
    fig = plt.figure(figsize=figsize)
    ax = []

    for i in range(len(ylabel)):
        ax += [plt.subplot(100 * rows + 10 * cols + i + 1)]

        if log:
            [ax[i].semilogx(x, [yvec[i] for yvec in y[j]]) for j in range(len(y))]
        else:
            [ax[i].plot(x, [yvec[i] for yvec in y[j]]) for j in range(len(y))]
            ax[i].set_xlim(0)

        ax[i].set_ylim(0, 1)
        ax[i].set_xlabel(xlabel)
        ax[i].set_ylabel(ylabel[i])

        if legend is not None:
            ax[i].legend(legend, fontsize=legendsize)

    plt.tight_layout()

    return fig, ax
