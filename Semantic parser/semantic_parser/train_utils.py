import json
import pandas as pd
import warnings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline, make_union
from xgboost import XGBClassifier
from .regex_classifier import PatternMatchingModel, RegexTransformer, LogisticTransformer
from .handcrafted_patterns import regexes, FEATURE_EXPRESSIONS
from .normalization import normalize_target, name2code


def make_maxent_model(x=None, y=None, y_name=None, fnames=None):
    return make_pipeline(
        CountVectorizer(min_df=5, ngram_range=(1, 2)),
        LogisticRegression(penalty='l1', C=0.3, solver='liblinear')
    )


def make_handcrafted_model(x=None, y=None, y_name=None, fnames=None):
    if y_name not in regexes:
        if y_name not in name2code:
            warnings.warn('Name not registered as pattern: {}'.format(y_name))
        y_name = name2code.get(y_name)
    return PatternMatchingModel(class_regexes=regexes[y_name], simplify='both')


def make_feature_extractor():
    return make_union(
        CountVectorizer(min_df=5, ngram_range=(1, 2)),
        RegexTransformer(regexes=FEATURE_EXPRESSIONS)
    )


def make_maxent_handcrafted_model(x=None, y=None, y_name=None, fnames=None):
    return LogisticRegression(penalty='l1', C=3, solver='liblinear')


def make_boosting_model(x=None, y=None, y_name=None, fnames=None):
    # return LogisticRegression(penalty='l1', C=10, solver='liblinear')
    return make_pipeline(
        LogisticTransformer(penalty='l1', C=0.1, solver='liblinear', ffilter='regextransformer', fnames=fnames),
        XGBClassifier(min_child_weight=10, max_depth=5, n_estimators=100, learning_rate=0.1)
    )


MODELS_REGISTER = {
    'maxent': make_maxent_model,
    'handcrafted': make_handcrafted_model,
    'maxent_handcrafted': make_maxent_handcrafted_model,
    'count_and_regex': make_feature_extractor
}


def normalize_target_series(y, target_name):
    return y.apply(normalize_target, target_name=target_name, only_allowed=True)
    

def load_dataset(dataset_name, data_type):
    if data_type == 'pickle':
        data = pd.read_pickle(dataset_name)
    elif data_type == 'tsv':
        data = pd.read_csv(dataset_name, encoding='utf-8', sep='\t')
    else:
        raise ValueError('The data type {} is not supported'.format(data_type))
    return data
  

def load_config(config):
    with open(config, encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data
