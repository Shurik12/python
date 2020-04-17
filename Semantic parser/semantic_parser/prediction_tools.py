
import numpy as np
import pandas as pd

from collections import Mapping
from .normalization import UNKNOWN_VALUE


def confident_predict(model, data, threshold=0.5, default_value=UNKNOWN_VALUE):
    """ 
    Apply a sklearn-style classifier to data and replace predictions with low confidence with the default value.
    """
    proba = model.predict_proba(data)
    
    #print (proba)
    
    if isinstance(threshold, (int, float)):
        # take the winner if it is larger than threshold
        pred = model.classes_[proba.argmax(axis=1)]
        pred[proba.max(axis=1) < threshold] = default_value
    elif isinstance(threshold, Mapping):
        # take the winner if the confidence is above
        pred = [default_value] * proba.shape[0]
        for i, row in enumerate(proba):
            winner_score = 0
            for class_name, class_score in zip(model.classes_, row):
                if class_score > winner_score and class_score > threshold.get(class_name, 0.5):
                    winner_score = class_score
                    pred[i] = class_name
        pred = np.array(pred)
    return pred


def gross_metrics(fact, pred, default_value=UNKNOWN_VALUE):
    pred = np.asarray(pred)
    confident = pred != default_value
    gross_recall = np.mean(confident)
    gross_accuracy = np.mean((pred == fact)[confident])
    return gross_recall, gross_accuracy


def print_gross_metrics(facts, preds, keys, verbose=True, **kwargs):
    recalls = []
    accuracies = []
    if verbose:
        print('{:40} {:6} {:6}'.format('Parameter \ Metric', 'Recall', 'Accuracy'))
    template = '{:40} {:6.3f} {:6.3f}'
    for key in keys:
        r, a = gross_metrics(facts[key], preds[key], **kwargs)
        if verbose: 
            print(template.format(key, r, a))
        recalls.append(r)
        accuracies.append(a)
    if verbose:
        meanr = np.mean(recalls)
        meana = np.mean(accuracies)
        print(template.format('Total', meanr, meana))
        print('Product = {:6.4f}'.format(meanr * meana))
    return pd.DataFrame({'recall': recalls, 'accuracy': accuracies}, index=keys)


def report_results(fact, pred):
    # todo: leave only one of these two functions
    has_pred_result = pred != 'unknown'
    has_fact_result = fact != 'unknown'
    eq = fact == pred
    cond_accuracy = (eq & has_pred_result).mean() / has_pred_result.mean()
    gross_recall = (has_fact_result & has_pred_result).mean() / has_fact_result.mean()
    print('recall: {}'.format(gross_recall.mean()))
    print(gross_recall)
    print()
    print('accuracy: {}'.format(cond_accuracy.fillna(0).mean()))
    print(cond_accuracy)
