import copy
import re
import numpy as np
import warnings

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.linear_model import LogisticRegression


def simplify(text):
    s = text.lower()
    s = re.sub('\W+', ' ', s)
    s = re.sub('\s+', ' ', s)
    return s


def findall(text, patterns):
    s = simplify(text)
    return {
        t_name: [
            v_name
            for v_name, regex in sub.items()
            if bool(re.match(regex, s))
        ] for t_name, sub in patterns.items()
    }


def choose_result(hypotheses, empty='unknown'):
    result = {
        k: v[0] if len(v) == 1 else empty
        for k, v in hypotheses.items()
    }
    return result


class PatternMatchingModel(BaseEstimator, ClassifierMixin, TransformerMixin):
    def __init__(self, class_regexes, classes=None, default_class='unknown', logistic_correction=0, simplify='both'):
        # todo: maybe, compile them to improve speed
        self.class_regexes = class_regexes
        self.classes_ = classes or []
        self.default_class = default_class
        self.logistic_correction = logistic_correction
        self.simplify = simplify
        # todo: actually implement the logistic correction

    def fit(self, X, y):
        new_classes = sorted(list(set(y).union(self.class_regexes.keys())))
        for new_class in new_classes:
            if new_class not in self.classes_:
                self.classes_.append(new_class)
        self.classes_ = np.array(self.classes_)
        return self

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

    def _get_class_match(self, text, class_name):
        regex = self.class_regexes.get(class_name)
        if not regex:
            return 0
        if not isinstance(regex, list):
            regex = [regex]
        matches = []
        if self.simplify != True:
            for r in regex:
                matches.append(bool(re.match(r, text)))
        if self.simplify != False:
            simplified = simplify(text)
            for r in regex:
                matches.append(bool(re.match(r, simplified)))
        return int(any(matches))

    def predict_proba(self, X, to_numpy=True):
        result = []
        default_class_position = None
        if self.default_class in self.classes_:
            default_class_position = list(self.classes_).index(self.default_class)
        for text in X:
            scores = [self._get_class_match(text, class_name) for class_name in self.classes_]
            scores_sum = sum(scores)
            if scores_sum == 0 and default_class_position is not None:
                scores[default_class_position] = 1
            elif scores_sum > 1:
                scores = [score / scores_sum for score in scores]
            result.append(scores)
        if to_numpy:
            result = np.array(result)
        return result

    def transform(self, X):
        return self.predict_proba(X)


class RegexTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, regexes, simplify='both'):
        names = set()
        for n, r in regexes:
            if n in names:
                warnings.warn('Expression name {} repeats'.format(n))
            names.add(n)
        self.raw_regexes = copy.deepcopy(regexes)
        self.regexes = [
            [name, self._compile(expression)]
            for name, expression in regexes
        ]
        self.simplify = simplify

    def _compile(self, expression):
        try:
            c = re.compile(expression)
        except Exception as e:
            warnings.warn('Could not compile expression {}'.format(expression))
            raise e
        return c

    def fit(self, X, y=None):
        return self

    def fit_transform(self, X, y=None, **fit_params):
        return self.transform(X)

    def get_feature_names(self):
        return [name for name, expression in self.regexes]

    def transform(self, X):
        if self.simplify:
            X = [simplify(text) for text in X]
        result = []
        for text in X:
            row = []
            if self.simplify != False:
                simplified = simplify(text)
            else:
                simplified = text
            for name, regex in self.regexes:
                matched = False
                if self.simplify != True:
                    matched = matched or bool(re.match(regex, text))
                if self.simplify != False:
                    matched = matched or bool(re.match(regex, simplified))
                row.append(int(matched))
            result.append(row)
        return np.array(result)


class DummyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X


class LogisticTransformer(LogisticRegression, TransformerMixin):
    def __init__(self, fnames=None, ffilter=None, **kwargs):
        LogisticRegression.__init__(self, **kwargs)
        self.fnames = fnames
        self.ffilter = ffilter
        self.kept_features = None
        if self.fnames and self.ffilter:
            self.kept_features = np.array([bool(re.match(self.ffilter, c)) for c in self.fnames])

    def transform(self, X):
        tr = self.predict_log_proba(X)
        if self.kept_features is not None:
            X = X[:, self.kept_features].todense()
        return np.concatenate([X, tr], axis=1)
