import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score


def cross_val_curves(model, x, y, k=10):
    plt.figure(figsize=(16, 6))

    # Plot ROC curve
    ax = plt.subplot(121)
    cross_val_roc_curve(model, x, y, ax, k=k, label='Mean', show_folds=True)
    ax.legend()

    # Plot precision/recall curve
    ax = plt.subplot(122)
    cross_val_precision_recall_curve(model, x, y, ax, k=k, label='Mean', show_folds=True)
    ax.legend()
    ax.set_ylim(0.4)

    plt.show()


def cross_val_precision_recall_curve(model, x, y, ax, k=10, label='Mean', show_folds=False):
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
    else:
        ax.plot(mean_recall, mean_precision, label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')


def cross_val_roc_curve(model, x, y, ax, k=10, label='Mean', show_folds=False):
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
    else:
        ax.plot(mean_fpr, mean_tpr, label='%s (Area = %0.2f)' % (label, mean_auc), lw=2)

    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')


def format_538(fig, xlabel, ylabel, title, subtitle, source, xoff, toff, soff, bottomtick=0, sig='line', n=75,
               prefix='', suffix='', suffix_offset=0):
    plt.style.use('fivethirtyeight')
    ax = fig.gca()

    # Add axis labels
    plt.xlabel(xlabel, fontsize=20, weight='bold')
    plt.ylabel(ylabel, fontsize=20, weight='bold')

    # Customize ticks
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.axhline(y=bottomtick, color='black', linewidth=1.3, alpha=0.7)
    [t.set_alpha(0.5) for t in ax.get_xticklabels()]
    [t.set_alpha(0.5) for t in ax.get_yticklabels()]

    fig.canvas.draw()
    ticks = ax.get_yticklabels()
    index = [i for i in range(len(ticks)) if len(ticks[i].get_text()) == 0]
    if len(index) > 0:
        index = max(index) - 1
    else:
        index = len(ticks) - 1
    [t.set_text(t.get_text() + ' '*suffix_offset) for t in ticks[:index]]
    ticks[index].set_text(prefix + ticks[index].get_text() + suffix)
    ax.set_yticklabels(ticks)

    # Add title and subtitle
    plt.text(x=toff[0], y=toff[1], s=title, fontsize=26, weight='bold', alpha=0.75, transform=ax.transAxes)
    plt.text(x=soff[0], y=soff[1], s=subtitle, fontsize=20, alpha=0.85, transform=ax.transAxes)

    # Add signature bar
    label1 = '©Kevin Lane'
    label2 = 'Source: ' + source

    if sig is 'line':
        plt.text(x=xoff, y=-0.1, s='  ' + '_' * n, color='grey', alpha=0.7, transform=ax.transAxes)
        plt.text(x=1.01, y=-0.1, s='_' * n + '  ', color='grey', alpha=0.7, transform=ax.transAxes,
                 horizontalalignment='right')
        plt.text(x=xoff, y=-0.15, s='  ' + label1, fontsize=14, color='grey', transform=ax.transAxes)
        plt.text(x=1.01, y=-0.15, s=label2 + '  ', fontsize=14, color='grey', transform=ax.transAxes,
                 horizontalalignment='right')
    elif sig is 'bar':
        plt.text(x=xoff, y=-0.14, s='  ' + label1 + ' ' * n, fontsize=14, color='#f0f0f0', backgroundcolor='grey',
                 transform=ax.transAxes)
        plt.text(x=1.01, y=-0.14, s=' ' * n + label2 + '  ', fontsize=14, color='#f0f0f0', backgroundcolor='grey',
                 transform=ax.transAxes, horizontalalignment='right')

    plt.show()


def plot_confusion_matrix(cm, classes, title='Confusion Matrix', cmap=plt.get_cmap('Blues')):
    # This function prints and plots the confusion matrix.
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
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
    plt.show()


def plot_metrics(x, y, xlabel, legend, legendsize=14, figsize=(16, 8), log=False):
    rows = 2
    cols = 3
    ylabel = ['Accuracy', 'Precision', 'Recall', 'ROC Area', 'Precision/Recall Area']
    plt.figure(figsize=figsize)

    for i in range(0, len(y[0][0])):
        ax = plt.subplot(100 * rows + 10 * cols + i + 1)

        if log:
            [ax.semilogx(x, [yvec[i] for yvec in y[j]]) for j in range(0, len(y))]
        else:
            [ax.plot(x, [yvec[i] for yvec in y[j]]) for j in range(0, len(y))]
            ax.set_xlim(0)

        ax.set_ylim(0, 1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel[i])
        ax.legend(legend, fontsize=legendsize)

    plt.tight_layout()
    plt.show()
